# Restaurante App - Semana 15

## Descripción

Proyecto académico de Programación Orientada a Objetos correspondiente a la **Semana 15: Conceptos fundamentales de manejo de eventos**.

Esta versión continúa la evolución del proyecto `restaurante_app` de semanas anteriores. Se conserva el inicio de sesión, la consulta de usuarios y la gestión de productos, y se incorpora una nueva sección de **Ventas** que relaciona un usuario con un producto.

## Objetivo de la Semana 15

Evidenciar el flujo básico de manejo de eventos:

`acción del usuario → botón → command= → callback → RestauranteServicio → persistencia → respuesta visual`

El botón **Registrar venta** utiliza `command=self._registrar_venta`. El callback obtiene las selecciones de la interfaz y delega la validación y el registro a `RestauranteServicio`.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.svg
│   └── venta.svg
└── main.py
```

## Funcionalidades

- Inicio de sesión con usuarios registrados.
- Consulta de usuarios.
- Registro, consulta, actualización y eliminación de productos.
- Nueva sección de **Ventas**.
- Selección de usuario y producto mediante `ttk.Combobox`.
- Botón **Registrar venta** enlazado con `command=`.
- Callback de venta en la interfaz.
- Validación y reglas de negocio en `RestauranteServicio`.
- Persistencia de ventas en `ventas.json`.
- Actualización inmediata del `Treeview` de ventas.
- Descuento de una unidad de stock al registrar una venta.
- Carpeta `assets/` con logo e ícono visual.

## Persistencia

La interfaz no escribe directamente los archivos JSON. Toda la persistencia se delega a la capa de servicios mediante `ArchivoServicio` y `RestauranteServicio`.

- `usuarios.json`: usuarios y credenciales.
- `productos.json`: productos y stock.
- `ventas.json`: ventas registradas.

## Credenciales de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | Administrador |
| mesero | 1234 | Mesero |
| caja | caja123 | Cajero |

## Ejecución

1. Abrir una terminal en la carpeta del repositorio.
2. Entrar a la aplicación:

```bash
cd restaurante_app
```

3. Ejecutar:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

## Comprobación sugerida

1. Iniciar sesión con `admin / admin123`.
2. Abrir **Usuarios** y comprobar los registros.
3. Abrir **Productos** y comprobar la gestión existente.
4. Abrir **Ventas**.
5. Seleccionar un usuario y un producto.
6. Presionar **Registrar venta**.
7. Verificar que la venta aparezca en la tabla.
8. Revisar `datos/ventas.json`.
9. Cerrar y volver a abrir la aplicación para comprobar que la venta persiste.

## Semana 15

La mejora principal de esta semana es la integración de manejo de eventos mediante `command=` y callbacks, manteniendo la arquitectura modular y evitando concentrar la lógica de negocio en la interfaz.
