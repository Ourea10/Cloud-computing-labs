from dataclasses import dataclass


@dataclass(frozen=True)
class ImageLayer:
    layer_id: str
    size_mb: int


@dataclass
class ContainerImage:
    name: str
    tag: str
    layers: list[ImageLayer]

    @property
    def size_mb(self) -> int:
        return sum(
            layer.size_mb
            for layer in self.layers
        )

    @property
    def reference(self) -> str:
        return f"{self.name}:{self.tag}"