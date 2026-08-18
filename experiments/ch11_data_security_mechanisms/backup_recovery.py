import hashlib
import uuid

from datetime import datetime, timezone

from experiments.ch11_data_security_mechanisms.models import (
    BackupSnapshot,
    RecoveryResult,
)


class BackupRecoverySystem:

    def __init__(self):

        self.backups: dict[
            str,
            BackupSnapshot,
        ] = {}

    def backup(
        self,
        resource_id: str,
        data: bytes,
    ) -> BackupSnapshot:

        checksum = hashlib.sha256(
            data
        ).hexdigest()

        snapshot = BackupSnapshot(
            backup_id=str(uuid.uuid4()),
            resource_id=resource_id,
            created_at=datetime.now(
                timezone.utc
            ),
            data=data,
            checksum=checksum,
        )

        self.backups[
            snapshot.backup_id
        ] = snapshot

        return snapshot

    def recover(
        self,
        backup_id: str,
    ) -> RecoveryResult:

        snapshot = self.backups[
            backup_id
        ]

        current_checksum = (
            hashlib.sha256(
                snapshot.data
            ).hexdigest()
        )

        valid = (
            current_checksum
            == snapshot.checksum
        )

        return RecoveryResult(
            backup_id=backup_id,
            resource_id=snapshot.resource_id,
            restored=valid,
        )