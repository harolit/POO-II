"""
Controlador del módulo de Usuarios - CU08.
"""
from database import get_connection
from utils.security import hash_password


class UsuarioController:

    @staticmethod
    def listar_usuarios():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.email, u.estado, r.nombre_rol
            FROM usuario u JOIN rol r ON u.id_rol = r.id_rol
            ORDER BY u.id_usuario
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def listar_roles():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_rol, nombre_rol FROM rol")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def crear_usuario(nombre, email, password, id_rol):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuario (nombre, email, password_hash, id_rol)
                VALUES (?, ?, ?, ?)
            """, (nombre, email, hash_password(password), id_rol))
            conn.commit()
            return True, "Usuario creado correctamente."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(id_usuario, estado):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET estado = ? WHERE id_usuario = ?", (estado, id_usuario))
        conn.commit()
        conn.close()
        return True, "Estado actualizado."