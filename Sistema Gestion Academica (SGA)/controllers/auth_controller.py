"""
Controlador de autenticación - CU01.
"""
from database import get_connection
from utils.security import verify_password
from datetime import datetime


class AuthController:

    @staticmethod
    def login(email: str, password: str):
        """Valida credenciales. Retorna (exito, mensaje, datos_usuario)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.email, u.password_hash,
                   u.estado, u.intentos_fallidos, r.nombre_rol, r.id_rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.email = ?
        """, (email,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return False, "Usuario no encontrado.", None

        if not user['estado']:
            conn.close()
            return False, "Usuario bloqueado. Contacte al administrador.", None

        if user['intentos_fallidos'] >= 3:
            conn.close()
            return False, "Cuenta bloqueada por 3 intentos fallidos.", None

        if not verify_password(password, user['password_hash']):
            cursor.execute("""
                UPDATE usuario SET intentos_fallidos = intentos_fallidos + 1
                WHERE id_usuario = ?
            """, (user['id_usuario'],))
            conn.commit()
            conn.close()
            return False, "Contraseña incorrecta.", None

        # Login exitoso: resetear intentos y registrar bitácora
        cursor.execute("""
            UPDATE usuario SET intentos_fallidos = 0 WHERE id_usuario = ?
        """, (user['id_usuario'],))
        cursor.execute("""
            INSERT INTO auditoria (id_usuario, accion, detalle, fecha)
            VALUES (?, ?, ?, ?)
        """, (user['id_usuario'], 'LOGIN', f"Sesión iniciada: {email}",
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        datos = {
            'id_usuario': user['id_usuario'],
            'nombre': user['nombre'],
            'email': user['email'],
            'rol': user['nombre_rol'],
            'id_rol': user['id_rol'],
        }
        return True, "Acceso concedido.", datos

    @staticmethod
    def registrar_bitacora(id_usuario, accion, detalle=""):
        """Registra evento en la bitácora de auditoría."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO auditoria (id_usuario, accion, detalle, fecha)
            VALUES (?, ?, ?, ?)
        """, (id_usuario, accion, detalle,
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()