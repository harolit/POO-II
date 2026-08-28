from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import os
from pathlib import Path
from PIL import Image, ImageTk

#RUTA DEL PROYECTO
BASE_DIR=Path(__file__).resolve().parent
RUTA_BBDD=BASE_DIR/"BaseUsuariosTMHM.db"
RUTA_ICONO=BASE_DIR/"interface_grafica.ico"
RUTA_IMAGEN_FONDO=BASE_DIR/"fondo_usuario.jpg"  # Cambia el nombre de la imagen según tu archivo

# ==========================================
# CONFIGURACIÓN DE LA VENTANA
# ==========================================

raiz = Tk()
raiz.title("Sistema de Gestión de Usuarios")
raiz.geometry("1150x750")
raiz.resizable(True, True)

#ICONO DE LA VENTANA
if RUTA_ICONO.exists():
    try:
        raiz.iconbitmap(str(RUTA_ICONO))
    except Exception as e:
        print("No se pudo cargar el icono: ",e)
else:
    print("Advertencia: no se encontro el icono:")
    print(RUTA_ICONO)

# ==========================================
# CREAR MENÚ
# ==========================================

# Crear la barra de menú principal
barra_menu = Menu(raiz)
raiz.config(menu=barra_menu)

# Crear el menú "BBDD"
menu_bbdd = Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="BBDD", menu=menu_bbdd)

# Función para conectar a la base de datos
def conectar_bbdd():
    try:
        conexion = sqlite3.connect(str(RUTA_BBDD))
        conexion.close()
        messagebox.showinfo(
            "Conexión",
            f"Conexión a la base de datos establecida correctamente.\n{RUTA_BBDD}"
        )
    except Exception as e:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar a la base de datos:\n{e}"
        )

# Función para salir
def salir_aplicacion():
    respuesta = messagebox.askyesno(
        "Salir",
        "¿Está seguro de que desea salir de la aplicación?"
    )
    if respuesta:
        raiz.destroy()

# Agregar opciones al menú BBDD
menu_bbdd.add_command(label="Conectar", command=conectar_bbdd)
menu_bbdd.add_separator()
menu_bbdd.add_command(label="Salir", command=salir_aplicacion)

# ==========================================
# VARIABLES
# ==========================================
# StringVar() es una variable especial de Tkinter que permite
# conectar una variable de Python con un componente de la interfaz gráfica

id_seleccionado = StringVar()

nombre = StringVar()
contraseña = StringVar()
apellido = StringVar()
direccion = StringVar()
ciudad = StringVar()
codigo_postal = StringVar()
correo = StringVar()
comentarios = StringVar()

genero = StringVar(value="Masculino")
estado = IntVar()

tipo_usuario = StringVar(value="Seleccione")

ruta_imagen = StringVar()
ruta_archivo = StringVar()

# ==========================================
# CONEXIÓN A BASE DE DATOS
# ==========================================

def conexion_bbdd():

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contraseña TEXT,
        apellido TEXT NOT NULL,
        direccion TEXT,
        ciudad TEXT,
        codigo_postal TEXT,
        correo TEXT,
        comentarios TEXT,
        genero TEXT,
        estado INTEGER,
        tipo_usuario TEXT,
        imagen TEXT,
        archivo TEXT
    )
    """)

    conexion.commit()
    conexion.close()


conexion_bbdd()

# ==========================================
# FUNCIÓN LIMPIAR
# ==========================================

def limpiar():

    id_seleccionado.set("")

    nombre.set("")
    contraseña.set("")
    apellido.set("")
    direccion.set("")
    ciudad.set("")
    codigo_postal.set("")
    correo.set("")
    comentarios.set("")

    genero.set("Masculino")
    estado.set(0)

    tipo_usuario.set("Seleccione")

    ruta_imagen.set("")
    ruta_archivo.set("")

    etiqueta_imagen.config(image="")
    etiqueta_imagen.image = None

# ==========================================
# ADJUNTAR IMAGEN
# ==========================================

def seleccionar_imagen():

    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.gif"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo:

        ruta_imagen.set(archivo)

        try:

            imagen = Image.open(archivo)

            imagen.thumbnail((150, 150))

            imagen_tk = ImageTk.PhotoImage(imagen)

            etiqueta_imagen.config(image=imagen_tk)

            etiqueta_imagen.image = imagen_tk

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo cargar la imagen:\n{error}"
            )

# ==========================================
# ADJUNTAR ARCHIVO
# ==========================================

def seleccionar_archivo():

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[
            ("Documentos", "*.pdf *.docx *.xlsx *.txt"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo:

        ruta_archivo.set(archivo)

        nombre_archivo = os.path.basename(archivo)

        etiqueta_archivo.config(
            text=f"Archivo: {nombre_archivo}"
        )
# ==========================================
# INSERTAR
# ==========================================

def insertar():

    if nombre.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el nombre."
        )
        return

    if contraseña.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar la contraseña."
        )
        return

    if apellido.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el apellido."
        )
        return

    if correo.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el correo electronico."
        )
        return

    if direccion.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar la direccion."
        )
        return

    if ciudad.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar la ciudad."
        )
        return

    if codigo_postal.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el codigo postal."
        )
        return

    if tipo_usuario.get() == "Seleccione":
        messagebox.showwarning(
            "Advertencia",
            "Debe seleccionar el tipo de usuario."
        )
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            estado,
            tipo_usuario,
            imagen,
            archivo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        nombre.get(),
        contraseña.get(),
        apellido.get(),
        direccion.get(),
        ciudad.get(),
        codigo_postal.get(),
        correo.get(),
        comentarios.get(),
        genero.get(),
        estado.get(),
        tipo_usuario.get(),
        ruta_imagen.get(),
        ruta_archivo.get()
    ))

    conexion.commit()
    conexion.close()

    messagebox.showinfo(
        "Registro",
        "Usuario registrado correctamente."
    )

    mostrar_datos()
    limpiar()


# ==========================================
# MOSTRAR DATOS
# ==========================================

def mostrar_datos():

    for elemento in tabla.get_children():
        tabla.delete(elemento)

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            estado,
            tipo_usuario,
            imagen,
            archivo
        FROM usuarios
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()

    conexion.close()

    for registro in registros:

        estado_texto = "Activo" if registro[10] == 1 else "Inactivo"

        tabla.insert(
            "",
            END,
            values=(
                registro[0],
                registro[1],
                registro[3],
                registro[4],
                registro[5],
                registro[6],
                registro[9],
                estado_texto,
                registro[11]
            )
        )


# ==========================================
# SELECCIONAR REGISTRO DEL TREEVIEW
# ==========================================

def seleccionar_registro(event):

    seleccionado = tabla.focus()

    if not seleccionado:
        return

    datos = tabla.item(seleccionado, "values")

    if not datos:
        return

    id_seleccionado.set(datos[0])

    # Cargar todos los campos desde la base de datos
    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT 
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            estado,
            tipo_usuario
        FROM usuarios
        WHERE id = ?
    """, (datos[0],))
    
    registro = cursor.fetchone()
    conexion.close()
    
    if registro:
        nombre.set(registro[0])
        contraseña.set(registro[1])
        apellido.set(registro[2])
        direccion.set(registro[3])
        ciudad.set(registro[4])
        codigo_postal.set(registro[5])
        correo.set(registro[6])
        comentarios.set(registro[7])
        genero.set(registro[8])
        
        if registro[9] == 1:
            estado.set(1)
        else:
            estado.set(0)
        
        tipo_usuario.set(registro[10])

    cargar_archivos_registro(datos[0])


# ==========================================
# CARGAR IMAGEN Y ARCHIVO DEL REGISTRO
# ==========================================

def cargar_archivos_registro(id_usuario):

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT imagen, archivo
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    registro = cursor.fetchone()

    conexion.close()

    if not registro:
        return

    imagen = registro[0]
    archivo = registro[1]

    ruta_imagen.set(imagen if imagen else "")
    ruta_archivo.set(archivo if archivo else "")

    if archivo:
        etiqueta_archivo.config(
            text=f"Archivo: {os.path.basename(archivo)}"
        )
    else:
        etiqueta_archivo.config(
            text="Archivo: No adjunto"
        )

    if imagen and os.path.exists(imagen):

        try:

            img = Image.open(imagen)

            img.thumbnail((150, 150))

            img_tk = ImageTk.PhotoImage(img)

            etiqueta_imagen.config(image=img_tk)

            etiqueta_imagen.image = img_tk

        except:
            etiqueta_imagen.config(image="")
            etiqueta_imagen.image = None

    else:

        etiqueta_imagen.config(image="")
        etiqueta_imagen.image = None


# ==========================================
# ACTUALIZAR
# ==========================================

def actualizar():

    if id_seleccionado.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Seleccione primero un registro."
        )
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET
            nombre = ?,
            contraseña = ?,
            apellido = ?,
            direccion = ?,
            ciudad = ?,
            codigo_postal = ?,
            correo = ?,
            comentarios = ?,
            genero = ?,
            estado = ?,
            tipo_usuario = ?,
            imagen = ?,
            archivo = ?
        WHERE id = ?
    """, (
        nombre.get(),
        contraseña.get(),
        apellido.get(),
        direccion.get(),
        ciudad.get(),
        codigo_postal.get(),
        correo.get(),
        comentarios.get(),
        genero.get(),
        estado.get(),
        tipo_usuario.get(),
        ruta_imagen.get(),
        ruta_archivo.get(),
        id_seleccionado.get()
    ))

    conexion.commit()
    conexion.close()

    messagebox.showinfo(
        "Actualizar",
        "Registro actualizado correctamente."
    )

    mostrar_datos()
    limpiar()


# ==========================================
# ELIMINAR
# ==========================================

def eliminar():

    if id_seleccionado.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Seleccione un registro."
        )
        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Está seguro de eliminar este registro?"
    )

    if respuesta:

        conexion = sqlite3.connect(str(RUTA_BBDD))
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM usuarios
            WHERE id = ?
        """, (id_seleccionado.get(),))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Eliminar",
            "Registro eliminado correctamente."
        )

        mostrar_datos()
        limpiar()


# ==========================================
# BUSCAR
# ==========================================

def buscar():

    texto = entrada_buscar.get()

    for elemento in tabla.get_children():
        tabla.delete(elemento)

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            estado,
            tipo_usuario
        FROM usuarios
        WHERE nombre LIKE ?
        OR apellido LIKE ?
        OR ciudad LIKE ?
        ORDER BY id DESC
    """, (
        "%" + texto + "%",
        "%" + texto + "%",
        "%" + texto + "%"
    ))

    registros = cursor.fetchall()

    conexion.close()

    for registro in registros:

        estado_texto = (
            "Activo"
            if registro[10] == 1
            else "Inactivo"
        )

        tabla.insert(
            "",
            END,
            values=(
                registro[0],
                registro[1],
                registro[3],
                registro[4],
                registro[5],
                registro[6],
                registro[9],
                estado_texto,
                registro[11]
            )
        )


# ==========================================
# FRAME PRINCIPAL DEL FORMULARIO
# ==========================================

miFrame = Frame(
    raiz,
    bd=2,
    relief="groove",
    padx=10,
    pady=10
)

miFrame.pack(
    padx=10,
    pady=10,
    fill="x"
)

# ==========================================
# TÍTULO
# ==========================================

Label(
    miFrame,
    text="FORMULARIO DE REGISTRO DE USUARIOS",
    font=("Arial", 16, "bold")
).grid(
    row=0,
    column=0,
    columnspan=5,
    pady=10
)

# ==========================================
# NOMBRE
# ==========================================

Label(
    miFrame,
    text="Nombre:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=nombre,
    width=25
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# APELLIDO
# ==========================================

Label(
    miFrame,
    text="Apellido:"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=apellido,
    width=25
).grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# IMAGEN DECORATIVA EN COLUMNA 4
# ==========================================

# Cargar la imagen decorativa
imagen_decorativa = None
if RUTA_IMAGEN_FONDO.exists():
    try:
        img_deco = Image.open(str(RUTA_IMAGEN_FONDO))
        # Redimensionar la imagen para que se vea bien
        img_deco = img_deco.resize((180, 220), Image.Resampling.LANCZOS)
        imagen_decorativa = ImageTk.PhotoImage(img_deco)
    except Exception as e:
        print(f"No se pudo cargar la imagen decorativa: {e}")

# Crear label para la imagen decorativa
label_imagen_decorativa = Label(
    miFrame,
    image=imagen_decorativa if imagen_decorativa else "",
    relief="solid",
    bd=1
)
label_imagen_decorativa.grid(
    row=1,
    column=4,
    rowspan=10,
    padx=10,
    pady=5,
    sticky="n"
)

# Guardar referencia para evitar que se borre
label_imagen_decorativa.image = imagen_decorativa

# ==========================================
# CONTRASEÑA
# ==========================================

Label(
    miFrame,
    text="Contraseña:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=contraseña,
    width=25,
    show="*"
).grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# CORREO
# ==========================================

Label(
    miFrame,
    text="Correo:"
).grid(
    row=2,
    column=2,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=correo,
    width=25
).grid(
    row=2,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# DIRECCIÓN
# ==========================================

Label(
    miFrame,
    text="Dirección:"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=direccion,
    width=25
).grid(
    row=3,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# CIUDAD
# ==========================================

Label(
    miFrame,
    text="Ciudad:"
).grid(
    row=3,
    column=2,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=ciudad,
    width=25
).grid(
    row=3,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# CÓDIGO POSTAL
# ==========================================

Label(
    miFrame,
    text="Código Postal:"
).grid(
    row=4,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=codigo_postal,
    width=25
).grid(
    row=4,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# RADIOBUTTON
# ==========================================

Label(
    miFrame,
    text="Género:"
).grid(
    row=4,
    column=2,
    padx=5,
    pady=5
)

Radiobutton(
    miFrame,
    text="Masculino",
    variable=genero,
    value="Masculino"
).grid(
    row=4,
    column=3,
    sticky="w"
)

Radiobutton(
    miFrame,
    text="Femenino",
    variable=genero,
    value="Femenino"
).grid(
    row=5,
    column=3,
    sticky="w"
)

# ==========================================
# CHECKBUTTON
# ==========================================

Checkbutton(
    miFrame,
    text="Usuario activo",
    variable=estado
).grid(
    row=6,
    column=1,
    pady=5
)

# ==========================================
# COMBOBOX
# ==========================================

Label(
    miFrame,
    text="Tipo de usuario:"
).grid(
    row=6,
    column=2,
    padx=5,
    pady=5
)

combo_tipo = ttk.Combobox(
    miFrame,
    textvariable=tipo_usuario,
    values=[
        "Administrador",
        "Docente",
        "Estudiante",
        "Invitado"
    ],
    state="readonly",
    width=22
)

combo_tipo.grid(
    row=6,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# COMENTARIOS
# ==========================================

Label(
    miFrame,
    text="Comentarios:"
).grid(
    row=7,
    column=0,
    padx=5,
    pady=5,
    sticky="ne"
)

Text(
    miFrame,
    height=3,
    width=23,
    wrap=WORD
).grid(
    row=7,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# IMAGEN
# ==========================================

Label(
    miFrame,
    text="Imagen:"
).grid(
    row=8,
    column=0,
    padx=5,
    pady=5
)

Button(
    miFrame,
    text="Seleccionar Imagen",
    command=seleccionar_imagen,
    bg="#3498DB",
    fg="white",
    width=20
).grid(
    row=8,
    column=1,
    padx=5,
    pady=5
)

etiqueta_imagen = Label(
    miFrame,
    width=20,
    height=8,
    relief="sunken"
)

etiqueta_imagen.grid(
    row=8,
    column=2,
    rowspan=3,
    padx=10,
    pady=5
)

# ==========================================
# ARCHIVO ADJUNTO
# ==========================================

Button(
    miFrame,
    text="📎 Adjuntar Archivo",
    command=seleccionar_archivo,
    bg="#9B59B6",
    fg="white",
    width=20
).grid(
    row=9,
    column=1,
    padx=5,
    pady=5
)

etiqueta_archivo = Label(
    miFrame,
    text="Archivo: No adjunto",
    width=30,
    anchor="w"
)

etiqueta_archivo.grid(
    row=10,
    column=0,
    columnspan=2,
    padx=5,
    pady=5
)

# ==========================================
# FRAME DE BOTONES
# ==========================================

frame_botones = Frame(
    raiz,
    bd=2,
    relief="groove",
    padx=10,
    pady=10
)

frame_botones.pack(
    padx=10,
    pady=5,
    fill="x"
)

# ==========================================
# BOTÓN INSERTAR
# ==========================================

Button(
    frame_botones,
    text="💾 INSERTAR",
    command=insertar,
    bg="#27AE60",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTÓN ACTUALIZAR
# ==========================================

Button(
    frame_botones,
    text="♻️ ACTUALIZAR",
    command=actualizar,
    bg="#F39C12",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTÓN ELIMINAR
# ==========================================

Button(
    frame_botones,
    text="🗑️ ELIMINAR",
    command=eliminar,
    bg="#E74C3C",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTON LIMPIAR
# ==========================================

Button(
    frame_botones,
    text="🧹 LIMPIAR",
    command=limpiar,
    bg="#34495E",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTÓN SALIR
# ==========================================

Button(
    frame_botones,
    text="🚪 SALIR",
    command=raiz.destroy,
    bg="#7F8C8D",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BUSCADOR
# ==========================================

frame_buscar = Frame(raiz)
frame_buscar.pack(
    padx=10,
    pady=5,
    fill="x"
)

Label(
    frame_buscar,
    text="Buscar:"
).pack(
    side=LEFT,
    padx=5
)

entrada_buscar = Entry(
    frame_buscar,
    width=40
)

entrada_buscar.pack(
    side=LEFT,
    padx=5
)

Button(
    frame_buscar,
    text="🔍 BUSCAR",
    command=buscar,
    bg="#2980B9",
    fg="white",
    width=15
).pack(
    side=LEFT,
    padx=5
)

Button(
    frame_buscar,
    text="MOSTRAR TODOS",
    command=mostrar_datos,
    bg="#16A085",
    fg="white",
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# FRAME DEL TREEVIEW
# ==========================================

frame_tabla = Frame(
    raiz,
    bd=2,
    relief="groove"
)
frame_tabla.pack(
    padx=10,
    pady=5,
    fill="both",
    expand=True
)

# ==========================================
# SCROLLBAR VERTICAL
# ==========================================

scroll_vertical = Scrollbar(
    frame_tabla,
    orient=VERTICAL
)

scroll_vertical.pack(
    side=RIGHT,
    fill=Y
)

# ==========================================
# SCROLLBAR HORIZONTAL
# ==========================================

scroll_horizontal = Scrollbar(
    frame_tabla,
    orient=HORIZONTAL
)

scroll_horizontal.pack(
    side=BOTTOM,
    fill=X
)

# ==========================================
# TREEVIEW
# ==========================================

columnas = (
    "ID",
    "Nombre",
    "Contraseña",
    "Apellido",
    "Dirección",
    "Ciudad",
    "Código Postal",
    "Correo",
    "Género",
    "Estado",
    "Tipo Usuario"
)

tabla = ttk.Treeview(
    frame_tabla,
    columns=columnas,
    show="headings",
    yscrollcommand=scroll_vertical.set,
    xscrollcommand=scroll_horizontal.set,
    height=10
)

# ==========================================
# CONFIGURAR COLUMNAS
# ==========================================

for columna in columnas:

    tabla.heading(
        columna,
        text=columna
    )

    tabla.column(
        columna,
        width=120,
        anchor="center"
    )

tabla.column("ID", width=50)
tabla.column("Nombre", width=120)
tabla.column("Apellido", width=120)
tabla.column("Dirección", width=180)
tabla.column("Ciudad", width=120)
tabla.column("Código Postal", width=100)
tabla.column("Género", width=100)
tabla.column("Estado", width=100)
tabla.column("Tipo Usuario", width=130)

tabla.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)

# ==========================================
# CONECTAR SCROLLBAR
# ==========================================

scroll_vertical.config(
    command=tabla.yview
)

scroll_horizontal.config(
    command=tabla.xview
)

# ==========================================
# EVENTO TREEVIEW
# ==========================================

tabla.bind(
    "<ButtonRelease-1>",
    seleccionar_registro
)

# ==========================================
# CARGAR DATOS
# ==========================================

mostrar_datos()

# ==========================================
# EJECUTAR
# ==========================================

raiz.mainloop()