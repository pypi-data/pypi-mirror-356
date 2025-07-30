
"""
Generic, high‑throughput **streaming** JSON → HyGraph loader (file **or** directory).
• Streams large node / edge arrays with **ijson**
• Dense internal IDs via xxhash64 ( ext‑ID → int map ).
• Time‑series blobs automatically attached to their owner.

Example
-------
loader = FastJSONLoader(
    hygraph        = hg,
    nodes_json     = "inputFiles/nodes",   # dir with *.json OR single file
    edges_json     = "inputFiles/edges",   # dir with *.json OR single file
    node_field_map = {"oid": "station_id", "start_time": "start"},
    edge_field_map = {"source_id": "from", "target_id": "to"}
)
loader.run_pipeline()
"""
from __future__ import annotations

import xxhash, ijson
from datetime import datetime
from pathlib   import Path
from typing    import Any, Dict, Optional, Iterable

from hygraph_core.hygraph              import HyGraph
from hygraph_core.timeseries_operators import TimeSeries, TimeSeriesMetadata

FAR_FUTURE_DATE = datetime(2100, 12, 31, 23, 59, 59)

# ---------------------------------------------------------------------------
# helper utils --------------------------------------------------------------
# ---------------------------------------------------------------------------

def fast_hash(val: Any) -> int:
    return xxhash.xxh64(str(val)).intdigest()

def parse_date(s: str | None) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None

def normalize_oid(raw) -> str:
    try:
        f = float(raw)
        return str(int(f)) if f.is_integer() else str(raw)
    except Exception:
        return str(raw)

# ---------------------------------------------------------------------------
# loader --------------------------------------------------------------------
# ---------------------------------------------------------------------------

class FastJSONLoader:
    """Stream huge *.json* node & edge arrays (single file **OR** directory) into HyGraph."""

    def __init__(self,
                 hygraph: HyGraph,
                 node_json_path: str | Path,
                 edge_json_path: str | Path,
                 node_field_map: Dict[str,str] | None = None,
                 edge_field_map: Dict[str,str] | None = None):
        self.hygraph = hygraph
        self.nodes_path = Path(node_json_path)
        self.edges_path = Path(edge_json_path)
        # user maps – may be empty
        self.nmap = node_field_map or {}
        self.emap = edge_field_map or {}
        # external → internal (hashed) ID
        self.ext2int: Dict[str,int] = {}

    # ------------------------------------------------------------------
    def run_pipeline(self):
        print("[JSON] streaming nodes …")
        for file in self._iter_json_files(self.nodes_path):
            self._stream_nodes(file)
        print("[JSON] streaming edges …")
        for file in self._iter_json_files(self.edges_path):
            self._stream_edges(file)
        print("[JSON] done →",
              len(self.hygraph.graph.nodes), "nodes,",
              len(self.hygraph.graph.edges), "edges")

    # ------------------------------------------------------------------
    @staticmethod
    def _iter_json_files(path: Path) -> Iterable[Path]:
        """Yield *.json files – handles file *or* directory input."""
        if path.is_dir():
            for p in sorted(path.iterdir()):
                if p.suffix.lower() == ".json":
                    yield p
        else:
            yield path

    # ------------------------------------------------------------------
    # nodes -------------------------------------------------------------
    # ------------------------------------------------------------------
    def _stream_nodes(self, file: Path):
        with file.open("rb") as f:
            for obj in ijson.items(f, "item"):
                self._process_node(obj)

    def _process_node(self, obj: Dict[str,Any]):
        fm = self.nmap
        oid_key   = fm.get("oid", "id")
        start_key = fm.get("start_time", "start_time")
        end_key   = fm.get("end_time", "end_time")
        label_key = fm.get("label", "label")
        ts_key    = fm.get("time_series_key", "ts")

        oid = normalize_oid(obj.get(oid_key))
        if not oid:
            return
        hid = self.ext2int.setdefault(oid, fast_hash(oid))

        start = parse_date(obj.get(start_key)) or datetime.now()
        end   = parse_date(obj.get(end_key))   or FAR_FUTURE_DATE
        node_label = obj.get(label_key, "node")

        mapped = {oid_key, start_key, end_key, label_key, ts_key}
        props  = {k:v for k,v in obj.items() if k not in mapped}

        if hid not in self.hygraph.graph.nodes:
            self.hygraph.add_pgnode(hid, node_label, start, end, props)
        else:
            self.hygraph.graph.nodes[hid]["data"].static_properties.update(props)

        ts_blob = obj.get(ts_key, {})
        if isinstance(ts_blob, dict):
            self._attach_time_series(hid, ts_blob, "node")

    # ------------------------------------------------------------------
    # edges -------------------------------------------------------------
    # ------------------------------------------------------------------
    def _stream_edges(self, file: Path):
        with file.open("rb") as f:
            for obj in ijson.items(f, "item"):
                self._process_edge(obj)

    def _process_edge(self, obj: Dict[str,Any]):
        fm = self.emap
        oid_key   = fm.get("oid", "id")
        src_key   = fm.get("source_id", "source_id")
        tgt_key   = fm.get("target_id", "target_id")
        start_key = fm.get("start_time", "start_time")
        end_key   = fm.get("end_time", "end_time")
        label_key = fm.get("label", "label")
        ts_key    = fm.get("time_series_key", "ts")

        oid = normalize_oid(obj.get(oid_key, f"edge_{id(obj)}"))
        hid = fast_hash(oid)

        s_ext = normalize_oid(obj.get(src_key))
        t_ext = normalize_oid(obj.get(tgt_key))
        s_int = self.ext2int.get(s_ext)
        t_int = self.ext2int.get(t_ext)
        if s_int is None or t_int is None:
            return  # missing endpoint → skip

        start = parse_date(obj.get(start_key)) or datetime.now()
        end   = parse_date(obj.get(end_key))   or FAR_FUTURE_DATE
        label = obj.get(label_key, "edge")

        mapped = {oid_key, src_key, tgt_key, start_key, end_key, label_key, ts_key}
        props  = {k:v for k,v in obj.items() if k not in mapped}

        if not self.hygraph.graph.has_edge(s_int, t_int, key=hid):
            self.hygraph.add_pgedge(hid, s_int, t_int, label, start, end, props)
        else:
            self.hygraph.graph[s_int][t_int][hid]["data"].static_properties.update(props)

        ts_blob = obj.get(ts_key, {})
        if isinstance(ts_blob, dict):
            self._attach_time_series(hid, ts_blob, "edge")

    # ------------------------------------------------------------------
    # time‑series -------------------------------------------------------
    # ------------------------------------------------------------------
    def _attach_time_series(self, owner_id: int, blob: Dict[str,Any], element_type: str):
        for name, arr in blob.items():
            if not isinstance(arr, list):
                continue
            tsid = f"{owner_id}_{name}"
            if tsid in self.hygraph.time_series:
                continue  # duplicate guard
            timestamps = [parse_date(d.get("Start")) or datetime.now() for d in arr]
            values     = [[d.get("Value", 0)] for d in arr]
            meta = TimeSeriesMetadata(owner_id, element_type)
            ts   = TimeSeries(tsid, timestamps, [name], values, meta)
            self.hygraph.time_series[tsid] = ts
            if element_type == "node":
                self.hygraph.graph.nodes[owner_id]["data"].add_temporal_property(name, ts, self.hygraph)
            else:
                for u,v,k,d in self.hygraph.graph.edges(keys=True, data=True):
                    if k == owner_id:
                        d["data"].add_temporal_property(name, ts, self.hygraph)
                        break
