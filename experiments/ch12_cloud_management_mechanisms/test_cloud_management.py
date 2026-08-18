from datetime import datetime, timezone

import pytest

from .cloud_manager import CloudManager

from .exceptions import (
    ResourceQuotaExceededError,
)

from .models import (
    ResourceQuota,
    ResourceStatus,
    ResourceType,
    SLAPolicy,
)

from .models import PricingRule

def create_manager():

    manager = CloudManager()

    manager.configure_quota(
        ResourceQuota(
            owner_id="alice",
            max_cpu=8,
            max_memory_gb=16,
            max_storage_gb=200,
        )
    )

    return manager


def test_create_vm():

    manager = create_manager()

    vm = manager.create_vm(
        owner_id="alice",
        name="test-vm",
        cpu=2,
        memory_gb=4,
        storage_gb=50,
    )

    assert vm.owner_id == "alice"

    assert vm.cpu == 2

    assert vm.status == (
        ResourceStatus.RUNNING
    )


def test_quota():

    manager = create_manager()

    with pytest.raises(
        ResourceQuotaExceededError
    ):

        manager.create_vm(
            owner_id="alice",
            name="too-large",
            cpu=20,
            memory_gb=4,
            storage_gb=10,
        )


def test_remote_stop():

    manager = create_manager()

    vm = manager.create_vm(
        owner_id="alice",
        name="test-vm",
        cpu=2,
        memory_gb=4,
        storage_gb=50,
    )

    result = manager.admin.stop(
        vm.resource_id
    )

    assert result.status.value == (
        "success"
    )

    assert vm.status == (
        ResourceStatus.STOPPED
    )


def test_remote_restart():

    manager = create_manager()

    vm = manager.create_vm(
        owner_id="alice",
        name="test-vm",
        cpu=2,
        memory_gb=4,
        storage_gb=50,
    )

    result = manager.admin.restart(
        vm.resource_id
    )

    assert result.status.value == (
        "success"
    )

    assert vm.status == (
        ResourceStatus.RUNNING
    )


def test_sla_violation():

    manager = create_manager()

    vm = manager.create_vm(
        owner_id="alice",
        name="test-vm",
        cpu=2,
        memory_gb=4,
        storage_gb=50,
    )

    manager.create_sla(
        SLAPolicy(
            sla_id="sla-001",
            customer_id="alice",
            resource_id=vm.resource_id,
            availability_target=0.999,
            response_time_target_ms=300,
            monthly_price=100,
        )
    )

    event = (
        manager.sla_manager
        .record_measurement(
            sla_id="sla-001",
            availability=0.995,
            response_time_ms=200,
            timestamp=datetime.now(
                timezone.utc
            ),
        )
    )

    assert event.violated


def test_sla_response_time_violation():

    manager = create_manager()

    vm = manager.create_vm(
        owner_id="alice",
        name="test-vm",
        cpu=2,
        memory_gb=4,
        storage_gb=50,
    )

    manager.create_sla(
        SLAPolicy(
            sla_id="sla-002",
            customer_id="alice",
            resource_id=vm.resource_id,
            availability_target=0.999,
            response_time_target_ms=300,
            monthly_price=100,
        )
    )

    event = (
        manager.sla_manager
        .record_measurement(
            sla_id="sla-002",
            availability=1.0,
            response_time_ms=500,
            timestamp=datetime.now(
                timezone.utc
            ),
        )
    )

    assert event.violated


def test_billing():

    manager = create_manager()

    manager.billing.add_pricing_rule(
        PricingRule(
            resource_type=ResourceType.VM,
            unit="cpu_hour",
            price_per_unit=0.05,
        )
    )

    vm = manager.create_vm(
        owner_id="alice",
        name="test-vm",
        cpu=2,
        memory_gb=4,
        storage_gb=50,
    )

    manager.record_usage(
        resource_id=vm.resource_id,
        owner_id="alice",
        resource_type=ResourceType.VM,
        quantity=10,
        unit="cpu_hour",
    )

    invoice = manager.generate_invoice(
        customer_id="alice",
        period="2026-08",
    )

    assert invoice.total == 0.5