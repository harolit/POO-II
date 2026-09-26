"""
Controlador del módulo de Reportes - CU07 y CU12.
"""
from database import get_connection
from datetime import datetime


class ReporteController:

    @staticmethod
    def generar_reporte_notas():
        """Genera consolidado de notas por aprendiz y asignatura."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.nombre AS aprendiz, a.nombre AS asignatura,
                   c.nota, e.nombre AS evaluacion, e.ponderacion
            FROM calificacion c
            JOIN aprendiz ap ON c.id_aprendiz = ap.id_aprendiz
            JOIN usuario u ON ap.id_usuario = u.id_usuario
            JOIN evaluacion e ON c.id_evaluacion = e.id_evaluacion
            JOIN asignatura a ON e.id_asignatura = a.id_asignatura
            ORDER BY u.nombre, a.nombre
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def generar_certificado(id_aprendiz):
        """Verifica si el aprendiz puede obtener certificado (CU12)."""
        conn = get_connection()
        cursor = conn.cursor()
        # Verificar promedio >= 3.0
        cursor.execute("""
            SELECT c.nota, e.ponderacion FROM calificacion c
            JOIN evaluacion e ON c.id_evaluacion = e.id_evaluacion
            WHERE c.id_aprendiz = ?
        """, (id_aprendiz,))
        rows = cursor.fetchall()
        if not rows:
            conn.close()
            return False, "El aprendiz no tiene calificaciones registradas."

        promedio = sum(r['nota'] * (r['ponderacion'] / 100) for r in rows)
        if promedio < 3.0:
            conn.close()
            return False, f"Promedio insuficiente ({promedio:.2f}). No cumple requisitos."

        # Verificar inasistencias
        cursor.execute("SELECT COUNT(*) FROM asistencia WHERE id_aprendiz = ?", (id_aprendiz,))
        total = cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(*) FROM asistencia
            WHERE id_aprendiz = ? AND estado IN ('Falla', 'Falla Justificada')
        """, (id_aprendiz,))
        fallas = cursor.fetchone()[0]
        conn.close()

        if total > 0 and (fallas / total) > 0.15:
            return False, "Inasistencia superior al 15%. No cumple requisitos."

        codigo_verificacion = f"SGA-{id_aprendiz}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return True, {
            'codigo': codigo_verificacion,
            'promedio': round(promedio, 2),
            'fecha': datetime.now().strftime('%d/%m/%Y'),
        }