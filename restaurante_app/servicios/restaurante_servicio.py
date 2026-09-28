from datetime import datetime
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class RestauranteServicio:
    def __init__(self, archivo_servicio, ruta_usuarios, ruta_productos, ruta_ventas):
        self.archivo_servicio = archivo_servicio
        self.ruta_usuarios = ruta_usuarios
        self.ruta_productos = ruta_productos
        self.ruta_ventas = ruta_ventas
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.recargar_datos()

    def recargar_datos(self):
        self.usuarios = [Usuario(**d) for d in self.archivo_servicio.leer_json(self.ruta_usuarios)]
        self.productos = [Producto(**d) for d in self.archivo_servicio.leer_json(self.ruta_productos)]
        self.ventas = [Venta(**d) for d in self.archivo_servicio.leer_json(self.ruta_ventas)]

    def validar_acceso(self, nombre_usuario, contrasena):
        nombre_usuario = nombre_usuario.strip()
        contrasena = contrasena.strip()
        if not nombre_usuario or not contrasena:
            return None
        return next((u for u in self.usuarios if u.usuario == nombre_usuario and u.contrasena == contrasena), None)

    def listar_usuarios(self): return list(self.usuarios)
    def listar_productos(self): return list(self.productos)
    def listar_ventas(self): return list(self.ventas)
    def cantidad_usuarios(self): return len(self.usuarios)
    def cantidad_productos(self): return len(self.productos)
    def cantidad_ventas(self): return len(self.ventas)

    def buscar_producto(self, id_producto):
        try: id_producto = int(str(id_producto).strip())
        except ValueError: return None
        return next((p for p in self.productos if p.id == id_producto), None)

    def buscar_usuario(self, id_usuario):
        try: id_usuario = int(str(id_usuario).strip())
        except ValueError: return None
        return next((u for u in self.usuarios if u.id == id_usuario), None)

    def registrar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        datos = self._validar_producto(id_producto, nombre, categoria, precio, cantidad)
        if self.buscar_producto(datos["id"]) is not None:
            raise ValueError("Ya existe un producto con ese ID.")
        producto = Producto(**datos)
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        datos = self._validar_producto(id_producto, nombre, categoria, precio, cantidad)
        producto = self.buscar_producto(datos["id"])
        if producto is None:
            raise ValueError("No existe un producto con ese ID.")
        producto.nombre = datos["nombre"]
        producto.categoria = datos["categoria"]
        producto.precio = datos["precio"]
        producto.cantidad = datos["cantidad"]
        self._guardar_productos()
        return producto

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("No existe un producto con ese ID.")
        self.productos.remove(producto)
        self._guardar_productos()
        return producto

    def registrar_venta(self, usuario_id, producto_id):
        usuario = self.buscar_usuario(usuario_id)
        producto = self.buscar_producto(producto_id)
        if usuario is None:
            raise ValueError("Seleccione un usuario válido.")
        if producto is None:
            raise ValueError("Seleccione un producto válido.")
        if producto.cantidad <= 0:
            raise ValueError("El producto seleccionado no tiene stock disponible.")

        nuevo_id = max((v.id for v in self.ventas), default=0) + 1
        venta = Venta(
            id=nuevo_id,
            usuario_id=usuario.id,
            usuario_nombre=usuario.nombre,
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            precio=producto.precio,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        producto.cantidad -= 1
        self.ventas.append(venta)
        self._guardar_ventas()
        self._guardar_productos()
        return venta

    def _validar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        nombre = nombre.strip()
        categoria = categoria.strip()
        if not nombre or not categoria:
            raise ValueError("Nombre y categoría son obligatorios.")
        try: id_num = int(str(id_producto).strip())
        except ValueError as error: raise ValueError("El ID debe ser un número entero.") from error
        try: precio_num = float(str(precio).strip().replace(",", "."))
        except ValueError as error: raise ValueError("El precio debe ser un número válido.") from error
        try: cantidad_num = int(str(cantidad).strip())
        except ValueError as error: raise ValueError("La cantidad debe ser un número entero.") from error
        if id_num <= 0: raise ValueError("El ID debe ser mayor que cero.")
        if precio_num < 0: raise ValueError("El precio no puede ser negativo.")
        if cantidad_num < 0: raise ValueError("La cantidad no puede ser negativa.")
        return {"id": id_num, "nombre": nombre, "categoria": categoria, "precio": precio_num, "cantidad": cantidad_num}

    def _guardar_productos(self):
        self.archivo_servicio.escribir_json(self.ruta_productos, [p.a_diccionario() for p in self.productos])

    def _guardar_ventas(self):
        self.archivo_servicio.escribir_json(self.ruta_ventas, [v.a_diccionario() for v in self.ventas])
