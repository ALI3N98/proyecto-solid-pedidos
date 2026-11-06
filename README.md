# Sistema de gestión de pedidos – Patrones de diseño y SOLID

## 1. Descripción

Este proyecto implementa un ejemplo sencillo de gestión de pedidos para una tienda en línea. Permite crear pedidos normales y urgentes, calcular sus importes, guardar la información en una base de datos SQLite y notificar a los usuarios suscritos cuando se registra un pedido.

Se desarrolló en **Python 3.10 o superior** y utiliza únicamente la biblioteca estándar; no requiere instalar paquetes externos.

## 2. Requisitos

- Python 3.10 o superior.
- Terminal o consola.

Comprueba la versión instalada con:

macOS:
```bash
python3.13 --version
python3 --version
py --version
```

## 3. Estructura del proyecto

```text
proyecto_solid_pedidos/
├── pedidos/
│   ├── __init__.py
│   ├── database.py
│   ├── domain.py
│   ├── events.py
│   ├── factory.py
│   ├── interfaces.py
│   ├── main.py
│   ├── repository.py
│   └── service.py
├── tests/
│   └── test_pedidos.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 4. Cómo ejecutar el sistema

1. Descarga o clona el repositorio.
2. Abre una terminal dentro de la carpeta `proyecto_solid_pedidos`.
3. Ejecuta:

macOS:
```bash
python3.13 -m pedidos.main
python3 -m pedidos.main
py -3 -m pedidos.main
```

El programa crea un pedido urgente de ejemplo, lo guarda en el archivo `pedidos.db` y muestra las notificaciones en la consola. La notificación simula el aviso al usuario; no envía correos electrónicos reales.

Para utilizar otra ruta para la base de datos, define la variable de entorno `PEDIDOS_DB_PATH` **antes de ejecutar el programa**.

macOS o Linux:

```bash
PEDIDOS_DB_PATH="datos/pedidos.db" python -m pedidos.main
```

Windows PowerShell:

```powershell
$env:PEDIDOS_DB_PATH="datos/pedidos.db"
python -m pedidos.main
```

## 5. Patrones de diseño implementados

### Factory – `PedidoFactory`

La clase `PedidoFactory` centraliza la creación de pedidos. Actualmente registra `PedidoNormal` y `PedidoUrgente`, por lo que el servicio no necesita conocer ni instanciar directamente esas clases.

También cuenta con `registrar_tipo()`, que permite incorporar nuevos tipos de pedido registrando una clase creadora compatible. Esto evita modificar el método `crear()` cada vez que se agrega una variante.

### Singleton – `ConexionDB`

La clase `ConexionDB` controla su creación mediante `__new__` y un bloqueo (`Lock`). De esta forma, las distintas partes del sistema que solicitan la conexión reciben la misma instancia y comparten una conexión SQLite. La primera construcción determina la ruta de la base de datos durante ese proceso.

### Observer – `Evento`

La clase `Evento` mantiene una lista de usuarios suscritos y ofrece los métodos `suscribir()`, `cancelar_suscripcion()` y `notificar()`. Cuando `PedidoService` registra un pedido, publica el evento y cada usuario suscrito recibe la notificación mediante `actualizar()`.

En esta versión, `UsuarioSuscrito` muestra el aviso en consola. El diseño permite agregar otros observadores, por ejemplo, uno que utilice un proveedor de correo electrónico.

## 6. Aplicación de los principios SOLID

- **SRP – Responsabilidad única:** `Pedido` y sus variantes representan las reglas del pedido; `PedidoFactory` crea objetos; `SQLitePedidoRepository` guarda datos; `Evento` administra suscripciones y notificaciones; y `PedidoService` coordina el caso de uso. Cada clase tiene una responsabilidad delimitada.
- **OCP – Abierto/cerrado:** se pueden registrar nuevos tipos de pedido con `PedidoFactory.registrar_tipo()` sin cambiar su método `crear()`. También pueden agregarse observadores nuevos sin modificar `Evento`, siempre que implementen `actualizar()`.
- **LSP – Sustitución de Liskov:** `PedidoNormal` y `PedidoUrgente` respetan el contrato de `Pedido`: ambos ofrecen tipo, costo de envío, días de entrega y cálculo de totales. Por eso, el servicio y el repositorio pueden trabajar con cualquiera de ellos sin condiciones especiales.
- **ISP – Segregación de interfaces:** `interfaces.py` define protocolos pequeños y enfocados: `FabricaPedidos`, `RepositorioPedidos`, `PublicadorPedidos` y `ObservadorPedido`. Cada componente depende únicamente de las operaciones que necesita.
- **DIP – Inversión de dependencias:** `PedidoService` recibe una fábrica, un repositorio y un publicador definidos mediante protocolos. No crea por su cuenta la conexión SQLite ni depende directamente de `SQLitePedidoRepository`; las implementaciones se proporcionan desde `main.py`.

## 7. Persistencia de datos

SQLite almacena los pedidos en la tabla `pedidos` y sus productos en `productos_pedido`. El repositorio utiliza operaciones parametrizadas para guardar la información y mantiene ambas inserciones dentro de una transacción.

## 8. Ejecutar las pruebas

Desde la carpeta raíz del proyecto, ejecuta:

macOS:
```bash
python3.13 -m unittest discover -s tests -v
python3 -m unittest discover -s tests -v
py -3 -m unittest discover -s tests -v
```

Las pruebas verifican la creación de pedidos normales y urgentes, el registro de un nuevo tipo, el comportamiento de las suscripciones, el flujo del servicio y la identidad compartida de la conexión Singleton.

## 9. Posibles mejoras futuras

- Enviar notificaciones reales por correo electrónico o SMS.
- Agregar más tipos de pedido y reglas de envío.
- Incorporar una interfaz gráfica o una API web.
- Añadir autenticación y administración de usuarios.
- Incorporar validaciones, reportes y consultas de pedidos.

## 10. Conclusión

El proyecto demuestra que los patrones de diseño y los principios SOLID pueden trabajar en conjunto. Factory organiza la creación de pedidos, Singleton administra una conexión compartida y Observer desacopla las notificaciones. A su vez, SOLID ayuda a separar responsabilidades y facilita que el sistema pueda extenderse y mantenerse sin afectar innecesariamente sus componentes.


## 11. Subir el proyecto a GitHub

Desde la terminal, dentro de la carpeta del proyecto, ejecuta estos comandos:

```bash
git init
git add .
git commit -m "Proyecto final: patrones de diseño y SOLID"
git branch -M main
```

Después crea un repositorio vacío en GitHub. Copia la dirección HTTPS del repositorio y ejecuta (reemplazando la dirección de ejemplo):

```bash
git remote add origin https://github.com/USUARIO/proyecto-solid-pedidos.git
git push -u origin main
```

Al finalizar, comparte el enlace del repositorio como entrega. No incluyas archivos de base de datos (`*.db`); están excluidos mediante `.gitignore`.
