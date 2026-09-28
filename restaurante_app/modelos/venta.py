class Venta:
    def __init__(self, id, usuario_id, usuario_nombre, producto_id, producto_nombre, precio, fecha):
        self.id = int(id)
        self.usuario_id = int(usuario_id)
        self.usuario_nombre = usuario_nombre.strip()
        self.producto_id = int(producto_id)
        self.producto_nombre = producto_nombre.strip()
        self.precio = float(precio)
        self.fecha = fecha

    def a_diccionario(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "usuario_nombre": self.usuario_nombre,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "precio": self.precio,
            "fecha": self.fecha,
        }
