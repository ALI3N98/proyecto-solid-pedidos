"""Entidades y reglas principales del dominio de pedidos."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4


class Producto:
    """Representa un producto que puede agregarse a un pedido."""

    def __init__(self, nombre: str, precio: float) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
        self.nombre = nombre.strip()
        self.precio = float(precio)


class Pedido(ABC):
    """Contrato común para todos los tipos de pedido."""

    def __init__(self, cliente: str, productos: list[Producto]) -> None:
        if not cliente or not cliente.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        if not productos:
            raise ValueError("El pedido debe contener al menos un producto.")

        self.id = str(uuid4())
        self.cliente = cliente.strip()
        self.productos = list(productos)
        self.fecha_creacion = datetime.now(timezone.utc).isoformat(timespec="seconds")

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Nombre identificador del tipo de pedido."""
        raise NotImplementedError

    @property
    @abstractmethod
    def costo_envio(self) -> float:
        """Costo de envío correspondiente al tipo de pedido."""
        raise NotImplementedError

    @property
    @abstractmethod
    def dias_entrega(self) -> int:
        """Tiempo estimado de entrega en días."""
        raise NotImplementedError

    def calcular_subtotal(self) -> float:
        return sum(producto.precio for producto in self.productos)

    def calcular_total(self) -> float:
        return self.calcular_subtotal() + self.costo_envio


class PedidoNormal(Pedido):
    """Pedido con envío estándar."""

    @property
    def tipo(self) -> str:
        return "normal"

    @property
    def costo_envio(self) -> float:
        return 50.0

    @property
    def dias_entrega(self) -> int:
        return 5


class PedidoUrgente(Pedido):
    """Pedido con prioridad de preparación y envío."""

    @property
    def tipo(self) -> str:
        return "urgente"

    @property
    def costo_envio(self) -> float:
        return 120.0

    @property
    def dias_entrega(self) -> int:
        return 1
