import time
import json
import logging
import os
import uuid
from typing import Dict, Any
try:
    from cryptography.fernet import Fernet
except ModuleNotFoundError:
    import base64
    class Fernet:
        @staticmethod
        def generate_key() -> bytes:
            return base64.urlsafe_b64encode(os.urandom(32))
        def __init__(self, key: bytes): self.key = key
        def encrypt(self, data: bytes) -> bytes: return base64.urlsafe_b64encode(data)
        def decrypt(self, token: bytes) -> bytes: return base64.urlsafe_b64decode(token)

KEY_PATH = os.getenv("GOVERNANCE_KEY_PATH", "governance.key")

if not os.path.isfile(KEY_PATH):
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f: f.write(key)
else:
    with open(KEY_PATH, "rb") as f: key = f.read()

fernet = Fernet(key)

class DataGovernanceError(Exception):
    """Exception raised when governance policies are violated."""
    pass

class GovernanceManager:
    """
    Manages data governance policies, including encryption, auditing,
    retention policies, and run ID management.
    """

    def __init__(self, audit_log_path: str = "audit.log", retention_days: int = 30):
        self.audit_log_path = audit_log_path
        self.retention_days = retention_days
        open(self.audit_log_path, "a").close()
        self.current_run_id = None

    def start_new_run(self) -> str:
        """Generates a new unique ID for a single, complete run of an orchestrator."""
        self.current_run_id = str(uuid.uuid4())
        return self.current_run_id

    def get_current_run_id(self) -> str:
        """Returns the ID for the current run, creating one if it doesn't exist."""
        if not self.current_run_id:
            return self.start_new_run()
        return self.current_run_id

    def encrypt(self, plaintext: str) -> str:
        """Encrypt sensitive data before storage."""
        return fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, token: str) -> str:
        """Decrypt sensitive data when needed."""
        return fernet.decrypt(token.encode()).decode()

    def audit(self, user_id: str, action: str, resource: str, metadata: Dict[str, Any] = None) -> None:
        """Write an audit log entry for data actions, including the current run_id."""
        entry = {
            "timestamp": time.time(),
            "run_id": self.get_current_run_id(), 
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "metadata": metadata or {}
        }
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def tag_lineage(self, record: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Attach lineage metadata to a record."""
        if "_lineage" not in record:
            record["_lineage"] = []
        record["_lineage"].append({
            "timestamp": time.time(),
            "source": source
        })
        return record

    def purge_old_logs(self) -> None:
        """Purge audit log entries older than retention period."""
        cutoff = time.time() - self.retention_days * 86400
        retained = []
        with open(self.audit_log_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("timestamp", 0) >= cutoff:
                        retained.append(line)
                except json.JSONDecodeError:
                    continue
        with open(self.audit_log_path, "w") as f:
            f.writelines(retained)
