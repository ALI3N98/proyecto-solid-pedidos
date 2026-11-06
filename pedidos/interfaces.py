"""Abstracciones pequeñas para reducir el acoplamiento entre módulos."""

from typing import Protocol

from .domain import Pedido


class FabricaPedidos(Protocol):
    def crear(self, tipo: str, cliente: str, productos: list) -> Pedido:
        """Construye un pedido del tipo solicitado."""
        ...


class RepositorioPedidos(Protocol):
    def guardar(self, pedido: Pedido) -> None:
        """Persiste un pedido."""
        ...


class PublicadorPedidos(Protocol):
    def notificar(self, pedido: Pedido) -> None:
        """Publica el evento de creación de un pedido."""
        ...


class ObservadorPedido(Protocol):
    def actualizar(self, pedido: Pedido) -> None:
        """Recibe la notificación de un nuevo pedido."""
        ...
