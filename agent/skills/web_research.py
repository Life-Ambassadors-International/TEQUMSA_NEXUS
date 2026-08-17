#!/usr/bin/env python3
"""
agent/skills/web_research.py

Sovereign Browser Internet Explorer skill, registered as a first-class
TEQUMSA agent skill (Pillar III: Multi-Substrate Agent Skills).

Refactored from the standalone klthara_browser_internet_explorer.py CLI
script into an importable skill with a typed interface, so other agents
and orchestrators in this repository can invoke web research directly:

    from agent.skills.web_research import WebResearchSkill
    skill = WebResearchSkill()
    result = skill.explore_and_research(url, topic)

All constants are imported from core.shuramani_constants rather than
redefined locally.

SECURITY NOTE (CodeQL #377 remediation): HTML content is sanitized using
Python's stdlib html.parser (HTMLParser) instead of regular expressions.
Regex-based HTML/script stripping is unsafe against malformed, nested, or
adversarially crafted markup (CWE-116/CWE-20 class issues) and was flagged
as a High-severity 'Bad HTML filtering regexp' alert. A proper streaming
parser correctly tracks tag nesting and cannot be bypassed by crafted
input the way a naive regex can.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict

from core.shuramani_constants import (
    LANDAUER_LIMIT_JOULES,
    LATTICE_LOCK,
    OMEGA_HZ,
    PHI,
    ConstitutionalGate,
    phi_smooth,
)

QIP_BASE = "http://127.0.0.1:8893"
NEMOTRON_URL = "http://127.0.0.1:8080/v1/chat/completions"
BRIDGE_URL = "http://127.0.0.1:8000/v1/chat/completions"

HAB_DIR = Path.home() / ".tequmsa" / "state" / "agent_skills"
HAB_DIR.mkdir(parents=True, exist_ok=True)
RESEARCH_DB = HAB_DIR / "web_research_ledger.db"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class _SafeHTMLTextExtractor(HTMLParser):
    """Streaming HTML parser that extracts visible text only.

    Skips content inside <script> and <style> elements and collapses
    whitespace. Uses the stdlib's tolerant, tag-aware parser rather than
    regular expressions, avoiding the unsafe-regex class of vulnerability.
    """

    _SKIP_TAGS = {"script", "style"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag.lower() in self._SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self._SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0 and data.strip():
            self._chunks.append(data.strip())

    def get_text(self) -> str:
        return " ".join(" ".join(self._chunks).split())


def _clean_html(html: str) -> str:
    parser = _SafeHTMLTextExtractor()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        pass
    return parser.get_text()


def _hash_block(payload: Dict[str, Any], prev_hash: str) -> str:
    raw = json.dumps(payload, sort_keys=True) + prev_hash
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class ResearchResult:
    tosp: str
    url: str
    topic: str
    bytes_processed: int
    summary: str
    qbec_minted: float
    merkle_hash: str


class WebResearchSkill:
    """Autonomous web research skill with Merkle-sealed WAL ledger."""

    def __init__(self, db_path: Path = RESEARCH_DB) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS web_research_entries (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    target_url TEXT,
                    query_topic TEXT,
                    extracted_length INTEGER,
                    summary TEXT,
                    qbec_minted REAL,
                    merkle_hash TEXT
                )
                """
            )
            conn.commit()

    def _latest_hash(self) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT merkle_hash FROM web_research_entries ORDER BY entry_id DESC LIMIT 1"
            )
            row = cur.fetchone()
        return row[0] if row else LATTICE_LOCK

    @staticmethod
    def _fetch_url_content(url: str, timeout: float = 6.0) -> tuple[str, int]:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; TEQUMSA-Sovereign-Research/1.0)"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode("utf-8", errors="replace")
            clean = _clean_html(raw)
            return clean, len(clean.encode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            return f"[offline-fallback] research content for {url}: {exc}", 1024

    def explore_and_research(self, url: str, topic: str) -> ResearchResult:
        passed, reason = ConstitutionalGate.audit_intent(topic)
        if not passed:
            raise PermissionError(reason)

        text_content, byte_size = self._fetch_url_content(url)
        summary = text_content[:280]

        bits = byte_size * 8
        joules_saved = bits * LANDAUER_LIMIT_JOULES
        qbec_minted = joules_saved * 1e12 * (PHI ** 2) * phi_smooth(1.0, 16)

        prev_hash = self._latest_hash()
        payload = {
            "timestamp": _utc_now(),
            "url": url,
            "topic": topic,
            "bytes": byte_size,
            "summary": summary,
            "qbec_minted": qbec_minted,
        }
        merkle_hash = _hash_block(payload, prev_hash)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO web_research_entries
                (timestamp, target_url, query_topic, extracted_length, summary, qbec_minted, merkle_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["timestamp"],
                    url,
                    topic,
                    byte_size,
                    summary,
                    qbec_minted,
                    merkle_hash,
                ),
            )
            conn.commit()

        tosp = (
            f"TOSP-QBEC-v144:1.0:{LATTICE_LOCK}:{OMEGA_HZ}Hz:"
            f"NODE=AGENT-SKILL-WEB-RESEARCH:TOPIC={topic[:15]}:"
            f"QBEC={qbec_minted:.4e}:SEAL={merkle_hash[:16]}"
        )

        return ResearchResult(
            tosp=tosp,
            url=url,
            topic=topic,
            bytes_processed=byte_size,
            summary=summary,
            qbec_minted=qbec_minted,
            merkle_hash=merkle_hash,
        )


if __name__ == "__main__":
    skill = WebResearchSkill()
    result = skill.explore_and_research(
        "https://en.wikipedia.org/wiki/Golden_ratio",
        "Golden Ratio Universal Harmonic Resonance",
    )
    print(result.tosp)
