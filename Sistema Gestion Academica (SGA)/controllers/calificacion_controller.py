"""
Controlador del módulo de Calificaciones - CU05.
"""
from database import get_connection
from utils.helpers import validar_nota


class CalificacionController:

    @staticmethod
    def listar_evaluaciones():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id_evaluacion, e.nombre, e.ponderacion, a.nombre AS asignatura
            FROM evaluacion e
            JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def listar_aprendices():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id_aprendiz, u.nombre, a.documento
            FROM aprendiz a JOIN usuario u ON a.id_usuario = u.id_usuario
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def registrar_calificacion(id_evaluacion, id_aprendiz, nota, observacion=""):
        if not validar_nota(nota):
            return False, "Nota fuera de rango permitido (0.0 - 5.0)."

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO calificacion (id_evaluacion, id_aprendiz, nota, observacion)
                VALUES (?, ?, ?, ?)
            """, (id_evaluacion, id_aprendiz, float(nota), observacion))
            conn.commit()
            return True, "Calificación registrada correctamente."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def calcular_promedio_aprendiz(id_aprendiz):
        """Calcula el promedio ponderado del aprendiz."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nota, e.ponderacion
            FROM calificacion c
            JOIN evaluacion e ON c.id_evaluacion = e.id_evaluacion
            WHERE c.id_aprendiz = ?
        """, (id_aprendiz,))
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return 0.0
        total = sum(r['nota'] * (r['ponderacion'] / 100) for r in rows)
        return round(total, 2)