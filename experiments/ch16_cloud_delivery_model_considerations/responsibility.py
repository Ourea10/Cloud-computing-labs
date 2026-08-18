from .enums import (
    DeliveryModel,
    Layer,
    Responsibility,
)

from .models import (
    DeliveryModelDefinition,
    LayerResponsibility,
)


class ResponsibilityManager:

    def __init__(self):

        self.models = {}

        self._initialize_models()

    def _initialize_models(self):

        iaas = DeliveryModelDefinition(
            model=DeliveryModel.IAAS,
            name="Infrastructure as a Service",
            description=(
                "Customer manages operating "
                "system and applications while "
                "provider manages infrastructure."
            ),
        )

        paas = DeliveryModelDefinition(
            model=DeliveryModel.PAAS,
            name="Platform as a Service",
            description=(
                "Provider manages infrastructure "
                "and platform while customer "
                "focuses on applications and data."
            ),
        )

        saas = DeliveryModelDefinition(
            model=DeliveryModel.SAAS,
            name="Software as a Service",
            description=(
                "Provider delivers a complete "
                "application service."
            ),
        )

        self.models[
            DeliveryModel.IAAS
        ] = iaas

        self.models[
            DeliveryModel.PAAS
        ] = paas

        self.models[
            DeliveryModel.SAAS
        ] = saas

        self._configure_iaas()
        self._configure_paas()
        self._configure_saas()

    def _configure_iaas(self):

        model = self.models[
            DeliveryModel.IAAS
        ]

        provider_layers = {
            Layer.FACILITY,
            Layer.NETWORK,
            Layer.STORAGE,
            Layer.COMPUTE,
        }

        self._configure(
            model,
            provider_layers,
        )

    def _configure_paas(self):

        model = self.models[
            DeliveryModel.PAAS
        ]

        provider_layers = {
            Layer.FACILITY,
            Layer.NETWORK,
            Layer.STORAGE,
            Layer.COMPUTE,
            Layer.OPERATING_SYSTEM,
            Layer.RUNTIME,
            Layer.DATABASE,
        }

        self._configure(
            model,
            provider_layers,
        )

    def _configure_saas(self):

        model = self.models[
            DeliveryModel.SAAS
        ]

        provider_layers = set(Layer)

        provider_layers.remove(
            Layer.DATA
        )

        provider_layers.remove(
            Layer.IDENTITY
        )

        self._configure(
            model,
            provider_layers,
        )

    def _configure(
        self,
        model,
        provider_layers,
    ):

        for layer in Layer:

            if layer in provider_layers:

                responsibility = (
                    Responsibility.PROVIDER
                )

            else:

                responsibility = (
                    Responsibility.CUSTOMER
                )

            model.responsibilities.append(
                LayerResponsibility(
                    layer=layer,
                    responsibility=responsibility,
                )
            )

    def get_model(
        self,
        model: DeliveryModel,
    ):

        return self.models[model]

    def get_responsibility(
        self,
        model: DeliveryModel,
        layer: Layer,
    ):

        definition = self.get_model(
            model
        )

        for item in (
            definition.responsibilities
        ):

            if item.layer == layer:

                return item.responsibility

        raise ValueError(
            f"No responsibility defined "
            f"for {layer}"
        )

    def matrix(
        self,
        model: DeliveryModel,
    ):

        definition = self.get_model(
            model
        )

        return {
            item.layer.value:
                item.responsibility.value
            for item
            in definition.responsibilities
        }