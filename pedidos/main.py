"""Punto de entrada: ejecuta una demostración del sistema."""

from .database import ConexionDB
from .domain import Producto
from .events import Evento, UsuarioSuscrito
from .factory import PedidoFactory
from .repository import SQLitePedidoRepository
from .service import PedidoService


def main() -> None:
    # Singleton: ambas partes del sistema pueden obtener la misma conexión.
    conexion = ConexionDB()
    repositorio = SQLitePedidoRepository(conexion)

    # Observer: los usuarios suscritos reciben el aviso del nuevo pedido.
    evento = Evento()
    evento.suscribir(UsuarioSuscrito("Ana López", "ana@ejemplo.com"))
    evento.suscribir(UsuarioSuscrito("Carlos Ruiz", "carlos@ejemplo.com"))

    # Factory: el servicio solicita un pedido sin instanciar clases concretas.
    fabrica = PedidoFactory()
    servicio = PedidoService(fabrica, repositorio, evento)

    productos = [
        Producto("Teclado mecánico", 850.00),
        Producto("Mouse inalámbrico", 420.00),
    ]
    pedido = servicio.crear_pedido("urgente", "María García", productos)

    print("\n--- RESUMEN DEL PEDIDO ---")
    print(f"Folio: {pedido.id}")
    print(f"Cliente: {pedido.cliente}")
    print(f"Tipo: {pedido.tipo}")
    print(f"Productos: {', '.join(p.nombre for p in pedido.productos)}")
    print(f"Subtotal: ${pedido.calcular_subtotal():.2f}")
    print(f"Envío: ${pedido.costo_envio:.2f}")
    print(f"Total: ${pedido.calcular_total():.2f}")
    print(f"Entrega estimada: {pedido.dias_entrega} día(s)")
    print(f"\nPedidos guardados en: {conexion.ruta.resolve()}")


if __name__ == "__main__":
    main()
