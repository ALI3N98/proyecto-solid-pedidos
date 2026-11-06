"""Pruebas unitarias de los patrones y del flujo de creación de pedidos."""

import tempfile
import unittest
from pathlib import Path

from pedidos.database import ConexionDB
from pedidos.domain import Pedido, PedidoNormal, PedidoUrgente, Producto
from pedidos.events import Evento
from pedidos.factory import PedidoFactory
from pedidos.service import PedidoService
from pedidos.repository import SQLitePedidoRepository


class ObservadorDePrueba:
    def __init__(self) -> None:
        self.pedidos_recibidos = []

    def actualizar(self, pedido: Pedido) -> None:
        self.pedidos_recibidos.append(pedido)


class RepositorioDePrueba:
    def __init__(self) -> None:
        self.pedidos_guardados = []

    def guardar(self, pedido: Pedido) -> None:
        self.pedidos_guardados.append(pedido)


class PedidoProgramado(Pedido):
    """Ejemplo de extensión registrada sin cambiar el método crear()."""

    @property
    def tipo(self) -> str:
        return "programado"

    @property
    def costo_envio(self) -> float:
        return 30.0

    @property
    def dias_entrega(self) -> int:
        return 7


class TestPedidoFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = PedidoFactory()
        self.productos = [Producto("Libro", 200)]

    def test_crea_pedido_normal_y_urgente(self) -> None:
        normal = self.factory.crear("normal", "Luis", self.productos)
        urgente = self.factory.crear("urgente", "Luis", self.productos)

        self.assertIsInstance(normal, PedidoNormal)
        self.assertIsInstance(urgente, PedidoUrgente)
        self.assertEqual(normal.dias_entrega, 5)
        self.assertEqual(urgente.dias_entrega, 1)

    def test_permite_registrar_un_nuevo_tipo(self) -> None:
        self.factory.registrar_tipo("programado", PedidoProgramado)
        pedido = self.factory.crear("programado", "Luis", self.productos)
        self.assertIsInstance(pedido, PedidoProgramado)

    def test_rechaza_un_tipo_desconocido(self) -> None:
        with self.assertRaises(ValueError):
            self.factory.crear("economico", "Luis", self.productos)


class TestObserverYServicio(unittest.TestCase):
    def test_evento_notifica_a_usuarios_suscritos(self) -> None:
        evento = Evento()
        observador = ObservadorDePrueba()
        evento.suscribir(observador)
        pedido = PedidoNormal("Luis", [Producto("Libro", 200)])

        evento.notificar(pedido)

        self.assertEqual(observador.pedidos_recibidos, [pedido])
        self.assertEqual(len(evento.usuarios_suscritos), 1)

    def test_cancelar_suscripcion_evitar_notificacion(self) -> None:
        evento = Evento()
        observador = ObservadorDePrueba()
        evento.suscribir(observador)
        evento.cancelar_suscripcion(observador)
        evento.notificar(PedidoNormal("Luis", [Producto("Libro", 200)]))

        self.assertEqual(observador.pedidos_recibidos, [])

    def test_servicio_guarda_y_notifica_el_pedido(self) -> None:
        repositorio = RepositorioDePrueba()
        evento = Evento()
        observador = ObservadorDePrueba()
        evento.suscribir(observador)
        servicio = PedidoService(PedidoFactory(), repositorio, evento)

        pedido = servicio.crear_pedido(
            "urgente", "Luis", [Producto("Libro", 200)]
        )

        self.assertEqual(repositorio.pedidos_guardados, [pedido])
        self.assertEqual(observador.pedidos_recibidos, [pedido])


class TestSingleton(unittest.TestCase):
    def test_dos_construcciones_comparten_la_misma_instancia(self) -> None:
        with tempfile.TemporaryDirectory() as carpeta:
            ruta_1 = Path(carpeta) / "primera.db"
            ruta_2 = Path(carpeta) / "segunda.db"
            db_1 = ConexionDB(ruta_1)
            db_2 = ConexionDB(ruta_2)

            self.assertIs(db_1, db_2)
            self.assertEqual(db_1.ruta, ruta_1)

            repositorio = SQLitePedidoRepository(db_1)
            pedido = PedidoNormal("Luis", [Producto("Libro", 200)])
            repositorio.guardar(pedido)
            pedidos_guardados = repositorio.listar()

            self.assertEqual(len(pedidos_guardados), 1)
            self.assertEqual(pedidos_guardados[0]["id"], pedido.id)
            self.assertEqual(pedidos_guardados[0]["total"], 250.0)
            db_1.cerrar()


if __name__ == "__main__":
    unittest.main()
