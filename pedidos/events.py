"""Implementación del patrón Observer para notificar nuevos pedidos."""

from .domain import Pedido
from .interfaces import ObservadorPedido


class Evento:
    """Mantiene usuarios suscritos y les notifica cuando se crea un pedido."""

    def __init__(self) -> None:
        self._usuarios_suscritos: list[ObservadorPedido] = []

    @property
    def usuarios_suscritos(self) -> tuple[ObservadorPedido, ...]:
        return tuple(self._usuarios_suscritos)

    def suscribir(self, usuario: ObservadorPedido) -> None:
        if usuario not in self._usuarios_suscritos:
            self._usuarios_suscritos.append(usuario)

    def cancelar_suscripcion(self, usuario: ObservadorPedido) -> None:
        if usuario in self._usuarios_suscritos:
            self._usuarios_suscritos.remove(usuario)

    def notificar(self, pedido: Pedido) -> None:
        for usuario in tuple(self._usuarios_suscritos):
            usuario.actualizar(pedido)


class UsuarioSuscrito:
    """Usuario registrado como observador; muestra la notificación en consola."""

    def __init__(self, nombre: str, correo: str) -> None:
        if not nombre.strip() or not correo.strip():
            raise ValueError("El usuario debe tener nombre y correo.")
        self.nombre = nombre.strip()
        self.correo = correo.strip()

    def actualizar(self, pedido: Pedido) -> None:
        print(
            f"[Notificación para {self.nombre} <{self.correo}>] "
            f"Se registró un pedido {pedido.tipo} para {pedido.cliente}. "
            f"Folio: {pedido.id[:8]}"
        )
