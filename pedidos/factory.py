"""Implementación del patrón Factory para crear pedidos."""

from collections.abc import Callable

from .domain import Pedido, PedidoNormal, PedidoUrgente, Producto

CreadorPedido = Callable[[str, list[Producto]], Pedido]


class PedidoFactory:
    """Crea pedidos sin que el servicio conozca sus clases concretas.

    Se pueden registrar nuevos tipos mediante registrar_tipo(), sin modificar
    el método crear().
    """

    def __init__(self) -> None:
        self._creadores: dict[str, CreadorPedido] = {}
        self.registrar_tipo("normal", PedidoNormal)
        self.registrar_tipo("urgente", PedidoUrgente)

    def registrar_tipo(self, tipo: str, creador: CreadorPedido) -> None:
        if not tipo or not tipo.strip():
            raise ValueError("El tipo de pedido debe tener un nombre.")
        self._creadores[tipo.strip().lower()] = creador

    def crear(self, tipo: str, cliente: str, productos: list[Producto]) -> Pedido:
        clave = tipo.strip().lower()
        creador = self._creadores.get(clave)
        if creador is None:
            tipos = ", ".join(sorted(self._creadores))
            raise ValueError(f"Tipo de pedido '{tipo}' no válido. Tipos disponibles: {tipos}.")
        return creador(cliente, productos)
