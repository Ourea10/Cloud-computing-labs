from experiments.ch08_infrastructure.infrastructure import (
    CloudInfrastructure,
)

from experiments.ch09_specialized_mechanisms.audit_monitor import (
    AuditMonitor,
)

from experiments.ch09_specialized_mechanisms.failover import (
    FailoverSystem,
)

from experiments.ch09_specialized_mechanisms.load_balancer import (
    LoadBalancer,
)

from experiments.ch09_specialized_mechanisms.pay_per_use import (
    PayPerUseMonitor,
)

from experiments.ch09_specialized_mechanisms.resource_cluster import (
    ResourceCluster,
)

from experiments.ch09_specialized_mechanisms.scaling import (
    AutomatedScalingListener,
    ScalingController,
)

from experiments.ch09_specialized_mechanisms.sla_monitor import (
    SLAMonitor,
)

from experiments.ch09_specialized_mechanisms.state_management import (
    StateManagementDatabase,
)


class SpecializedCloudController:

    def __init__(
        self,
        cloud: CloudInfrastructure,
        state_database: StateManagementDatabase,
        audit_monitor: AuditMonitor,
        load_balancer: LoadBalancer,
        sla_monitor: SLAMonitor,
        pay_per_use: PayPerUseMonitor,
        failover: FailoverSystem,
    ):

        self.cloud = cloud

        self.state_database = (
            state_database
        )

        self.audit_monitor = (
            audit_monitor
        )

        self.load_balancer = (
            load_balancer
        )

        self.sla_monitor = (
            sla_monitor
        )

        self.pay_per_use = (
            pay_per_use
        )

        self.failover = failover

        self.clusters: dict[
            str,
            ResourceCluster,
        ] = {}

    def create_cluster(
        self,
        cluster_id: str,
    ) -> ResourceCluster:

        cluster = ResourceCluster(
            cluster_id
        )

        self.clusters[
            cluster_id
        ] = cluster

        return cluster

    def record_resource_state(
        self,
        resource_id: str,
        resource_type: str,
        tenant_id: str,
        state: str,
        metadata: str = "{}",
    ) -> None:

        self.state_database.save_resource(
            resource_id=resource_id,
            resource_type=resource_type,
            tenant_id=tenant_id,
            state=state,
            metadata=metadata,
        )

    def audit(
        self,
        actor: str,
        tenant_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None,
        success: bool,
        metadata: dict | None = None,
    ):

        return self.audit_monitor.record(
            actor=actor,
            tenant_id=tenant_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            success=success,
            metadata=metadata,
        )