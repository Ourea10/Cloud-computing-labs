from .infrastructure.network import (
    LocalNetworkProvider,
)

from .infrastructure.compute import (
    LocalComputeProvider,
)

from .infrastructure.storage import (
    LocalStorageProvider,
)

from .infrastructure.queue import (
    LocalQueue,
)

from .repositories.user_repository import (
    UserRepository,
)

from .repositories.project_repository import (
    ProjectRepository,
)

from .repositories.resource_repository import (
    ResourceRepository,
)

from .repositories.metric_repository import (
    MetricRepository,
)

from .repositories.alert_repository import (
    AlertRepository,
)

from .services.auth_service import (
    AuthService,
)

from .services.project_service import (
    ProjectService,
)

from .services.resource_service import (
    ResourceService,
)

from .services.monitoring_service import (
    MonitoringService,
)

from .services.alert_service import (
    AlertService,
)

from .services.audit_service import (
    AuditService,
)

from .services.delivery_service import (
    DeliveryService,
)

from .workers.metrics_worker import (
    MetricsWorker,
)


def print_section(title: str):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main():

    print_section(
        "CHAPTER 17 - FINAL CLOUD PLATFORM"
    )

    # ==========================================================
    # 1. NETWORK
    # ==========================================================

    print_section("1. NETWORK")

    network = LocalNetworkProvider()

    vpc_id = network.create_network(
        name="learning-vpc",
        cidr="10.0.0.0/16",
    )

    public_subnet_id = (
        network.create_subnet(
            network_id=vpc_id,
            name="public-subnet",
            cidr="10.0.1.0/24",
        )
    )

    private_subnet_id = (
        network.create_subnet(
            network_id=vpc_id,
            name="private-subnet",
            cidr="10.0.2.0/24",
        )
    )

    print(
        f"VPC: {vpc_id}"
    )

    print(
        f"Public subnet: "
        f"{public_subnet_id}"
    )

    print(
        f"Private subnet: "
        f"{private_subnet_id}"
    )

    # ==========================================================
    # 2. DELIVERY MODEL
    # ==========================================================

    print_section(
        "2. DELIVERY MODEL"
    )

    delivery_service = (
        DeliveryService()
    )

    delivery_model = (
        delivery_service.recommend(
            {
                "minimal_operations": True
            }
        )
    )

    print(
        f"Recommended model: "
        f"{delivery_model.name}"
    )

    print(
        f"Compute responsibility: "
        f"{delivery_model.compute}"
    )

    print(
        f"Operating system responsibility: "
        f"{delivery_model.operating_system}"
    )

    print(
        f"Application responsibility: "
        f"{delivery_model.application}"
    )

    # ==========================================================
    # 3. REPOSITORIES
    # ==========================================================

    print_section(
        "3. INITIALIZE APPLICATION"
    )

    user_repository = (
        UserRepository()
    )

    project_repository = (
        ProjectRepository()
    )

    resource_repository = (
        ResourceRepository()
    )

    metric_repository = (
        MetricRepository()
    )

    alert_repository = (
        AlertRepository()
    )

    # ==========================================================
    # 4. SERVICES
    # ==========================================================

    auth_service = AuthService(
        user_repository
    )

    project_service = ProjectService(
        project_repository
    )

    resource_service = ResourceService(
        resource_repository
    )

    monitoring_service = (
        MonitoringService(
            metric_repository
        )
    )

    alert_service = AlertService(
        alert_repository
    )

    audit_service = AuditService()

    # ==========================================================
    # 5. AUTHENTICATION
    # ==========================================================

    print_section(
        "4. USER REGISTRATION"
    )

    user = auth_service.register(
        email="alice@example.com",
        password="alice-password",
    )

    print(
        f"Created user: "
        f"{user.email}"
    )

    authenticated_user = (
        auth_service.authenticate(
            email="alice@example.com",
            password="alice-password",
        )
    )

    if authenticated_user is None:

        print(
            "Authentication failed"
        )

        return

    print(
        f"Authenticated user: "
        f"{authenticated_user.email}"
    )

    audit_service.record(
        actor_id=authenticated_user.id,
        action="LOGIN",
    )

    # ==========================================================
    # 6. PROJECT
    # ==========================================================

    print_section(
        "5. CREATE PROJECT"
    )

    project = project_service.create(
        owner_id=authenticated_user.id,
        name="ecommerce",
        description=(
            "E-commerce cloud platform"
        ),
    )

    print(
        f"Project: {project.name}"
    )

    print(
        f"Description: "
        f"{project.description}"
    )

    audit_service.record(
        actor_id=authenticated_user.id,
        action="CREATE_PROJECT",
    )

    # ==========================================================
    # 7. COMPUTE
    # ==========================================================

    print_section(
        "6. CREATE COMPUTE RESOURCE"
    )

    compute = (
        LocalComputeProvider()
    )

    compute_resource_id = (
        compute.create(
            "api-server"
        )
    )

    print(
        f"Compute resource: "
        f"{compute_resource_id}"
    )

    # ==========================================================
    # 8. APPLICATION RESOURCE
    # ==========================================================

    resource = resource_service.create(
        project_id=project.id,
        name="api-server",
        resource_type="compute",
    )

    resource_service.update_status(
        resource.id,
        "running",
    )

    print(
        f"Application resource: "
        f"{resource.id}"
    )

    print(
        f"Resource status: "
        f"{resource.status}"
    )

    audit_service.record(
        actor_id=authenticated_user.id,
        action="CREATE_RESOURCE",
        resource_id=resource.id,
    )

    # ==========================================================
    # 9. STORAGE
    # ==========================================================

    print_section(
        "7. OBJECT STORAGE"
    )

    storage = (
        LocalStorageProvider()
    )

    storage.put(
        key="config.json",
        data=(
            b'{"environment": "local"}'
        ),
    )

    stored_object = storage.get(
        "config.json"
    )

    print(
        f"Stored object: "
        f"{stored_object.decode()}"
    )

    # ==========================================================
    # 10. QUEUE
    # ==========================================================

    print_section(
        "8. MESSAGE QUEUE"
    )

    queue = LocalQueue()

    queue.send(
        {
            "resource_id": resource.id,
            "cpu_usage": 92.5,
            "memory_usage": 81.0,
        }
    )

    print(
        "Metric event sent to queue"
    )

    # ==========================================================
    # 11. WORKER
    # ==========================================================

    print_section(
        "9. BACKGROUND WORKER"
    )

    worker = MetricsWorker(
        queue=queue,
        monitoring_service=(
            monitoring_service
        ),
    )

    metric = worker.process_once()

    print(
        f"Resource: "
        f"{metric.resource_id}"
    )

    print(
        f"CPU usage: "
        f"{metric.cpu_usage}%"
    )

    print(
        f"Memory usage: "
        f"{metric.memory_usage}%"
    )

    # ==========================================================
    # 12. MONITORING
    # ==========================================================

    print_section(
        "10. MONITORING"
    )

    metrics = (
        monitoring_service.get_metrics(
            resource.id
        )
    )

    print(
        f"Metrics collected: "
        f"{len(metrics)}"
    )

    for item in metrics:

        print(
            f"CPU={item.cpu_usage}% "
            f"Memory={item.memory_usage}%"
        )

    # ==========================================================
    # 13. ALERT
    # ==========================================================

    print_section(
        "11. ALERT"
    )

    alert = alert_service.create(
        resource_id=resource.id,
        metric="cpu",
        threshold=80,
    )

    print(
        f"Alert threshold: "
        f"{alert.threshold}%"
    )

    alert_service.evaluate(
        alert,
        metric.cpu_usage,
    )

    print(
        f"Current CPU: "
        f"{metric.cpu_usage}%"
    )

    print(
        f"Alert triggered: "
        f"{alert.triggered}"
    )

    if alert.triggered:

        audit_service.record(
            actor_id=authenticated_user.id,
            action="CPU_ALERT_TRIGGERED",
            resource_id=resource.id,
        )

    # ==========================================================
    # 14. AUDIT
    # ==========================================================

    print_section(
        "12. AUDIT LOG"
    )

    events = (
        audit_service.list_events()
    )

    for event in events:

        print(
            f"{event['timestamp']} | "
            f"{event['action']} | "
            f"resource="
            f"{event['resource_id']}"
        )

    # ==========================================================
    # 15. FINAL ARCHITECTURE SUMMARY
    # ==========================================================

    print_section(
        "13. FINAL ARCHITECTURE"
    )

    print(
        """
Client
  |
  v
API
  |
  +--------------------+
  |                    |
  v                    v
Services          Infrastructure
  |                    |
  |              +-----+-----+------+
  |              |           |      |
  v              v           v      v
Repositories   Network    Compute  Storage
  |                         |
  v                         v
Database                   Queue
                             |
                             v
                           Worker
                             |
                             v
                        Monitoring
                             |
                             v
                           Alert
        """
    )

    print(
        "Chapter 17 demo completed."
    )


if __name__ == "__main__":

    main()