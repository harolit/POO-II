"""
Controlador del módulo de Evaluaciones - CU04.
"""
from database import get_connection
from datetime import datetime


class EvaluacionController:

    @staticmethod
    def listar_evaluaciones():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id_evaluacion, e.nombre, e.ponderacion, e.fecha,
                   a.nombre AS asignatura, i.especialidad
            FROM evaluacion e
            JOIN asignatura a ON e.id_asignatura = a.id_asignatura
            JOIN instructor i ON e.id_instructor = i.id_instructor
            ORDER BY e.fecha DESC
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def listar_asignaturas():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_asignatura, nombre FROM asignatura")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def crear_evaluacion(id_asignatura, id_instructor, nombre, ponderacion, fecha):
        try:
            ponderacion = float(ponderacion)
        except ValueError:
            return False, "La ponderación debe ser un número."

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Validar que la suma de ponderaciones no supere 100%
            cursor.execute("""
                SELECT COALESCE(SUM(ponderacion), 0) FROM evaluacion
                WHERE id_asignatura = ?
            """, (id_asignatura,))
            suma_actual = cursor.fetchone()[0]
            if suma_actual + ponderacion > 100:
                return False, f"La ponderación total superaría 100% (actual: {suma_actual}%)."

            cursor.execute("""
                INSERT INTO evaluacion (id_asignatura, id_instructor, nombre, ponderacion, fecha)
                VALUES (?, ?, ?, ?, ?)
            """, (id_asignatura, id_instructor, nombre, ponderacion, fecha))
            conn.commit()
            return True, "Evaluación programada correctamente."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()