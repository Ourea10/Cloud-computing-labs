import os
import tempfile

from experiments.ch09_specialized_mechanisms.audit_monitor import (
    AuditMonitor,
)

from experiments.ch09_specialized_mechanisms.failover import (
    FailoverSystem,
)

from experiments.ch09_specialized_mechanisms.load_balancer import (
    LoadBalancer,
)

from experiments.ch09_specialized_mechanisms.models import (
    BackendTarget,
    Device,
    DeviceType,
    FailoverMode,
    FailoverResource,
    PricingRule,
    ResourceState,
    ScalingPolicy,
    SLAObjective,
    UsageEvent,
    utc_now,
)

from experiments.ch09_specialized_mechanisms.multi_device_broker import (
    BrokerMessage,
    MultiDeviceBroker,
)

from experiments.ch09_specialized_mechanisms.pay_per_use import (
    PayPerUseMonitor,
)

from experiments.ch09_specialized_mechanisms.resource_cluster import (
    ResourceCluster,
)

from experiments.ch09_specialized_mechanisms.scaling import (
    AutomatedScalingListener,
)

from experiments.ch09_specialized_mechanisms.sla_monitor import (
    SLAMonitor,
)

from experiments.ch09_specialized_mechanisms.state_management import (
    StateManagementDatabase,
)


def demo_scaling():

    print("\n=== Automated Scaling ===")

    listener = AutomatedScalingListener(
        ScalingPolicy(
            min_instances=2,
            max_instances=5,
            scale_out_threshold=70,
            scale_in_threshold=30,
        )
    )

    event = listener.evaluate(
        resource_group="api",
        cpu_percent=85,
        current_count=2,
    )

    print(event)


def demo_load_balancer():

    print("\n=== Load Balancer ===")

    load_balancer = LoadBalancer()

    for index in range(1, 4):

        load_balancer.register(
            BackendTarget(
                resource_id=f"server-{index}",
                address=f"10.0.0.{index}",
                port=8000,
            )
        )

        load_balancer.mark_healthy(
            f"server-{index}"
        )

    for _ in range(6):

        target = (
            load_balancer.select_target()
        )

        print(
            "Request routed to:",
            target.resource_id,
        )

        load_balancer.release_connection(
            target.resource_id
        )

    load_balancer.mark_unhealthy(
        "server-2"
    )

    print(
        "After server-2 failure:"
    )

    for _ in range(4):

        target = (
            load_balancer.select_target()
        )

        print(
            "Request routed to:",
            target.resource_id,
        )

        load_balancer.release_connection(
            target.resource_id
        )


def demo_sla():

    print("\n=== SLA Monitor ===")

    monitor = SLAMonitor()

    monitor.register_objective(
        SLAObjective(
            name="api-availability",
            target=99.0,
            metric="availability",
        )
    )

    values = [
        100.0,
        100.0,
        99.5,
        98.0,
    ]

    for value in values:

        observation = monitor.check(
            "api-availability",
            lambda value=value: value,
        )

        print(observation)

    print(
        "Availability:",
        monitor.availability(
            "api-availability"
        ),
    )


def demo_pay_per_use():

    print("\n=== Pay Per Use ===")

    monitor = PayPerUseMonitor()

    monitor.register_price(
        PricingRule(
            resource_type="vcpu_hour",
            unit="vcpu-hour",
            price_per_unit=0.02,
        )
    )

    charge = monitor.record_usage(
        UsageEvent(
            timestamp=utc_now(),
            tenant_id="tenant-a",
            resource_id="server-001",
            resource_type="vcpu_hour",
            quantity=5,
            unit="vcpu-hour",
        )
    )

    print(charge)

    print(
        "Tenant total:",
        monitor.tenant_total(
            "tenant-a"
        ),
    )


def demo_audit():

    print("\n=== Audit Monitor ===")

    with tempfile.NamedTemporaryFile(
        delete=False
    ) as file:

        path = file.name

    try:

        audit = AuditMonitor(
            log_file=path
        )

        audit.record(
            actor="alice",
            tenant_id="tenant-a",
            action="create_server",
            resource_type="virtual_server",
            resource_id="server-001",
            success=True,
        )

        audit.record(
            actor="alice",
            tenant_id="tenant-a",
            action="delete_server",
            resource_type="virtual_server",
            resource_id="server-002",
            success=False,
        )

        print(
            audit.find_by_actor(
                "alice"
            )
        )

    finally:

        os.unlink(path)


def demo_failover():

    print("\n=== Failover ===")

    system = FailoverSystem()

    system.create_group(
        group_id="api-ha",
        mode=FailoverMode.ACTIVE_PASSIVE,
        resources=[
            FailoverResource(
                resource_id="primary",
                address="10.0.0.1",
                state=ResourceState.ACTIVE,
            ),
            FailoverResource(
                resource_id="secondary",
                address="10.0.0.2",
                state=ResourceState.INACTIVE,
            ),
        ],
    )

    system.fail(
        "api-ha",
        "primary",
    )

    promoted = system.recover(
        "api-ha"
    )

    print(
        "Promoted resource:",
        promoted.resource_id,
    )

    print(
        "State:",
        promoted.state,
    )


def demo_cluster():

    print("\n=== Resource Cluster ===")

    cluster = ResourceCluster(
        "api-cluster"
    )

    for index in range(1, 5):

        cluster.add(
            f"server-{index}"
        )

    print(
        "Health:",
        cluster.health_ratio(),
    )

    cluster.mark_failed(
        "server-1"
    )

    cluster.mark_failed(
        "server-2"
    )

    print(
        "Health after failures:",
        cluster.health_ratio(),
    )

    print(
        "Healthy:",
        cluster.is_healthy(),
    )


def demo_broker():

    print("\n=== Multi-Device Broker ===")

    broker = MultiDeviceBroker()

    broker.register_device(
        Device(
            device_id="server-001",
            device_type=DeviceType.SERVER,
            endpoint="10.0.0.1",
        )
    )

    broker.register_device(
        Device(
            device_id="monitor-001",
            device_type=DeviceType.CLIENT,
            endpoint="monitor",
        )
    )

    broker.subscribe(
        "monitor-001",
        "metrics.cpu",
    )

    broker.publish(
        BrokerMessage(
            source_device="server-001",
            topic="metrics.cpu",
            payload={
                "cpu": 87.5
            },
        )
    )

    message = broker.consume(
        "monitor-001"
    )

    print(message)


def demo_state_database():

    print("\n=== State Management Database ===")

    with tempfile.NamedTemporaryFile(
        suffix=".db",
        delete=False,
    ) as file:

        database_path = file.name

    try:

        database = (
            StateManagementDatabase(
                database_path
            )
        )

        database.save_resource(
            resource_id="server-001",
            resource_type="virtual_server",
            tenant_id="tenant-a",
            state="running",
            metadata='{"cpu": 2}',
        )

        print(
            database.get_resource(
                "server-001"
            )
        )

    finally:

        os.unlink(database_path)


def main():

    demo_scaling()
    demo_load_balancer()
    demo_sla()
    demo_pay_per_use()
    demo_audit()
    demo_failover()
    demo_cluster()
    demo_broker()
    demo_state_database()


if __name__ == "__main__":
    main()