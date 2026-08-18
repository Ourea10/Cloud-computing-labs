from datetime import datetime, timezone

from experiments.ch11_data_security_mechanisms.models import (
    ActivityEvent,
    DataClassification,
    DataLossEvent,
    DLPAction,
    DLPPolicy,
    FileObject,
    TrafficEvent,
    TrafficProtocol,
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

from experiments.ch11_data_security_mechanisms.activity_log_monitor import (
    ActivityLogMonitor,
)

from experiments.ch11_data_security_mechanisms.traffic_monitor import (
    TrafficMonitor,
)

from experiments.ch11_data_security_mechanisms.data_loss_protection import (
    DataLossProtectionMonitor,
)

from experiments.ch11_data_security_mechanisms.secure_data_service import (
    SecureDataService,
)


def main():

    print(
        "=== Chapter 11: Data Security ==="
    )

    virus_scanner = (
        DigitalVirusScanner()
    )

    code_analyzer = (
        MaliciousCodeAnalyzer()
    )

    dlp = DLPSystem()

    dlp.add_policy(
        DLPPolicy(
            name="block-confidential-external",
            classification=(
                DataClassification.CONFIDENTIAL
            ),
            action=DLPAction.BLOCK,
            destination_type="external",
        )
    )

    backup = BackupRecoverySystem()

    activity_monitor = (
        ActivityLogMonitor()
    )

    traffic_monitor = TrafficMonitor()

    data_loss_monitor = (
        DataLossProtectionMonitor(
            threshold_bytes=100_000_000
        )
    )

    service = SecureDataService(
        virus_scanner=virus_scanner,
        code_analyzer=code_analyzer,
        dlp=dlp,
        backup=backup,
    )

    clean_file = FileObject(
        file_id="file-001",
        name="report.txt",
        content=b"Cloud computing report",
        owner="alice",
        classification=(
            DataClassification.INTERNAL
        ),
    )

    result = service.upload(
        file=clean_file,
        user_id="alice",
        destination="internal-storage",
        destination_type="internal",
    )

    print(
        "\nUpload result:"
    )

    print(result)

    activity_monitor.record(
        ActivityEvent(
            timestamp=datetime.now(
                timezone.utc
            ),
            user_id="alice",
            resource_id="file-001",
            action="upload",
            source_ip="10.0.0.10",
        )
    )

    traffic_monitor.record(
        TrafficEvent(
            timestamp=datetime.now(
                timezone.utc
            ),
            source_ip="10.0.0.10",
            destination_ip="10.0.1.20",
            destination_port=443,
            protocol=TrafficProtocol.HTTPS,
            bytes_transferred=1024,
        )
    )

    suspicious = (
        data_loss_monitor.analyze(
            DataLossEvent(
                timestamp=datetime.now(
                    timezone.utc
                ),
                resource_id="file-001",
                user_id="alice",
                operation="download",
                data_size=500_000_000,
                reason="Large external transfer",
            )
        )
    )

    print(
        "\nLarge data transfer detected:",
        suspicious,
    )

    print(
        "\nActivity count:",
        len(
            activity_monitor.find_by_user(
                "alice"
            )
        ),
    )

    print(
        "\nTraffic bytes:",
        traffic_monitor.total_bytes(),
    )


if __name__ == "__main__":
    main()