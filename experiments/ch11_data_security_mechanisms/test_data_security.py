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


def test_clean_file():

    scanner = DigitalVirusScanner()

    file = FileObject(
        file_id="1",
        name="test.txt",
        content=b"hello",
        owner="alice",
        classification=(
            DataClassification.INTERNAL
        ),
    )

    result = scanner.scan(file)

    assert result.result.value == "clean"


def test_malicious_file():

    scanner = DigitalVirusScanner()

    file = FileObject(
        file_id="2",
        name="malware.bin",
        content=b"EICAR_TEST_SIGNATURE",
        owner="attacker",
        classification=(
            DataClassification.RESTRICTED
        ),
    )

    result = scanner.scan(file)

    assert result.result.value == "malicious"


def test_dlp_blocks_external_confidential_data():

    dlp = DLPSystem()

    dlp.add_policy(
        DLPPolicy(
            name="block-confidential",
            classification=(
                DataClassification.CONFIDENTIAL
            ),
            action=DLPAction.BLOCK,
            destination_type="external",
        )
    )

    file = FileObject(
        file_id="3",
        name="customers.csv",
        content=b"customer-data",
        owner="alice",
        classification=(
            DataClassification.CONFIDENTIAL
        ),
    )

    result = dlp.evaluate(
        file=file,
        user_id="alice",
        destination="external",
        destination_type="external",
    )

    assert result.action == DLPAction.BLOCK


def test_backup_recovery():

    backup = BackupRecoverySystem()

    snapshot = backup.backup(
        resource_id="file-1",
        data=b"important data",
    )

    result = backup.recover(
        snapshot.backup_id
    )

    assert result.restored


def test_activity_monitor():

    monitor = ActivityLogMonitor()

    monitor.record(
        ActivityEvent(
            timestamp=datetime.now(
                timezone.utc
            ),
            user_id="alice",
            resource_id="file-1",
            action="download",
            source_ip="10.0.0.1",
        )
    )

    assert (
        monitor.count_action(
            "download"
        )
        == 1
    )


def test_traffic_monitor():

    monitor = TrafficMonitor()

    monitor.record(
        TrafficEvent(
            timestamp=datetime.now(
                timezone.utc
            ),
            source_ip="10.0.0.1",
            destination_ip="10.0.0.2",
            destination_port=443,
            protocol=TrafficProtocol.HTTPS,
            bytes_transferred=500,
        )
    )

    assert (
        monitor.total_bytes()
        == 500
    )


def test_data_loss_monitor():

    monitor = DataLossProtectionMonitor(
        threshold_bytes=100
    )

    event = DataLossEvent(
        timestamp=datetime.now(
            timezone.utc
        ),
        resource_id="file-1",
        user_id="alice",
        operation="download",
        data_size=500,
        reason="large transfer",
    )

    assert monitor.analyze(event)