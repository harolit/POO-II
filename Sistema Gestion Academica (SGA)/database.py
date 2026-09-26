"""
Módulo de conexión y gestión de la base de datos SQLite.
Diseño normalizado en 3FN según el documento del proyecto SGA.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sga.db')


def get_connection():
    """Retorna una conexión activa a la base de datos SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Crea todas las tablas del sistema según el MER (14 entidades en 3FN)."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla 1: ROL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rol (
            id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_rol VARCHAR(50) UNIQUE NOT NULL,
            descripcion TEXT
        )
    """)

    # Tabla 2: USUARIO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(256) NOT NULL,
            id_rol INTEGER NOT NULL,
            estado BOOLEAN DEFAULT 1,
            intentos_fallidos INTEGER DEFAULT 0,
            FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
        )
    """)

    # Tabla 3: PLAN_ESTUDIO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plan_estudio (
            id_plan INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_plan VARCHAR(20) UNIQUE NOT NULL,
            nombre_plan VARCHAR(150) NOT NULL,
            version VARCHAR(10) NOT NULL,
            fecha_creacion DATE NOT NULL
        )
    """)

    # Tabla 4: COMPETENCIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competencia (
            id_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo VARCHAR(30) NOT NULL,
            nombre VARCHAR(200) NOT NULL,
            id_plan INTEGER NOT NULL,
            FOREIGN KEY (id_plan) REFERENCES plan_estudio(id_plan)
        )
    """)

    # Tabla 5: RESULTADO_APRENDIZAJE (RAP)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultado_aprendizaje (
            id_rap INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo VARCHAR(30) NOT NULL,
            descripcion TEXT NOT NULL,
            id_competencia INTEGER NOT NULL,
            FOREIGN KEY (id_competencia) REFERENCES competencia(id_competencia)
        )
    """)

    # Tabla 6: ASIGNATURA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asignatura (
            id_asignatura INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo VARCHAR(30) NOT NULL,
            nombre VARCHAR(120) NOT NULL,
            creditos INTEGER NOT NULL,
            id_rap INTEGER,
            FOREIGN KEY (id_rap) REFERENCES resultado_aprendizaje(id_rap)
        )
    """)

    # Tabla 7: INSTRUCTOR
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructor (
            id_instructor INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            especialidad VARCHAR(100) NOT NULL,
            documento VARCHAR(20) UNIQUE NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    # Tabla 8: APRENDIZ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aprendiz (
            id_aprendiz INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            documento VARCHAR(20) UNIQUE NOT NULL,
            ficha VARCHAR(20) NOT NULL,
            estado VARCHAR(30) DEFAULT 'En Formación',
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    # Tabla 9: MATRICULA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matricula (
            id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aprendiz INTEGER NOT NULL,
            id_asignatura INTEGER NOT NULL,
            periodo VARCHAR(20) NOT NULL,
            estado VARCHAR(20) DEFAULT 'Activa',
            FOREIGN KEY (id_aprendiz) REFERENCES aprendiz(id_aprendiz),
            FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura)
        )
    """)

    # Tabla 10: EVALUACION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluacion (
            id_evaluacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_asignatura INTEGER NOT NULL,
            id_instructor INTEGER NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            ponderacion DECIMAL(5,2) NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura),
            FOREIGN KEY (id_instructor) REFERENCES instructor(id_instructor)
        )
    """)

    # Tabla 11: CALIFICACION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calificacion (
            id_calificacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evaluacion INTEGER NOT NULL,
            id_aprendiz INTEGER NOT NULL,
            nota DECIMAL(3,2) NOT NULL,
            observacion TEXT,
            FOREIGN KEY (id_evaluacion) REFERENCES evaluacion(id_evaluacion),
            FOREIGN KEY (id_aprendiz) REFERENCES aprendiz(id_aprendiz)
        )
    """)

    # Tabla 12: ASISTENCIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asistencia (
            id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aprendiz INTEGER NOT NULL,
            id_asignatura INTEGER NOT NULL,
            fecha DATE NOT NULL,
            estado VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_aprendiz) REFERENCES aprendiz(id_aprendiz),
            FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura)
        )
    """)

    # Tabla 13: NOTIFICACION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificacion (
            id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            fecha_envio DATETIME NOT NULL,
            leido BOOLEAN DEFAULT 0,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    # Tabla 14: AUDITORIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            accion VARCHAR(100) NOT NULL,
            detalle TEXT,
            fecha DATETIME NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    conn.commit()
    _seed_data(conn)
    conn.close()


def _seed_data(conn):
    """Inserta datos iniciales si la BD está vacía."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rol")
    if cursor.fetchone()[0] > 0:
        return

    # Roles base
    roles = [
        ('Administrador', 'Acceso total al sistema'),
        ('Coordinador', 'Gestión académica y reportes'),
        ('Instructor', 'Calificaciones y asistencia'),
        ('Aprendiz', 'Consulta de notas e historial'),
    ]
    cursor.executemany("INSERT INTO rol (nombre_rol, descripcion) VALUES (?, ?)", roles)

    # Usuarios demo (password: admin123, etc.)
    from utils.security import hash_password
    usuarios = [
        ('Administrador SGA', 'admin@sga.edu.co', hash_password('admin123'), 1),
        ('Coordinador Académico', 'coord@sga.edu.co', hash_password('coord123'), 2),
        ('Instructor Demo', 'instructor@sga.edu.co', hash_password('inst123'), 3),
        ('Aprendiz Demo', 'aprendiz@sga.edu.co', hash_password('apre123'), 4),
    ]
    cursor.executemany(
        "INSERT INTO usuario (nombre, email, password_hash, id_rol) VALUES (?, ?, ?, ?)",
        usuarios
    )

    # Plan de estudio demo
    cursor.execute("""
        INSERT INTO plan_estudio (codigo_plan, nombre_plan, version, fecha_creacion)
        VALUES ('ADSO-2026', 'Análisis y Desarrollo de Software', '1.0', ?)
    """, (datetime.now().strftime('%Y-%m-%d'),))
    id_plan = cursor.lastrowid

    # Competencia y RAP demo
    cursor.execute("""
        INSERT INTO competencia (codigo, nombre, id_plan) VALUES (?, ?, ?)
    """, ('COMP-001', 'Desarrollar software con POO', id_plan))
    id_comp = cursor.lastrowid

    cursor.execute("""
        INSERT INTO resultado_aprendizaje (codigo, descripcion, id_competencia)
        VALUES (?, ?, ?)
    """, ('RAP-001', 'Implementar clases y objetos en Python', id_comp))
    id_rap = cursor.lastrowid

    # Asignatura demo
    cursor.execute("""
        INSERT INTO asignatura (codigo, nombre, creditos, id_rap) VALUES (?, ?, ?, ?)
    """, ('POO-201', 'Programación Orientada a Objetos II', 4, id_rap))

    # Instructor demo
    cursor.execute("""
        INSERT INTO instructor (id_usuario, especialidad, documento)
        VALUES (3, 'Ingeniería de Software', '12345678')
    """)

    # Aprendiz demo
    cursor.execute("""
        INSERT INTO aprendiz (id_usuario, documento, ficha) VALUES (4, '98765432', 'ADSO-2560')
    """)

    conn.commit()


if __name__ == '__main__':
    init_database()
    print("✅ Base de datos SGA inicializada correctamente.")