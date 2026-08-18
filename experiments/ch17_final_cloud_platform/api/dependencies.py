from ..repositories.user_repository import (
    UserRepository,
)

from ..repositories.project_repository import (
    ProjectRepository,
)

from ..repositories.resource_repository import (
    ResourceRepository,
)

from ..repositories.metric_repository import (
    MetricRepository,
)

from ..repositories.alert_repository import (
    AlertRepository,
)


user_repository = UserRepository()

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