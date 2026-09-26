"""
Vista principal del Dashboard - CU10.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.calificacion_controller import CalificacionController
from controllers.asistencia_controller import AsistenciaController
from controllers.reporte_controller import ReporteController


class DashboardView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()

    def _construir_ui(self):
        # Título
        header = tk.Frame(self.parent, bg="#0f172a", pady=15)
        header.pack(fill="x")
        tk.Label(header, text=f"📊 Dashboard - Bienvenido, {self.usuario['nombre']}",
                 font=("Segoe UI", 16, "bold"), bg="#0f172a", fg="#f1f5f9").pack(side="left", padx=20)
        tk.Label(header, text=f"Rol: {self.usuario['rol']}",
                 font=("Segoe UI", 11), bg="#0f172a", fg="#38bdf8").pack(side="right", padx=20)

        # Tarjetas KPI
        kpi_frame = tk.Frame(self.parent, bg="#f1f5f9", pady=20)
        kpi_frame.pack(fill="x", padx=20)

        self._crear_kpi(kpi_frame, "👥 Aprendices", self._contar("aprendiz"), "#0ea5e9")
        self._crear_kpi(kpi_frame, "📚 Planes", self._contar("plan_estudio"), "#10b981")
        self._crear_kpi(kpi_frame, "📝 Evaluaciones", self._contar("evaluacion"), "#f59e0b")
        self._crear_kpi(kpi_frame, "🗓 Asistencias", self._contar("asistencia"), "#8b5cf6")

        # Panel de promedios
        tk.Label(self.parent, text="📈 Rendimiento Académico",
                 font=("Segoe UI", 13, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=(20, 5))

        cols = ("Aprendiz", "Promedio", "Inasistencia %")
        tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=200, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Cargar aprendices con promedios
        try:
            from database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ap.id_aprendiz, u.nombre
                FROM aprendiz ap JOIN usuario u ON ap.id_usuario = u.id_usuario
            """)
            for row in cursor.fetchall():
                promedio = CalificacionController.calcular_promedio_aprendiz(row['id_aprendiz'])
                inasist = AsistenciaController.porcentaje_inasistencia(row['id_aprendiz'])
                tree.insert("", "end", values=(row['nombre'], f"{promedio:.2f}", f"{inasist}%"))
            conn.close()
        except Exception as e:
            print(f"Error cargando dashboard: {e}")

    def _crear_kpi(self, parent, titulo, valor, color):
        frame = tk.Frame(parent, bg="white", padx=20, pady=15, relief="ridge", bd=1)
        frame.pack(side="left", padx=10, expand=True, fill="both")
        tk.Label(frame, text=titulo, font=("Segoe UI", 10), bg="white", fg="#64748b").pack(anchor="w")
        tk.Label(frame, text=str(valor), font=("Segoe UI", 24, "bold"), bg="white", fg=color).pack(anchor="w")

    def _contar(self, tabla):
        try:
            from database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            n = cursor.fetchone()[0]
            conn.close()
            return n
        except Exception:
            return 0