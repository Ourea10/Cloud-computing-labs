class MetaCloud:

    def __init__(self):

        self.providers = {}

    def register_provider(
        self,
        provider_id: str,
        provider,
    ):

        self.providers[
            provider_id
        ] = provider

    def get_provider(
        self,
        provider_id: str,
    ):

        return self.providers[
            provider_id
        ]

    def list_providers(self):

        return list(
            self.providers.keys()
        )

    def execute(
        self,
        provider_id: str,
        operation,
        *args,
        **kwargs,
    ):

        provider = self.get_provider(
            provider_id
        )

        return operation(
            provider,
            *args,
            **kwargs,
        )