"""
Controlador del módulo de Planes de Estudio - CU02.
"""
from database import get_connection
from datetime import datetime


class PlanController:

    @staticmethod
    def listar_planes():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plan_estudio ORDER BY id_plan DESC")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def crear_plan(codigo, nombre, version):
        if not codigo or not nombre or not version:
            return False, "Todos los campos son obligatorios."
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO plan_estudio (codigo_plan, nombre_plan, version, fecha_creacion)
                VALUES (?, ?, ?, ?)
            """, (codigo, nombre, version, datetime.now().strftime('%Y-%m-%d')))
            conn.commit()
            return True, "Plan de estudio registrado correctamente."
        except Exception as e:
            return False, f"Error: El código del plan ya existe. ({e})"
        finally:
            conn.close()

    @staticmethod
    def listar_competencias(id_plan):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM competencia WHERE id_plan = ?", (id_plan,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def crear_competencia(codigo, nombre, id_plan):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO competencia (codigo, nombre, id_plan) VALUES (?, ?, ?)
            """, (codigo, nombre, id_plan))
            conn.commit()
            return True, "Competencia registrada."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def crear_rap(codigo, descripcion, id_competencia):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO resultado_aprendizaje (codigo, descripcion, id_competencia)
                VALUES (?, ?, ?)
            """, (codigo, descripcion, id_competencia))
            conn.commit()
            return True, "RAP registrado correctamente."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()