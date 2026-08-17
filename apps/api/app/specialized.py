from experiments.ch09_specialized_mechanisms.audit_monitor import (
    AuditMonitor,
)

from experiments.ch09_specialized_mechanisms.load_balancer import (
    LoadBalancer,
)

from experiments.ch09_specialized_mechanisms.pay_per_use import (
    PayPerUseMonitor,
)

from experiments.ch09_specialized_mechanisms.sla_monitor import (
    SLAMonitor,
)

from experiments.ch09_specialized_mechanisms.state_management import (
    StateManagementDatabase,
)


audit_monitor = AuditMonitor(
    log_file="cloud-audit.log"
)

load_balancer = LoadBalancer()

sla_monitor = SLAMonitor()

pay_per_use = PayPerUseMonitor()

state_database = StateManagementDatabase(
    "cloud_state.db"
)