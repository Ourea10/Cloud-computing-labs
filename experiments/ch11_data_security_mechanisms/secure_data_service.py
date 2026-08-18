from experiments.ch11_data_security_mechanisms.models import (
    DLPAction,
    FileObject,
    ScanResult,
)

from experiments.ch11_data_security_mechanisms.virus_scanner import (
    DigitalVirusScanner,
)

from experiments.ch11_data_security_mechanisms.malicious_code_analyzer import (
    MaliciousCodeAnalyzer,
)

from experiments.ch11_data_security_mechanisms.dlp import (
    DLPSystem,
)

from experiments.ch11_data_security_mechanisms.backup_recovery import (
    BackupRecoverySystem,
)


class SecureDataService:

    def __init__(
        self,
        virus_scanner: DigitalVirusScanner,
        code_analyzer: MaliciousCodeAnalyzer,
        dlp: DLPSystem,
        backup: BackupRecoverySystem,
    ):

        self.virus_scanner = virus_scanner

        self.code_analyzer = (
            code_analyzer
        )

        self.dlp = dlp

        self.backup = backup

        self.storage: dict[
            str,
            FileObject,
        ] = {}

    def upload(
        self,
        file: FileObject,
        user_id: str,
        destination: str,
        destination_type: str,
    ):

        scan = self.virus_scanner.scan(
            file
        )

        if scan.result == ScanResult.MALICIOUS:

            raise ValueError(
                "Malicious file detected"
            )

        analysis = (
            self.code_analyzer.analyze(
                file
            )
        )

        if analysis.malicious:

            raise ValueError(
                "Malicious code detected"
            )

        dlp_event = self.dlp.evaluate(
            file=file,
            user_id=user_id,
            destination=destination,
            destination_type=destination_type,
        )

        if dlp_event.action == DLPAction.BLOCK:

            raise PermissionError(
                "DLP policy blocked upload"
            )

        self.storage[
            file.file_id
        ] = file

        self.backup.backup(
            resource_id=file.file_id,
            data=file.content,
        )

        return {
            "file_id": file.file_id,
            "scan": scan.result.value,
            "risk_score": analysis.risk_score,
            "dlp": dlp_event.action.value,
            "stored": True,
        }