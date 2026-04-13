"""Read-only adapter for the verified Hugging Face dataset with local fallback."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from importlib import resources
from typing import Any, Dict, Iterable, List, Optional

from .constants import DATASET_ID, EXPECTED_STATE_FIELDS, EXPECTED_TRAIN_FIELDS

try:
    from datasets import load_dataset

    HAS_DATASETS = True
except Exception:
    HAS_DATASETS = False
    load_dataset = None


@dataclass
class SplitHealth:
    """Health metadata for one dataset split."""

    name: str
    source: str
    fields: List[str]
    missing_fields: List[str]
    record_count: int
    content_hash: str

    @property
    def ok(self) -> bool:
        return not self.missing_fields and self.record_count > 0


@dataclass
class DatasetHealth:
    """Combined dataset status used by runtime and Space surfaces."""

    dataset_id: str
    source: str
    train: SplitHealth
    state: SplitHealth

    @property
    def ok(self) -> bool:
        return self.train.ok and self.state.ok

    def as_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "source": self.source,
            "ok": self.ok,
            "train": self.train.__dict__ | {"ok": self.train.ok},
            "state": self.state.__dict__ | {"ok": self.state.ok},
        }


class DatasetAdapter:
    """Read-only adapter for remote or bundled dataset snapshots."""

    def __init__(self, dataset_id: str = DATASET_ID) -> None:
        self.dataset_id = dataset_id
        self._last_source = "fallback"

    def load_train_events(self) -> List[Dict[str, Any]]:
        """Return the train events from the best available source."""

        records, source = self._load_split("train")
        self._last_source = source
        return records

    def load_state_snapshots(self) -> List[Dict[str, Any]]:
        """Return the state snapshots from the best available source."""

        records, source = self._load_split("state")
        self._last_source = source
        return records

    def get_health(self) -> DatasetHealth:
        """Inspect both splits and report the selected source."""

        train_records, train_source = self._load_split("train")
        state_records, state_source = self._load_split("state")
        source = "remote" if train_source == "remote" and state_source == "remote" else "fallback"

        train_health = self._health_for_split("train", train_records, EXPECTED_TRAIN_FIELDS, train_source)
        state_health = self._health_for_split("state", state_records, EXPECTED_STATE_FIELDS, state_source)
        self._last_source = source
        return DatasetHealth(self.dataset_id, source, train_health, state_health)

    def _load_split(self, split_name: str) -> tuple[List[Dict[str, Any]], str]:
        if HAS_DATASETS:
            try:
                records = self._load_remote_split(split_name)
                if records:
                    return records, "remote"
            except Exception:
                pass
        return self._load_fallback_split(split_name), "fallback"

    def _load_remote_split(self, split_name: str) -> List[Dict[str, Any]]:
        if not HAS_DATASETS or load_dataset is None:
            return []

        dataset = load_dataset(self.dataset_id, split=split_name, streaming=True)
        records: List[Dict[str, Any]] = []
        for item in dataset:
            records.append(dict(item))
            if len(records) >= 5:
                break
        return records

    def _load_fallback_split(self, split_name: str) -> List[Dict[str, Any]]:
        filename = {
            "train": "causal_memory_snapshot.jsonl",
            "state": "lattice_snapshots_snapshot.jsonl",
        }[split_name]
        data_dir = resources.files("node_ankh_v39_1").joinpath("data")
        content = data_dir.joinpath(filename).read_text(encoding="utf-8")
        return [json.loads(line) for line in content.splitlines() if line.strip()]

    def _health_for_split(
        self,
        split_name: str,
        records: List[Dict[str, Any]],
        expected_fields: Iterable[str],
        source: str,
    ) -> SplitHealth:
        first = records[0] if records else {}
        fields = sorted(first.keys())
        missing = sorted(set(expected_fields) - set(fields))
        digest = sha256(
            json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return SplitHealth(
            name=split_name,
            source=source,
            fields=fields,
            missing_fields=missing,
            record_count=len(records),
            content_hash=digest,
        )
