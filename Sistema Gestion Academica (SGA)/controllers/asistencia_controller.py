"""
Controlador del módulo de Asistencia - CU09.
"""
from database import get_connection
from datetime import datetime


class AsistenciaController:

    @staticmethod
    def listar_asistencias():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id_asistencia, s.fecha, s.estado,
                   u.nombre AS aprendiz, a.nombre AS asignatura
            FROM asistencia s
            JOIN aprendiz ap ON s.id_aprendiz = ap.id_aprendiz
            JOIN usuario u ON ap.id_usuario = u.id_usuario
            JOIN asignatura a ON s.id_asignatura = a.id_asignatura
            ORDER BY s.fecha DESC
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def registrar_asistencia(id_aprendiz, id_asignatura, fecha, estado):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO asistencia (id_aprendiz, id_asignatura, fecha, estado)
                VALUES (?, ?, ?, ?)
            """, (id_aprendiz, id_asignatura, fecha, estado))
            conn.commit()
            return True, "Asistencia registrada correctamente."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def porcentaje_inasistencia(id_aprendiz):
        """Calcula el % de inasistencia del aprendiz."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM asistencia WHERE id_aprendiz = ?", (id_aprendiz,))
        total = cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(*) FROM asistencia
            WHERE id_aprendiz = ? AND estado IN ('Falla', 'Falla Justificada')
        """, (id_aprendiz,))
        fallas = cursor.fetchone()[0]
        conn.close()
        return round((fallas / total) * 100, 2) if total > 0 else 0.0