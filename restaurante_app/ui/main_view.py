import tkinter as tk
from tkinter import messagebox, ttk

class MainView(ttk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, on_logout):
        super().__init__(master, padding=15)
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.usuario_venta_var = tk.StringVar()
        self.producto_venta_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Sistema listo.")
        self.tabla_productos = None
        self.tabla_ventas = None
        self._construir_interfaz()
        self._mostrar_inicio()

    def _construir_interfaz(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        encabezado = ttk.Frame(self, padding=(5, 5, 5, 10))
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(encabezado, text="Restaurante App - Semana 15", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(encabezado, text=f"Sesión: {self.usuario_actual.nombre} ({self.usuario_actual.rol})").grid(row=1, column=0, sticky="w")
        ttk.Button(encabezado, text="Cerrar sesión", command=self.on_logout).grid(row=0, column=1, rowspan=2)

        menu = ttk.LabelFrame(self, text="Navegación", padding=10)
        menu.grid(row=1, column=0, sticky="ns", padx=(0, 12))
        ttk.Button(menu, text="Inicio", width=20, command=self._mostrar_inicio).pack(fill="x", pady=4)
        ttk.Button(menu, text="Productos", width=20, command=self._mostrar_productos).pack(fill="x", pady=4)
        ttk.Button(menu, text="Usuarios", width=20, command=self._mostrar_usuarios).pack(fill="x", pady=4)
        ttk.Button(menu, text="Ventas", width=20, command=self._mostrar_ventas).pack(fill="x", pady=4)

        self.contenido = ttk.Frame(self, padding=5)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(0, weight=1)

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self):
        self._limpiar_contenido()
        panel = ttk.LabelFrame(self.contenido, text="Resumen del sistema", padding=25)
        panel.grid(row=0, column=0, sticky="nsew")
        ttk.Label(panel, text="Bienvenido al panel principal", font=("Arial", 17, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 15))
        resumen = (
            f"Productos registrados: {self.restaurante_servicio.cantidad_productos()}\n"
            f"Usuarios registrados: {self.restaurante_servicio.cantidad_usuarios()}\n"
            f"Ventas registradas: {self.restaurante_servicio.cantidad_ventas()}\n\n"
            "Semana 15 incorpora manejo de eventos mediante command= y callbacks."
        )
        ttk.Label(panel, text=resumen, justify="left", font=("Arial", 11)).grid(row=1, column=0, sticky="nw")

    def _mostrar_productos(self):
        self._limpiar_contenido()
        contenedor = ttk.Frame(self.contenido)
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)
        ttk.Label(contenedor, text="Gestión de productos", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))
        formulario = ttk.LabelFrame(contenedor, text="Datos del producto", padding=12)
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        for col in range(5):
            formulario.columnconfigure(col, weight=1)
        campos=[("ID",self.id_var),("Nombre",self.nombre_var),("Categoría",self.categoria_var),("Precio",self.precio_var),("Cantidad",self.cantidad_var)]
        for columna,(texto,variable) in enumerate(campos):
            ttk.Label(formulario,text=f"{texto}:").grid(row=0,column=columna,sticky="w",padx=4)
            ttk.Entry(formulario,textvariable=variable).grid(row=1,column=columna,sticky="ew",padx=4,pady=(3,8))
        acciones=ttk.Frame(formulario)
        acciones.grid(row=2,column=0,columnspan=5)
        ttk.Button(acciones,text="Registrar",command=self._registrar_producto).pack(side="left",padx=4)
        ttk.Button(acciones,text="Cargar / Consultar",command=self._cargar_producto).pack(side="left",padx=4)
        ttk.Button(acciones,text="Actualizar",command=self._actualizar_producto).pack(side="left",padx=4)
        ttk.Button(acciones,text="Eliminar",command=self._eliminar_producto).pack(side="left",padx=4)
        ttk.Button(acciones,text="Limpiar",command=self._limpiar_formulario).pack(side="left",padx=4)
        tabla_frame=ttk.LabelFrame(contenedor,text="Productos registrados",padding=8)
        tabla_frame.grid(row=2,column=0,sticky="nsew")
        tabla_frame.columnconfigure(0,weight=1)
        tabla_frame.rowconfigure(0,weight=1)
        columnas=("id","nombre","categoria","precio","cantidad")
        self.tabla_productos=ttk.Treeview(tabla_frame,columns=columnas,show="headings",height=12)
        for col,titulo in zip(columnas,["ID","Producto","Categoría","Precio","Cantidad"]):
            self.tabla_productos.heading(col,text=titulo)
            self.tabla_productos.column(col,anchor="center",width=140)
        self.tabla_productos.grid(row=0,column=0,sticky="nsew")
        self._actualizar_tabla_productos()

    def _mostrar_usuarios(self):
        self._limpiar_contenido()
        panel=ttk.LabelFrame(self.contenido,text="Consulta de usuarios",padding=10)
        panel.grid(row=0,column=0,sticky="nsew")
        panel.columnconfigure(0,weight=1)
        panel.rowconfigure(1,weight=1)
        ttk.Label(panel,text="Usuarios registrados",font=("Arial",16,"bold")).grid(row=0,column=0,sticky="w",pady=(0,10))
        columnas=("id","nombre","usuario","rol")
        tabla=ttk.Treeview(panel,columns=columnas,show="headings",height=14)
        for col,titulo in zip(columnas,["ID","Nombre","Usuario","Rol"]):
            tabla.heading(col,text=titulo)
            tabla.column(col,anchor="center",width=160)
        for usuario in self.restaurante_servicio.listar_usuarios():
            tabla.insert("",tk.END,values=(usuario.id,usuario.nombre,usuario.usuario,usuario.rol))
        tabla.grid(row=1,column=0,sticky="nsew")

    def _mostrar_ventas(self):
        self._limpiar_contenido()
        contenedor=ttk.Frame(self.contenido)
        contenedor.grid(row=0,column=0,sticky="nsew")
        contenedor.columnconfigure(0,weight=1)
        contenedor.rowconfigure(2,weight=1)
        ttk.Label(contenedor,text="Registro de ventas",font=("Arial",16,"bold")).grid(row=0,column=0,sticky="w",pady=(0,10))
        formulario=ttk.LabelFrame(contenedor,text="Nueva venta",padding=12)
        formulario.grid(row=1,column=0,sticky="ew",pady=(0,10))
        formulario.columnconfigure(1,weight=1)
        formulario.columnconfigure(3,weight=1)
        ttk.Label(formulario,text="Usuario:").grid(row=0,column=0,padx=5,pady=5)
        combo_usuarios=ttk.Combobox(formulario,textvariable=self.usuario_venta_var,state="readonly")
        combo_usuarios["values"]=[f"{u.id} - {u.nombre}" for u in self.restaurante_servicio.listar_usuarios()]
        combo_usuarios.grid(row=0,column=1,sticky="ew",padx=5,pady=5)
        ttk.Label(formulario,text="Producto:").grid(row=0,column=2,padx=5,pady=5)
        self.combo_productos=ttk.Combobox(formulario,textvariable=self.producto_venta_var,state="readonly")
        self.combo_productos["values"]=[f"{p.id} - {p.nombre} (${p.precio:.2f}) | Stock: {p.cantidad}" for p in self.restaurante_servicio.listar_productos()]
        self.combo_productos.grid(row=0,column=3,sticky="ew",padx=5,pady=5)
        ttk.Button(formulario,text="Registrar venta",command=self._registrar_venta).grid(row=1,column=0,columnspan=4,pady=(10,2))
        tabla_frame=ttk.LabelFrame(contenedor,text="Ventas registradas",padding=8)
        tabla_frame.grid(row=2,column=0,sticky="nsew")
        tabla_frame.columnconfigure(0,weight=1)
        tabla_frame.rowconfigure(0,weight=1)
        columnas=("id","usuario","producto","precio","fecha")
        self.tabla_ventas=ttk.Treeview(tabla_frame,columns=columnas,show="headings",height=13)
        for col,titulo in zip(columnas,["ID","Usuario","Producto","Precio","Fecha"]):
            self.tabla_ventas.heading(col,text=titulo)
            self.tabla_ventas.column(col,anchor="center",width=150)
        self.tabla_ventas.grid(row=0,column=0,sticky="nsew")
        self._actualizar_tabla_ventas()

    def _registrar_venta(self):
        try:
            if not self.usuario_venta_var.get() or not self.producto_venta_var.get():
                raise ValueError("Seleccione un usuario y un producto.")
            usuario_id=self.usuario_venta_var.get().split(" - ",1)[0]
            producto_id=self.producto_venta_var.get().split(" - ",1)[0]
            venta=self.restaurante_servicio.registrar_venta(usuario_id,producto_id)
            self.usuario_venta_var.set("")
            self.producto_venta_var.set("")
            self._actualizar_tabla_ventas()
            self.combo_productos["values"]=[f"{p.id} - {p.nombre} (${p.precio:.2f}) | Stock: {p.cantidad}" for p in self.restaurante_servicio.listar_productos()]
            messagebox.showinfo("Venta registrada",f"Venta #{venta.id} registrada correctamente.")
        except ValueError as error:
            messagebox.showwarning("Validación",str(error))

    def _registrar_producto(self):
        try:
            producto=self.restaurante_servicio.registrar_producto(self.id_var.get(),self.nombre_var.get(),self.categoria_var.get(),self.precio_var.get(),self.cantidad_var.get())
            self._actualizar_tabla_productos()
            self._limpiar_formulario()
            messagebox.showinfo("Producto",f"Producto '{producto.nombre}' registrado.")
        except ValueError as error:
            messagebox.showwarning("Validación",str(error))

    def _cargar_producto(self):
        producto=self.restaurante_servicio.buscar_producto(self.id_var.get())
        if producto is None:
            messagebox.showinfo("Consulta","No se encontró un producto con ese ID.")
            return
        self.id_var.set(str(producto.id))
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(f"{producto.precio:.2f}")
        self.cantidad_var.set(str(producto.cantidad))

    def _actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(self.id_var.get(),self.nombre_var.get(),self.categoria_var.get(),self.precio_var.get(),self.cantidad_var.get())
            self._actualizar_tabla_productos()
        except ValueError as error:
            messagebox.showwarning("Validación",str(error))

    def _eliminar_producto(self):
        producto=self.restaurante_servicio.buscar_producto(self.id_var.get())
        if producto is None:
            messagebox.showinfo("Eliminar","No se encontró un producto con ese ID.")
            return
        if messagebox.askyesno("Confirmar",f"¿Eliminar '{producto.nombre}'?"):
            self.restaurante_servicio.eliminar_producto(self.id_var.get())
            self._actualizar_tabla_productos()
            self._limpiar_formulario()

    def _actualizar_tabla_productos(self):
        if self.tabla_productos is None: return
        for item in self.tabla_productos.get_children(): self.tabla_productos.delete(item)
        for p in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert("",tk.END,values=(p.id,p.nombre,p.categoria,f"${p.precio:.2f}",p.cantidad))

    def _actualizar_tabla_ventas(self):
        if self.tabla_ventas is None: return
        for item in self.tabla_ventas.get_children(): self.tabla_ventas.delete(item)
        for v in self.restaurante_servicio.listar_ventas():
            self.tabla_ventas.insert("",tk.END,values=(v.id,v.usuario_nombre,v.producto_nombre,f"${v.precio:.2f}",v.fecha))

    def _limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")
