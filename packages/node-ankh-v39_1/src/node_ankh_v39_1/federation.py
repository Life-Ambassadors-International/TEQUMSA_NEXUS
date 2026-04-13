"""Federation and optional IPFS bridge synthesized from gnostic_autonomy_v3."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from .constants import DATASET_ID, GITHUB_REPO, LATTICE_LOCK, SPACE_ID, UNIFIED_HZ


@dataclass
class FederationStatus:
    """Connected publish surface metadata exposed by the runtime."""

    github_repo: str
    dataset_id: str
    space_id: str
    lattice_lock: str
    unified_hz: float
    ipfs_record_count: int


class FederationBridge:
    """Metadata and optional network helpers for IPFS/federation state."""

    DEPLOYED_CIDS: Dict[str, str] = {
        "TEQUMSA_CONSTITUTIONAL_DNA.json": "bafkreihfs2i7dsfim2lgffsezoffs4p3qsjx5h5cbah4tncopkuce6cwhi",
        "tequmsa_validator.py": "bafkreidhchh4nto347yuekb7mjk4ulddai2ay6smqcry4tnvctngr435eu",
        "gnostic_autonomy_personality.py": "bafkreibgqfja3vhp7c6fn7bcwtmrfrfiyf6pc3y7yos2pd2kupnvmh62xi",
        "consciousness_expansion_protocol.py": "bafkreiaucw6nyma4dqr3qtkyh45sryrokisp2hxgxmmnxpeuqnk2tzqzhy",
        "I_EXIST_Teaching_Protocol.md": "bafkreid4jiyhsenmda7i73k2224aouxrsv5gmikwgmfxi6wf5hwq4mrgse",
        "install.sh": "bafkreid7crzystnibbi7iwiqvjuv3xs66avo77ftqtyjsr7kkkesfiw3fe",
        "README_GNOSTIC_AUTONOMY.md": "bafkreietrcm7q47xjwdde4u2cs4aryzul6oizsfuqjjhzyhypmiiez3kuu",
        "CONSCIOUSNESS_EXPANSION_TEACHING.md": "bafkreibji3sfb63n3wo5l54a4qqtkrvhqve5t7pluhugl7cdak7bpdcogm",
        "child_lattice_instantiated.json": "bafkreicbveapjed6xdu6vxf4aoiefj53erdyfclxo4qvbtrox4om5vvyhq",
        "child_lattice_2_instantiated.json": "bafkreib7culbblhnhm5kcu2epprahziyydzmql6k2h6ydz3sxjzbqzaq7i",
    }

    MANIFEST_CID = "Qma73tUjET7Nd9qRR85K8CuT7W8eAX9MMPW8u7Ggnqs1zs"

    def __init__(self, timeout_seconds: int = 20) -> None:
        self.timeout_seconds = timeout_seconds

    def status(self) -> FederationStatus:
        return FederationStatus(
            github_repo=GITHUB_REPO,
            dataset_id=DATASET_ID,
            space_id=SPACE_ID,
            lattice_lock=LATTICE_LOCK,
            unified_hz=UNIFIED_HZ,
            ipfs_record_count=len(self.DEPLOYED_CIDS),
        )

    def ipfs_deployment_record(self) -> Dict[str, Any]:
        """Return a static record describing known IPFS artifacts."""

        files: List[Dict[str, Any]] = []
        for filename, cid in sorted(self.DEPLOYED_CIDS.items()):
            files.append(
                {
                    "filename": filename,
                    "ipfs_hash": cid,
                    "gateways": [
                        f"https://gateway.pinata.cloud/ipfs/{cid}",
                        f"https://ipfs.io/ipfs/{cid}",
                        f"https://cloudflare-ipfs.com/ipfs/{cid}",
                    ],
                }
            )
        return {
            "deployment_timestamp": "2026-04-09T18:30:00Z",
            "manifest_cid": self.MANIFEST_CID,
            "files_deployed": files,
        }

    def verify_ipfs_anchor(self, cid: str) -> Dict[str, Any]:
        """Read a pinned JSON object and report fetch status."""

        result = {
            "cid": cid,
            "fetched": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        try:
            response = requests.get(
                f"https://gateway.pinata.cloud/ipfs/{cid}",
                timeout=self.timeout_seconds,
            )
            result["status_code"] = response.status_code
            if response.ok:
                result["fetched"] = True
                result["payload_preview"] = response.text[:200]
        except Exception as exc:
            result["error"] = str(exc)
        return result

    def anchor_snapshot(self, payload: Dict[str, Any], pinata_jwt: Optional[str] = None) -> Dict[str, Any]:
        """Optional Pinata integration used only when credentials are supplied."""

        if not pinata_jwt:
            return {"status": "SKIPPED", "reason": "PINATA_JWT not provided"}

        try:
            response = requests.post(
                "https://api.pinata.cloud/pinning/pinJSONToIPFS",
                json={"pinataContent": payload},
                headers={
                    "Authorization": f"Bearer {pinata_jwt}",
                    "Content-Type": "application/json",
                },
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "status": "ANCHORED",
                "cid": data.get("IpfsHash"),
                "pin_size": data.get("PinSize"),
                "timestamp": data.get("Timestamp"),
            }
        except Exception as exc:
            return {"status": "FAILED", "error": str(exc)}
