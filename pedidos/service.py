"""Caso de uso principal: registrar un pedido y publicar su evento."""

from .domain import Pedido, Producto
from .interfaces import FabricaPedidos, PublicadorPedidos, RepositorioPedidos


class PedidoService:
    """Coordina la creación, persistencia y notificación de pedidos.

    Depende de protocolos (abstracciones), no de implementaciones concretas.
    """

    def __init__(
        self,
        fabrica: FabricaPedidos,
        repositorio: RepositorioPedidos,
        publicador: PublicadorPedidos,
    ) -> None:
        self._fabrica = fabrica
        self._repositorio = repositorio
        self._publicador = publicador

    def crear_pedido(self, tipo: str, cliente: str, productos: list[Producto]) -> Pedido:
        pedido = self._fabrica.crear(tipo, cliente, productos)
        self._repositorio.guardar(pedido)
        self._publicador.notificar(pedido)
        return pedido
