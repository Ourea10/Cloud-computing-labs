from .models import (
    CloudProvider,
    FederatedResource,
    ProviderStatus,
)

from .exceptions import (
    ProviderUnavailableError,
)


class FederationManager:

    def __init__(self):

        self.providers: dict[
            str,
            CloudProvider,
        ] = {}

        self.resources: list[
            FederatedResource
        ] = []

    def register_provider(
        self,
        provider: CloudProvider,
    ):

        self.providers[
            provider.provider_id
        ] = provider

    def add_resource(
        self,
        resource: FederatedResource,
    ):

        provider = self.providers[
            resource.provider_id
        ]

        if (
            provider.status
            != ProviderStatus.AVAILABLE
        ):

            raise ProviderUnavailableError(
                f"Provider "
                f"{provider.name} "
                f"is unavailable"
            )

        self.resources.append(
            resource
        )

    def find_resources(
        self,
        resource_type,
    ):

        return [
            resource
            for resource
            in self.resources
            if resource.resource_type
            == resource_type
        ]