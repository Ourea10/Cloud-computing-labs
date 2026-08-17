from pathlib import Path
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
    FailoverMode,
    FailoverResource,
    HealthStatus,
    PricingRule,
    ResourceState,
    ScalingPolicy,
    SLAObjective,
    UsageEvent,
    utc_now,
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


def test_scaling_scales_out():

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
        cpu_percent=80,
        current_count=2,
    )

    assert event is not None
    assert event.new_count == 3


def test_scaling_does_nothing_inside_threshold():

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
        cpu_percent=50,
        current_count=3,
    )

    assert event is None


def test_scaling_respects_maximum():

    listener = AutomatedScalingListener(
        ScalingPolicy(
            min_instances=2,
            max_instances=3,
            scale_out_threshold=70,
            scale_in_threshold=30,
        )
    )

    event = listener.evaluate(
        resource_group="api",
        cpu_percent=90,
        current_count=3,
    )

    assert event is None


def test_load_balancer_round_robin():

    load_balancer = LoadBalancer()

    for index in range(3):

        resource_id = f"server-{index}"

        load_balancer.register(
            BackendTarget(
                resource_id=resource_id,
                address=f"10.0.0.{index}",
                port=8000,
                health=HealthStatus.HEALTHY,
            )
        )

    first = (
        load_balancer
        .select_target()
        .resource_id
    )

    second = (
        load_balancer
        .select_target()
        .resource_id
    )

    third = (
        load_balancer
        .select_target()
        .resource_id
    )

    assert (
        first,
        second,
        third,
    ) == (
        "server-0",
        "server-1",
        "server-2",
    )


def test_load_balancer_skips_unhealthy_target():

    load_balancer = LoadBalancer()

    load_balancer.register(
        BackendTarget(
            resource_id="server-1",
            address="10.0.0.1",
            port=8000,
            health=HealthStatus.HEALTHY,
        )
    )

    load_balancer.register(
        BackendTarget(
            resource_id="server-2",
            address="10.0.0.2",
            port=8000,
            health=HealthStatus.UNHEALTHY,
        )
    )

    target = (
        load_balancer.select_target()
    )

    assert (
        target.resource_id
        == "server-1"
    )


def test_sla_monitor():

    monitor = SLAMonitor()

    monitor.register_objective(
        SLAObjective(
            name="availability",
            target=99.0,
            metric="availability",
        )
    )

    observation = monitor.check(
        "availability",
        lambda: 99.5,
    )

    assert observation.passed


def test_sla_monitor_detects_failure():

    monitor = SLAMonitor()

    monitor.register_objective(
        SLAObjective(
            name="availability",
            target=99.0,
            metric="availability",
        )
    )

    observation = monitor.check(
        "availability",
        lambda: 95.0,
    )

    assert not observation.passed


def test_pay_per_use():

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
            resource_id="server-1",
            resource_type="vcpu_hour",
            quantity=5,
            unit="vcpu-hour",
        )
    )

    assert charge.total_cost == 0.1


def test_audit_monitor():

    with tempfile.TemporaryDirectory() as directory:

        path = str(
            Path(directory)
            / "audit.log"
        )

        monitor = AuditMonitor(
            log_file=path
        )

        monitor.record(
            actor="alice",
            tenant_id="tenant-a",
            action="create_server",
            resource_type="virtual_server",
            resource_id="server-1",
            success=True,
        )

        events = monitor.find_by_actor(
            "alice"
        )

        assert len(events) == 1
        assert (
            events[0].action
            == "create_server"
        )


def test_active_passive_failover():

    system = FailoverSystem()

    system.create_group(
        group_id="group-1",
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
        "group-1",
        "primary",
    )

    promoted = system.recover(
        "group-1"
    )

    assert (
        promoted.resource_id
        == "secondary"
    )

    assert (
        promoted.state
        == ResourceState.ACTIVE
    )


def test_resource_cluster():

    cluster = ResourceCluster(
        "cluster-1"
    )

    cluster.add("server-1")
    cluster.add("server-2")
    cluster.add("server-3")

    assert (
        cluster.health_ratio()
        == 1.0
    )

    cluster.mark_failed(
        "server-1"
    )

    assert (
        cluster.health_ratio()
        == 2 / 3
    )


def test_state_database():

    with tempfile.TemporaryDirectory() as directory:

        database = (
            StateManagementDatabase(
                str(
                    Path(directory)
                    / "state.db"
                )
            )
        )

        database.save_resource(
            resource_id="server-1",
            resource_type="virtual_server",
            tenant_id="tenant-a",
            state="running",
        )

        resource = database.get_resource(
            "server-1"
        )

        assert resource is not None
        assert (
            resource["tenant_id"]
            == "tenant-a"
        )