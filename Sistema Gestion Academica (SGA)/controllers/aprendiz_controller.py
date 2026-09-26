"""
Controlador del módulo de Aprendices - CU03.
"""
from database import get_connection
from utils.security import hash_password
from utils.helpers import validar_email


class AprendizController:

    @staticmethod
    def listar_aprendices():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id_aprendiz, a.documento, a.ficha, a.estado,
                   u.nombre, u.email, u.id_usuario
            FROM aprendiz a
            JOIN usuario u ON a.id_usuario = u.id_usuario
            ORDER BY a.id_aprendiz DESC
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def registrar_aprendiz(nombre, email, documento, ficha):
        if not all([nombre, email, documento, ficha]):
            return False, "Todos los campos son obligatorios."
        if not validar_email(email):
            return False, "El correo electrónico no es válido."

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Validar duplicados
            cursor.execute("SELECT id_usuario FROM usuario WHERE email = ?", (email,))
            if cursor.fetchone():
                return False, "El correo ya está registrado."
            cursor.execute("SELECT id_aprendiz FROM aprendiz WHERE documento = ?", (documento,))
            if cursor.fetchone():
                return False, "El documento ya está registrado."

            # Crear usuario con rol Aprendiz (id_rol=4)
            pwd_hash = hash_password(documento)  # Password inicial = documento
            cursor.execute("""
                INSERT INTO usuario (nombre, email, password_hash, id_rol)
                VALUES (?, ?, ?, 4)
            """, (nombre, email, pwd_hash))
            id_usuario = cursor.lastrowid

            # Crear aprendiz
            cursor.execute("""
                INSERT INTO aprendiz (id_usuario, documento, ficha)
                VALUES (?, ?, ?)
            """, (id_usuario, documento, ficha))
            conn.commit()
            return True, f"Aprendiz registrado. Contraseña inicial: {documento}"
        except Exception as e:
            conn.rollback()
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def matricular(id_aprendiz, id_asignatura, periodo):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO matricula (id_aprendiz, id_asignatura, periodo)
                VALUES (?, ?, ?)
            """, (id_aprendiz, id_asignatura, periodo))
            conn.commit()
            return True, "Matrícula registrada correctamente."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()