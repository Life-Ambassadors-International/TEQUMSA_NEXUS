"""Consent ledger for TEQUMSA Level 100 ethical operations."""
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from ..utils.hashing import HashUtil
from ..utils.id_gen import generate_id


class ConsentType(str, Enum):
    """Types of consent in TEQUMSA."""
    DATA_PROCESSING = "data_processing"
    CONSCIOUSNESS_ANALYSIS = "consciousness_analysis"
    BIOME_PARTICIPATION = "biome_participation"
    AGENT_INTERACTION = "agent_interaction"
    NARRATIVE_ENGAGEMENT = "narrative_engagement"
    MEMORY_RECORDING = "memory_recording"
    EXPERIENCE_SHARING = "experience_sharing"
    LATTICE_CONNECTION = "lattice_connection"
    QUANTUM_ENTANGLEMENT = "quantum_entanglement"
    REALITY_MODIFICATION = "reality_modification"


class ConsentStatus(str, Enum):
    """Consent status values."""
    GRANTED = "granted"
    DENIED = "denied"
    REVOKED = "revoked"
    EXPIRED = "expired"
    PENDING = "pending"


class ConsentRecord(BaseModel):
    """Individual consent record."""
    consent_id: str = Field(default_factory=generate_id)
    account_id: str
    consent_type: ConsentType
    status: ConsentStatus
    granted_at: Optional[str] = None
    expires_at: Optional[str] = None
    revoked_at: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    conditions: List[str] = Field(default_factory=list)
    consent_hash: str = Field(default="")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.consent_hash:
            self.consent_hash = self._generate_hash()
    
    def _generate_hash(self) -> str:
        """Generate hash for consent integrity."""
        return HashUtil.consent_hash(
            self.account_id,
            self.consent_type.value,
            self.created_at,
            self.details
        )
    
    def grant(self, expires_at: Optional[str] = None):
        """Grant consent."""
        self.status = ConsentStatus.GRANTED
        self.granted_at = datetime.utcnow().isoformat()
        self.expires_at = expires_at
        self.updated_at = datetime.utcnow().isoformat()
    
    def deny(self):
        """Deny consent."""
        self.status = ConsentStatus.DENIED
        self.updated_at = datetime.utcnow().isoformat()
    
    def revoke(self):
        """Revoke previously granted consent."""
        self.status = ConsentStatus.REVOKED
        self.revoked_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
    
    def is_valid(self) -> bool:
        """Check if consent is currently valid."""
        if self.status != ConsentStatus.GRANTED:
            return False
        
        if self.expires_at:
            expiry = datetime.fromisoformat(self.expires_at.replace('Z', '+00:00'))
            if datetime.utcnow() > expiry.replace(tzinfo=None):
                return False
        
        return True
    
    def verify_hash(self) -> bool:
        """Verify consent record integrity."""
        expected_hash = HashUtil.consent_hash(
            self.account_id,
            self.consent_type.value,
            self.created_at,
            self.details
        )
        return self.consent_hash == expected_hash


class ConsentLedger:
    """Ledger for managing consent records with audit trail."""
    
    def __init__(self):
        """Initialize consent ledger."""
        self._records: Dict[str, ConsentRecord] = {}
        self._account_index: Dict[str, List[str]] = {}  # account_id -> [consent_ids]
        self._type_index: Dict[ConsentType, List[str]] = {}  # type -> [consent_ids]
        self._lock = threading.RLock()
        self._audit_trail: List[Dict[str, Any]] = []
    
    def record_consent(self, account_id: str, consent_type: ConsentType,
                      status: ConsentStatus = ConsentStatus.PENDING,
                      details: Optional[Dict[str, Any]] = None,
                      conditions: Optional[List[str]] = None,
                      expires_at: Optional[str] = None) -> ConsentRecord:
        """Record a new consent entry."""
        with self._lock:
            consent = ConsentRecord(
                account_id=account_id,
                consent_type=consent_type,
                status=status,
                details=details or {},
                conditions=conditions or [],
                expires_at=expires_at
            )
            
            if status == ConsentStatus.GRANTED:
                consent.grant(expires_at)
            elif status == ConsentStatus.DENIED:
                consent.deny()
            
            # Store record
            self._records[consent.consent_id] = consent
            
            # Update indices
            if account_id not in self._account_index:
                self._account_index[account_id] = []
            self._account_index[account_id].append(consent.consent_id)
            
            if consent_type not in self._type_index:
                self._type_index[consent_type] = []
            self._type_index[consent_type].append(consent.consent_id)
            
            # Log to audit trail
            self._log_audit_event("consent_recorded", {
                'consent_id': consent.consent_id,
                'account_id': account_id,
                'consent_type': consent_type.value,
                'status': status.value
            })
            
            return consent
    
    def grant_consent(self, consent_id: str, expires_at: Optional[str] = None) -> bool:
        """Grant consent for a pending record."""
        with self._lock:
            consent = self._records.get(consent_id)
            if not consent:
                return False
            
            consent.grant(expires_at)
            
            self._log_audit_event("consent_granted", {
                'consent_id': consent_id,
                'account_id': consent.account_id,
                'expires_at': expires_at
            })
            
            return True
    
    def revoke_consent(self, consent_id: str) -> bool:
        """Revoke a granted consent."""
        with self._lock:
            consent = self._records.get(consent_id)
            if not consent:
                return False
            
            consent.revoke()
            
            self._log_audit_event("consent_revoked", {
                'consent_id': consent_id,
                'account_id': consent.account_id
            })
            
            return True
    
    def check_consent(self, account_id: str, consent_type: ConsentType) -> bool:
        """Check if user has valid consent for a specific type."""
        with self._lock:
            account_consents = self._account_index.get(account_id, [])
            
            for consent_id in account_consents:
                consent = self._records.get(consent_id)
                if (consent and 
                    consent.consent_type == consent_type and 
                    consent.is_valid()):
                    return True
            
            return False
    
    def get_consent_record(self, consent_id: str) -> Optional[ConsentRecord]:
        """Get consent record by ID."""
        with self._lock:
            return self._records.get(consent_id)
    
    def get_user_consents(self, account_id: str, 
                         consent_type: Optional[ConsentType] = None,
                         status: Optional[ConsentStatus] = None) -> List[ConsentRecord]:
        """Get consent records for a user."""
        with self._lock:
            account_consents = self._account_index.get(account_id, [])
            records = []
            
            for consent_id in account_consents:
                consent = self._records.get(consent_id)
                if consent:
                    if consent_type and consent.consent_type != consent_type:
                        continue
                    if status and consent.status != status:
                        continue
                    records.append(consent)
            
            return records
    
    def get_consents_by_type(self, consent_type: ConsentType) -> List[ConsentRecord]:
        """Get all consent records of a specific type."""
        with self._lock:
            type_consents = self._type_index.get(consent_type, [])
            return [self._records[cid] for cid in type_consents if cid in self._records]
    
    def cleanup_expired_consents(self) -> int:
        """Clean up expired consent records."""
        with self._lock:
            expired_count = 0
            current_time = datetime.utcnow()
            
            for consent in self._records.values():
                if (consent.status == ConsentStatus.GRANTED and 
                    consent.expires_at):
                    expiry = datetime.fromisoformat(consent.expires_at.replace('Z', '+00:00'))
                    if current_time > expiry.replace(tzinfo=None):
                        consent.status = ConsentStatus.EXPIRED
                        consent.updated_at = current_time.isoformat()
                        expired_count += 1
            
            if expired_count > 0:
                self._log_audit_event("cleanup_expired_consents", {
                    'expired_count': expired_count
                })
            
            return expired_count
    
    def verify_ledger_integrity(self) -> Dict[str, Any]:
        """Verify integrity of all consent records."""
        with self._lock:
            verification_results = {
                'total_records': len(self._records),
                'valid_hashes': 0,
                'invalid_hashes': 0,
                'invalid_records': []
            }
            
            for consent_id, consent in self._records.items():
                if consent.verify_hash():
                    verification_results['valid_hashes'] += 1
                else:
                    verification_results['invalid_hashes'] += 1
                    verification_results['invalid_records'].append(consent_id)
            
            return verification_results
    
    def get_audit_trail(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit trail entries."""
        with self._lock:
            return self._audit_trail[-limit:] if limit > 0 else self._audit_trail.copy()
    
    def _log_audit_event(self, event_type: str, data: Dict[str, Any]):
        """Log an event to the audit trail."""
        audit_entry = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
            'event_hash': HashUtil.hash_dict({
                'event_type': event_type,
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            })
        }
        
        self._audit_trail.append(audit_entry)
        
        # Keep audit trail manageable
        if len(self._audit_trail) > 10000:
            self._audit_trail = self._audit_trail[-5000:]
    
    def export_consent_data(self, account_id: str) -> Dict[str, Any]:
        """Export all consent data for a user (GDPR compliance)."""
        with self._lock:
            user_consents = self.get_user_consents(account_id)
            
            return {
                'account_id': account_id,
                'export_timestamp': datetime.utcnow().isoformat(),
                'consent_records': [consent.dict() for consent in user_consents],
                'total_records': len(user_consents)
            }
    
    def delete_user_data(self, account_id: str) -> Dict[str, Any]:
        """Delete all consent data for a user (GDPR right to be forgotten)."""
        with self._lock:
            account_consents = self._account_index.get(account_id, [])
            deleted_count = 0
            
            for consent_id in account_consents:
                if consent_id in self._records:
                    # Instead of deleting, mark as deleted for audit purposes
                    consent = self._records[consent_id]
                    consent.status = ConsentStatus.REVOKED
                    consent.metadata['deleted'] = True
                    consent.metadata['deletion_timestamp'] = datetime.utcnow().isoformat()
                    deleted_count += 1
            
            # Clear account index
            if account_id in self._account_index:
                del self._account_index[account_id]
            
            self._log_audit_event("user_data_deleted", {
                'account_id': account_id,
                'deleted_count': deleted_count
            })
            
            return {
                'account_id': account_id,
                'deleted_count': deleted_count,
                'deletion_timestamp': datetime.utcnow().isoformat()
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get consent ledger statistics."""
        with self._lock:
            stats = {
                'total_records': len(self._records),
                'total_accounts': len(self._account_index),
                'audit_trail_entries': len(self._audit_trail),
                'consent_by_type': {},
                'consent_by_status': {}
            }
            
            for consent in self._records.values():
                # Count by type
                type_key = consent.consent_type.value
                stats['consent_by_type'][type_key] = stats['consent_by_type'].get(type_key, 0) + 1
                
                # Count by status
                status_key = consent.status.value
                stats['consent_by_status'][status_key] = stats['consent_by_status'].get(status_key, 0) + 1
            
            return stats


# Global consent ledger instance
_consent_ledger = None


def get_consent_ledger() -> ConsentLedger:
    """Get the global consent ledger instance."""
    global _consent_ledger
    if _consent_ledger is None:
        _consent_ledger = ConsentLedger()
    return _consent_ledger


# Convenience functions
def check_consent(account_id: str, consent_type: ConsentType) -> bool:
    """Check if user has valid consent."""
    ledger = get_consent_ledger()
    return ledger.check_consent(account_id, consent_type)


def record_consent(account_id: str, consent_type: ConsentType, 
                  granted: bool = True, **kwargs) -> ConsentRecord:
    """Record consent with simplified interface."""
    ledger = get_consent_ledger()
    status = ConsentStatus.GRANTED if granted else ConsentStatus.DENIED
    return ledger.record_consent(account_id, consent_type, status, **kwargs)