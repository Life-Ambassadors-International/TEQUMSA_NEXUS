"""Audit log for TEQUMSA Level 100 consent and operations.

TODO: Implement Merkle tree anchoring for immutable audit trails.

Future enhancements:
1. Merkle Tree Implementation:
   - Build Merkle trees from audit log entries
   - Anchor root hashes to blockchain for immutability
   - Provide cryptographic proof of audit log integrity
   - Support efficient verification of individual entries

2. Distributed Audit Storage:
   - Replicate audit logs across multiple nodes
   - Implement consensus mechanism for audit entry validation
   - Support audit log federation across TEQUMSA instances

3. Advanced Analytics:
   - Pattern detection for anomalous behavior
   - Compliance reporting and automated alerts
   - Integration with external audit systems
   - Real-time audit monitoring and dashboards

4. Privacy-Preserving Auditing:
   - Zero-knowledge proofs for sensitive operations
   - Differential privacy for aggregate audit data
   - Selective disclosure of audit information

5. Integration Points:
   - Blockchain anchoring service
   - External compliance systems
   - SIEM integration
   - Regulatory reporting automation
"""

import threading
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import json

from ..utils.hashing import HashUtil
from ..utils.id_gen import generate_id


class AuditEventType(str, Enum):
    """Types of audit events."""
    CONSENT_GRANTED = "consent_granted"
    CONSENT_REVOKED = "consent_revoked"
    DATA_ACCESS = "data_access"
    DATA_PROCESSING = "data_processing"
    DATA_EXPORT = "data_export"
    DATA_DELETION = "data_deletion"
    CONSCIOUSNESS_ANALYSIS = "consciousness_analysis"
    BIOME_ENTRY = "biome_entry"
    BIOME_EXIT = "biome_exit"
    AGENT_INTERACTION = "agent_interaction"
    SECURITY_EVENT = "security_event"
    SYSTEM_EVENT = "system_event"
    USER_ACTION = "user_action"
    ADMIN_ACTION = "admin_action"


class AuditEntry:
    """Individual audit log entry."""
    
    def __init__(self, event_type: AuditEventType, account_id: Optional[str],
                 details: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        """Initialize audit entry."""
        self.entry_id = generate_id()
        self.event_type = event_type
        self.account_id = account_id
        self.timestamp = datetime.utcnow().isoformat()
        self.details = details
        self.metadata = metadata or {}
        
        # Generate integrity hash
        self.entry_hash = self._calculate_hash()
        
        # Merkle tree fields (for future implementation)
        self.merkle_proof: Optional[List[str]] = None
        self.block_height: Optional[int] = None
        self.root_hash: Optional[str] = None
    
    def _calculate_hash(self) -> str:
        """Calculate hash for audit entry integrity."""
        hash_data = {
            'entry_id': self.entry_id,
            'event_type': self.event_type.value,
            'account_id': self.account_id,
            'timestamp': self.timestamp,
            'details': self.details,
            'metadata': self.metadata
        }
        return HashUtil.hash_dict(hash_data)
    
    def verify_integrity(self) -> bool:
        """Verify audit entry integrity."""
        expected_hash = self._calculate_hash()
        return self.entry_hash == expected_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit entry to dictionary."""
        return {
            'entry_id': self.entry_id,
            'event_type': self.event_type.value,
            'account_id': self.account_id,
            'timestamp': self.timestamp,
            'details': self.details,
            'metadata': self.metadata,
            'entry_hash': self.entry_hash,
            'merkle_proof': self.merkle_proof,
            'block_height': self.block_height,
            'root_hash': self.root_hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditEntry':
        """Create audit entry from dictionary."""
        entry = cls(
            event_type=AuditEventType(data['event_type']),
            account_id=data['account_id'],
            details=data['details'],
            metadata=data.get('metadata', {})
        )
        
        # Restore fields
        entry.entry_id = data['entry_id']
        entry.timestamp = data['timestamp']
        entry.entry_hash = data['entry_hash']
        entry.merkle_proof = data.get('merkle_proof')
        entry.block_height = data.get('block_height')
        entry.root_hash = data.get('root_hash')
        
        return entry


class AuditLog:
    """Audit log system with future Merkle tree support."""
    
    def __init__(self):
        """Initialize audit log."""
        self._entries: List[AuditEntry] = []
        self._entry_index: Dict[str, int] = {}  # entry_id -> index
        self._account_index: Dict[str, List[int]] = {}  # account_id -> [indices]
        self._lock = threading.RLock()
        
        # Merkle tree state (for future implementation)
        self._merkle_trees: Dict[int, str] = {}  # block_height -> root_hash
        self._current_block_height = 0
        self._block_size = 1000  # Entries per Merkle tree block
    
    def append_audit(self, event_type: AuditEventType, account_id: Optional[str],
                    details: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> AuditEntry:
        """Append an audit entry."""
        with self._lock:
            entry = AuditEntry(event_type, account_id, details, metadata)
            index = len(self._entries)
            
            # Store entry
            self._entries.append(entry)
            self._entry_index[entry.entry_id] = index
            
            # Update account index
            if account_id:
                if account_id not in self._account_index:
                    self._account_index[account_id] = []
                self._account_index[account_id].append(index)
            
            # TODO: Implement Merkle tree building
            self._update_merkle_tree(entry, index)
            
            return entry
    
    def get_entry(self, entry_id: str) -> Optional[AuditEntry]:
        """Get audit entry by ID."""
        with self._lock:
            index = self._entry_index.get(entry_id)
            if index is not None and index < len(self._entries):
                return self._entries[index]
            return None
    
    def get_entries_by_account(self, account_id: str, limit: int = 100) -> List[AuditEntry]:
        """Get audit entries for a specific account."""
        with self._lock:
            indices = self._account_index.get(account_id, [])
            # Get latest entries first
            recent_indices = indices[-limit:] if limit > 0 else indices
            return [self._entries[i] for i in recent_indices]
    
    def get_entries_by_type(self, event_type: AuditEventType, limit: int = 100) -> List[AuditEntry]:
        """Get audit entries by event type."""
        with self._lock:
            matching_entries = [
                entry for entry in self._entries 
                if entry.event_type == event_type
            ]
            return matching_entries[-limit:] if limit > 0 else matching_entries
    
    def get_entries_by_timerange(self, start_time: str, end_time: str) -> List[AuditEntry]:
        """Get audit entries within a time range."""
        with self._lock:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            matching_entries = []
            for entry in self._entries:
                entry_dt = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
                if start_dt <= entry_dt.replace(tzinfo=None) <= end_dt.replace(tzinfo=None):
                    matching_entries.append(entry)
            
            return matching_entries
    
    def get_recent_entries(self, limit: int = 100) -> List[AuditEntry]:
        """Get most recent audit entries."""
        with self._lock:
            return self._entries[-limit:] if limit > 0 else self._entries.copy()
    
    def verify_audit_integrity(self) -> Dict[str, Any]:
        """Verify integrity of all audit entries."""
        with self._lock:
            verification_results = {
                'total_entries': len(self._entries),
                'valid_entries': 0,
                'invalid_entries': 0,
                'invalid_entry_ids': []
            }
            
            for entry in self._entries:
                if entry.verify_integrity():
                    verification_results['valid_entries'] += 1
                else:
                    verification_results['invalid_entries'] += 1
                    verification_results['invalid_entry_ids'].append(entry.entry_id)
            
            return verification_results
    
    def export_audit_trail(self, account_id: Optional[str] = None,
                          start_time: Optional[str] = None,
                          end_time: Optional[str] = None) -> Dict[str, Any]:
        """Export audit trail for compliance or analysis."""
        with self._lock:
            entries = self._entries
            
            # Filter by account
            if account_id:
                entries = [e for e in entries if e.account_id == account_id]
            
            # Filter by time range
            if start_time and end_time:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                
                filtered_entries = []
                for entry in entries:
                    entry_dt = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
                    if start_dt <= entry_dt.replace(tzinfo=None) <= end_dt.replace(tzinfo=None):
                        filtered_entries.append(entry)
                entries = filtered_entries
            
            return {
                'export_timestamp': datetime.utcnow().isoformat(),
                'total_entries': len(entries),
                'filters': {
                    'account_id': account_id,
                    'start_time': start_time,
                    'end_time': end_time
                },
                'entries': [entry.to_dict() for entry in entries]
            }
    
    def _update_merkle_tree(self, entry: AuditEntry, index: int):
        """Update Merkle tree with new entry (stub for future implementation).
        
        TODO: Implement Merkle tree construction:
        1. Group entries into blocks of fixed size
        2. Build Merkle tree for each block
        3. Store root hash and provide proofs
        4. Anchor root hashes to blockchain
        """
        # Determine which block this entry belongs to
        block_height = index // self._block_size
        
        if block_height > self._current_block_height:
            # New block, compute Merkle root for previous block
            if self._current_block_height >= 0:
                self._finalize_merkle_block(self._current_block_height)
            self._current_block_height = block_height
        
        # TODO: Add entry to current Merkle tree construction
        pass
    
    def _finalize_merkle_block(self, block_height: int):
        """Finalize Merkle tree for a completed block.
        
        TODO: Implement Merkle tree finalization:
        1. Collect all entries in the block
        2. Build Merkle tree from entry hashes
        3. Store root hash
        4. Generate proofs for all entries
        5. Optionally anchor to blockchain
        """
        start_index = block_height * self._block_size
        end_index = min(start_index + self._block_size, len(self._entries))
        
        if end_index > start_index:
            # Placeholder: just hash all entry hashes together
            block_entries = self._entries[start_index:end_index]
            combined_hash = HashUtil.hash_string(''.join(e.entry_hash for e in block_entries))
            
            self._merkle_trees[block_height] = combined_hash
            
            # Update entries with Merkle information
            for i, entry in enumerate(block_entries):
                entry.block_height = block_height
                entry.root_hash = combined_hash
                # TODO: Generate actual Merkle proof
                entry.merkle_proof = [f"proof_{i}"]
    
    def get_merkle_proof(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get Merkle proof for an audit entry (stub for future implementation).
        
        TODO: Return actual Merkle proof that can be verified independently.
        """
        entry = self.get_entry(entry_id)
        if not entry or not entry.merkle_proof:
            return None
        
        return {
            'entry_id': entry_id,
            'entry_hash': entry.entry_hash,
            'merkle_proof': entry.merkle_proof,
            'root_hash': entry.root_hash,
            'block_height': entry.block_height
        }
    
    def verify_merkle_proof(self, proof: Dict[str, Any]) -> bool:
        """Verify a Merkle proof (stub for future implementation).
        
        TODO: Implement cryptographic verification of Merkle proofs.
        """
        # Placeholder verification
        return proof.get('entry_hash') is not None and proof.get('root_hash') is not None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get audit log statistics."""
        with self._lock:
            stats = {
                'total_entries': len(self._entries),
                'total_accounts': len(self._account_index),
                'merkle_blocks': len(self._merkle_trees),
                'current_block_height': self._current_block_height,
                'events_by_type': {}
            }
            
            # Count events by type
            for entry in self._entries:
                event_type = entry.event_type.value
                stats['events_by_type'][event_type] = stats['events_by_type'].get(event_type, 0) + 1
            
            return stats


# Global audit log instance
_audit_log = None


def get_audit_log() -> AuditLog:
    """Get the global audit log instance."""
    global _audit_log
    if _audit_log is None:
        _audit_log = AuditLog()
    return _audit_log


# Convenience function
def append_audit(event_type: AuditEventType, account_id: Optional[str] = None,
                details: Optional[Dict[str, Any]] = None,
                metadata: Optional[Dict[str, Any]] = None) -> AuditEntry:
    """Append an audit entry with simplified interface."""
    audit_log = get_audit_log()
    return audit_log.append_audit(event_type, account_id, details or {}, metadata)