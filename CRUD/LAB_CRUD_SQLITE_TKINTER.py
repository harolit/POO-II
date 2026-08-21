#PROYECTO UNIFICADO 1
#CRUD CON TKINTER + SQLITE
#VARIABLES Y LIBRERIAS
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from pathlib import Path

#RUTA DEL PROYECTO
BASE_DIR=Path(__file__).resolve().parent
RUTA_BBDD=BASE_DIR/"BaseHM.db"
RUTA_ICONO=BASE_DIR/"interface_grafica.ico"

#VENTANA PRINCIPAL
raiz=Tk()
raiz.title("Proyecto Unificado 1 - CRUD")

#TAMAÑO DE LA VENTANA
ancho=1100
alto=650

#ICONO DE LA VENTANA
if RUTA_ICONO.exists():
    try:
        raiz.iconbitmap(str(RUTA_ICONO))
    except Exception as e:
        print("No se pudo cargar el icono: ",e)
else:
    print("Advertencia: no se encontro el icono:")
    print(RUTA_ICONO)

#VARIABLES TKINTER
miId=StringVar()
miNombre=StringVar()
miPass=StringVar()
miApellido=StringVar()
miDireccion=StringVar()

#FUNCIONES BDD Y CONEXION
def conexionBBDD():
    conexion=sqlite3.connect(str(RUTA_BBDD))
    cursor=conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TBL_USUARIOS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMBRE_USUARIO VARCHAR(50),
        PASSWORD VARCHAR(50),
        APELLIDO VARCHAR(50),
        DIRECCION VARCHAR(100),
        COMENTARIOS VARCHAR(255)
    )
    """)
    conexion.commit()
    conexion.close()

#VALIDAR CAMPOS
def validarCampos():
    if miNombre.get().strip()=="":
        messagebox.showwarning(
            "Validacion",
            "Ingrese el nombre"
        )
        return False
    if miPass.get().strip()=="":
        messagebox.showwarning(
            "Validacion",
            "Ingrese la contraseña"
        )
        return False
    if miApellido.get().strip()=="":
        messagebox.showwarning(
            "Validacion",
            "Ingrese el apellido"
        )
        return False
    if miDireccion.get().strip()=="":
        messagebox.showwarning(
            "Validacion",
            "Ingrese la direccion"
        )
        return False
    return True

#VALIDAR ID
def validarID():
    if miId.get().strip()=="":
        messagebox.showwarning(
            "Validacion",
            "Ingrese un ID"
        )
        return False
    if not miId.get().isdigit():
        messagebox.showwarning(
            "Validacion",
            "El ID debe ser numerico"
        )
        return False
    return True

#LIMPIAR CAMPOS
def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miPass.set("")
    miApellido.set("")
    miDireccion.set("")
    textComentario.delete(
        "1.0",
        END
    )

#CARGAR CAMPOS EN LA TABLA
def cargarDatos():
    for fila in tabla.get_children():
        tabla.delete(fila)
    conexion=sqlite3.connect(str(RUTA_BBDD))
    cursor=conexion.cursor()
    cursor.execute(
        """
        SELECT
            ID,
            NOMBRE_USUARIO,
            PASSWORD,
            APELLIDO,
            DIRECCION,
            COMENTARIOS
        FROM TBL_USUARIOS
        ORDER BY ID
        """
    )
    registros=cursor.fetchall()
    for registro in registros:
        tabla.insert(
            "",
            END,
            values=registro
        )
    conexion.close()

#CREAR / GUARDAR REGISTRO
def guardar():
    if not validarCampos():
        return
    conexion=sqlite3.connect(str(RUTA_BBDD))
    cursor=conexion.cursor()
    cursor.execute("""
        INSERT INTO TBL_USUARIOS
        (
            NOMBRE_USUARIO,
            PASSWORD,
            APELLIDO,
            DIRECCION,
            COMENTARIOS
        )
        VALUES (?,?,?,?,?)
    """, (
        miNombre.get().strip(),
        miPass.get().strip(),
        miApellido.get().strip(),
        miDireccion.get().strip(),
        textComentario.get("1.0",END).strip()
    ))
    conexion.commit()
    conexion.close()
    messagebox.showinfo(
        "BBDD",
        "Registro guardado correctamente"
    )
    limpiarCampos()
    cargarDatos()

#LEER/CONSULTAR REGISTRO
def consultar():
    if not validarID():
        return
    conexion=sqlite3.connect(str(RUTA_BBDD))
    cursor=conexion.cursor()
    cursor.execute(
        """
        SELECT *
        FROM TBL_USUARIOS
        WHERE ID = ?
        """,
        (miId.get(),)
    )
    usuario=cursor.fetchone()
    conexion.close()
    if usuario:
        miNombre.set(usuario[1])
        miPass.set(usuario[2])
        miApellido.set(usuario[3])
        miDireccion.set(usuario[4])
        textComentario.delete(
            "1.0",
            END
        )
        textComentario.insert(
            "1.0",
            usuario[5]
        )
    else:
        messagebox.showwarning(
            "Consulta",
            "No existe un registro con ese ID"
        )

# ACTUALIZAR REGISTRO
def actualizar():
    if not validarID():
        return
    if not validarCampos():
        return
    conexion=sqlite3.connect(str(RUTA_BBDD))
    cursor=conexion.cursor()
    cursor.execute("""
        UPDATE TBL_USUARIOS
        SET
            NOMBRE_USUARIO = ?,
            PASSWORD = ?,
            APELLIDO = ?,
            DIRECCION = ?,
            COMENTARIOS = ?
        WHERE ID = ?
    """, (
        miNombre.get().strip(),
        miPass.get().strip(),
        miApellido.get().strip(),
        miDireccion.get().strip(),
        textComentario.get("1.0",END).strip(),
        miId.get()
    ))
    conexion.commit()
    registros_actualizados=cursor.rowcount
    conexion.close()
    if registros_actualizados>0:
        messagebox.showinfo(
            "Actualizar",
            "Registro actualizado correctamente"
        )
    else:
        messagebox.showwarning(
            "Actualizar",
            "No existe el ID"
        )
    cargarDatos()
    limpiarCampos()

#ELIMINAR REGISTRO
def eliminar():
    if not validarID():
        return
    respuesta=messagebox.askyesno(
        "Eliminar",
        "¿Desea eliminar este registro?"
    )
    if not respuesta:
        return
    conexion=sqlite3.connect(str(RUTA_BBDD))
    cursor=conexion.cursor()
    cursor.execute(
        """
        DELETE FROM TBL_USUARIOS
        WHERE ID = ?
        """,
        (miId.get(),)
    )
    conexion.commit()
    registros_eliminados=cursor.rowcount
    conexion.close()
    if registros_eliminados>0:
        messagebox.showinfo(
            "Eliminar",
            "Registro eliminado correctamente"
        )
    else:
        messagebox.showwarning(
            "Eliminar",
            "No existe el ID"
        )
    cargarDatos()
    limpiarCampos()

#SELECCIONAR REGISTRO DE LA TABLA
def seleccionarRegistro(event):
    item=tabla.focus()
    if item == "":
        return
    datos=tabla.item(item)["values"]
    if not datos:
        return
    miId.set(datos[0])
    miNombre.set(datos[1])
    miPass.set(datos[2])
    miApellido.set(datos[3])
    miDireccion.set(datos[4])
    textComentario.delete(
        "1.0",
        END
    )
    textComentario.insert(
        "1.0",
        datos[5]
    )

#SALIR DE LA APLICACION
def salirAplicacion():
    valor=messagebox.askyesno(
        "Salir",
        "¿Desea salir de la aplicacion?"
    )
    if valor:
        raiz.destroy()

def salir():
    salirAplicacion()

#MENU
barraMenu=Menu(raiz)
raiz.config(menu=barraMenu)

#MENU BBDD
menuBBDD=Menu(
    barraMenu,
    tearoff=0
)
menuBBDD.add_command(
    label="Conectar",
    command=conexionBBDD
)
menuBBDD.add_separator()
menuBBDD.add_command(
    label="Salir",
    command=salirAplicacion
)
barraMenu.add_cascade(
    label="BBDD",
    menu=menuBBDD
)

#MENU AYUDA
menuAyuda=Menu(
    barraMenu,
    tearoff=0
)
menuAyuda.add_command(
    label="Acerca de",
    command=lambda: messagebox.showinfo(
        "Acerca de",
        "Proyecto Unificado 1\n"
        "CRUD con Tkinter y SQLite\n"
        "Desarrollado en Python\n"
        "CREADO POR: Harold Morales 1\n"
    )
)
barraMenu.add_cascade(
    label="Ayuda",
    menu=menuAyuda
)

# CREAR BASE DE DATOS
conexionBBDD()

# CENTRAR LA VENTANA EN LA PANTALLA
ancho_pantalla = raiz.winfo_screenwidth()
alto_pantalla = raiz.winfo_screenheight()
posicion_x = int(
    (ancho_pantalla - ancho) / 2
)
posicion_y = int(
    (alto_pantalla - alto) / 2
)
raiz.geometry(
    f"{ancho}x{alto}+{posicion_x}+{posicion_y}"
)

# FRAME DATOS
miFrame = Frame(
    raiz
)
miFrame.pack(
    pady=10
)

# ID
Label(
    miFrame,
    text="ID"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miId,
    width=30
).grid(
    row=0,
    column=1
)

# NOMBRE
Label(
    miFrame,
    text="Nombre"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miNombre,
    width=30
).grid(
    row=1,
    column=1
)

# PASSWORD
Label(
    miFrame,
    text="Password"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miPass,
    show="#",
    width=30
).grid(
    row=2,
    column=1
)

# APELLIDO
Label(
    miFrame,
    text="Apellido"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miApellido,
    width=30
).grid(
    row=3,
    column=1
)

# DIRECCION
Label(
    miFrame,
    text="Dirección"
).grid(
    row=4,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miDireccion,
    width=30
).grid(
    row=4,
    column=1
)

# COMENTARIOS
Label(
    miFrame,
    text="Comentarios"
).grid(
    row=5,
    column=0,
    padx=5,
    pady=5
)
textComentario = Text(
    miFrame,
    width=30,
    height=5
)
textComentario.grid(
    row=5,
    column=1
)

# SCROLL DE COMENTARIOS
scroll = Scrollbar(
    miFrame,
    command=textComentario.yview
)
scroll.grid(
    row=5,
    column=2,
    sticky="nsew"
)
textComentario.config(
    yscrollcommand=scroll.set
)

# FRAME BOTONES
frameBotones = Frame(
    raiz
)
frameBotones.pack(
    pady=10
)

# BOTONES (CORREGIDO: Ahora cada uno está en una columna diferente para no superponerse)
Button(
    frameBotones,
    text="Guardar",
    width=15,
    command=guardar
).grid(
    row=0,
    column=0,
    padx=5
)

Button(
    frameBotones,
    text="Consultar",
    width=15,
    command=consultar
).grid(
    row=0,
    column=1,
    padx=5
)

Button(
    frameBotones,
    text="Actualizar",
    width=15,
    command=actualizar
).grid(
    row=0,
    column=2,
    padx=5
)

Button(
    frameBotones,
    text="Eliminar",
    width=15,
    command=eliminar
).grid(
    row=0,
    column=3,
    padx=5
)

Button(
    frameBotones,
    text="Limpiar",
    width=15,
    command=limpiarCampos
).grid(
    row=0,
    column=4,
    padx=5
)

Button(
    frameBotones,
    text="Salir",
    width=15,
    command=salirAplicacion
).grid(
    row=0,
    column=5,
    padx=5
)

# FRAME TABLA
frameTabla = Frame(
    raiz
)
frameTabla.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# TABLA TREEVIEW
tabla = ttk.Treeview(
    frameTabla,
    columns=(
        "ID",
        "NOMBRE",
        "PASSWORD",
        "APELLIDO",
        "DIRECCION",
        "COMENTARIOS"
    ),
    show="headings"
)

# ENCABEZADOS
tabla.heading(
    "ID",
    text="ID"
)
tabla.heading(
    "NOMBRE",
    text="Nombre"
)
tabla.heading(
    "PASSWORD",
    text="Password"
)
tabla.heading(
    "APELLIDO",
    text="Apellido"
)
tabla.heading(
    "DIRECCION",
    text="Dirección"
)
tabla.heading(
    "COMENTARIOS",
    text="Comentarios"
)

# ANCHO DE COLUMNAS
tabla.column(
    "ID",
    width=50,
    anchor="center"
)
tabla.column(
    "NOMBRE",
    width=150
)
tabla.column(
    "PASSWORD",
    width=120
)
tabla.column(
    "APELLIDO",
    width=150
)
tabla.column(
    "DIRECCION",
    width=200
)
tabla.column(
    "COMENTARIOS",
    width=300
)

# SCROLL VERTICAL DE LA TABLA
scrollTabla = Scrollbar(
    frameTabla,
    orient=VERTICAL,
    command=tabla.yview
)
tabla.configure(
    yscrollcommand=scrollTabla.set
)

# MOSTRAR TABLA
tabla.pack(
    side=LEFT,
    fill="both",
    expand=True
)
scrollTabla.pack(
    side=RIGHT,
    fill="y"
)

# EVENTO SELECCIONAR REGISTRO
tabla.bind(
    "<<TreeviewSelect>>",
    seleccionarRegistro
)

# CARGAR REGISTROS EXISTENTES
cargarDatos()

# CERRAR CON LA X DE LA VENTANA
raiz.protocol(
    "WM_DELETE_WINDOW",
    salirAplicacion
)

#EJECUTAR APLICACION
raiz.mainloop()