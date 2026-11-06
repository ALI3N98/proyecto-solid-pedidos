"""Conexión SQLite compartida mediante el patrón Singleton."""

import os
import sqlite3
from pathlib import Path
from threading import Lock


class ConexionDB:
    """Garantiza una sola instancia de conexión por proceso.

    La primera construcción determina la ruta de la base de datos. Las
    construcciones posteriores devuelven la misma instancia y conexión.
    Puede definirse PEDIDOS_DB_PATH para cambiar la ruta predeterminada.
    """

    _instancia: "ConexionDB | None" = None
    _lock = Lock()

    def __new__(cls, ruta: str | Path | None = None) -> "ConexionDB":
        with cls._lock:
            if cls._instancia is None:
                cls._instancia = super().__new__(cls)
                cls._instancia._conexion = None
                cls._instancia._ruta = None
            return cls._instancia

    def __init__(self, ruta: str | Path | None = None) -> None:
        with self._lock:
            if self._conexion is not None:
                return

            ruta_elegida = ruta or os.getenv("PEDIDOS_DB_PATH", "pedidos.db")
            self._ruta = Path(ruta_elegida)
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            self._conexion = sqlite3.connect(str(self._ruta))
            self._conexion.row_factory = sqlite3.Row
            self._conexion.execute("PRAGMA foreign_keys = ON")

    @property
    def conexion(self) -> sqlite3.Connection:
        if self._conexion is None:
            raise RuntimeError("La conexión a la base de datos está cerrada.")
        return self._conexion

    @property
    def ruta(self) -> Path:
        if self._ruta is None:
            raise RuntimeError("La base de datos todavía no ha sido inicializada.")
        return self._ruta

    def cerrar(self) -> None:
        """Cierra la conexión actual (la instancia Singleton se conserva)."""
        with self._lock:
            if self._conexion is not None:
                self._conexion.close()
                self._conexion = None
