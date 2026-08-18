from dataclasses import dataclass


@dataclass
class Application:

    application_id: str
    name: str
    runtime: str
    replicas: int = 1


class PaaSProvider:

    def __init__(self):

        self.applications: dict[
            str,
            Application,
        ] = {}

    def deploy(
        self,
        application_id: str,
        name: str,
        runtime: str,
    ):

        application = Application(
            application_id=application_id,
            name=name,
            runtime=runtime,
        )

        self.applications[
            application_id
        ] = application

        return application

    def scale(
        self,
        application_id: str,
        replicas: int,
    ):

        if replicas < 1:

            raise ValueError(
                "Replicas must be >= 1"
            )

        application = (
            self.applications[
                application_id
            ]
        )

        application.replicas = replicas

        return application