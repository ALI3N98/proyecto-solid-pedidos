"""Repositorio SQLite: concentra las operaciones de persistencia."""

import sqlite3

from .database import ConexionDB
from .domain import Pedido


class SQLitePedidoRepository:
    """Guarda pedidos y sus productos en SQLite."""

    def __init__(self, database: ConexionDB) -> None:
        self._database = database
        self._crear_tablas()

    def _crear_tablas(self) -> None:
        with self._database.conexion:
            self._database.conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS pedidos (
                    id TEXT PRIMARY KEY,
                    cliente TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    costo_envio REAL NOT NULL,
                    total REAL NOT NULL,
                    dias_entrega INTEGER NOT NULL,
                    fecha_creacion TEXT NOT NULL
                )
                """
            )
            self._database.conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS productos_pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido_id TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
                )
                """
            )

    def guardar(self, pedido: Pedido) -> None:
        with self._database.conexion:
            self._database.conexion.execute(
                """
                INSERT INTO pedidos
                (id, cliente, tipo, subtotal, costo_envio, total, dias_entrega, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pedido.id,
                    pedido.cliente,
                    pedido.tipo,
                    pedido.calcular_subtotal(),
                    pedido.costo_envio,
                    pedido.calcular_total(),
                    pedido.dias_entrega,
                    pedido.fecha_creacion,
                ),
            )
            self._database.conexion.executemany(
                """
                INSERT INTO productos_pedido (pedido_id, nombre, precio)
                VALUES (?, ?, ?)
                """,
                [(pedido.id, producto.nombre, producto.precio) for producto in pedido.productos],
            )

    def listar(self) -> list[dict]:
        filas = self._database.conexion.execute(
            "SELECT * FROM pedidos ORDER BY fecha_creacion DESC"
        ).fetchall()
        return [dict(fila) for fila in filas]
