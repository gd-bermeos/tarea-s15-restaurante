class Usuario:
    def __init__(self, id, nombre, usuario, contrasena, rol):
        self.id = int(id)
        self.nombre = nombre.strip()
        self.usuario = usuario.strip()
        self.contrasena = contrasena
        self.rol = rol.strip()

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    def __str__(self):
        return f"{self.nombre} | Usuario: {self.usuario} | Rol: {self.rol}"
