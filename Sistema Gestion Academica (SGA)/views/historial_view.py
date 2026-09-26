"""
Vista del Historial Académico - CU06.
"""
import tkinter as tk
from tkinter import ttk
from controllers.calificacion_controller import CalificacionController
from controllers.asistencia_controller import AsistenciaController
from database import get_connection


class HistorialView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="📖 Historial Académico",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        cols = ("Aprendiz", "Asignatura", "Evaluación", "Nota", "Ponderación")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.lbl_prom = tk.Label(self.parent, text="", font=("Segoe UI", 12, "bold"),
                                 bg="#f1f5f9", fg="#0f172a")
        self.lbl_prom.pack(pady=10)

    def _cargar(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.nombre AS aprendiz, a.nombre AS asignatura,
                       e.nombre AS evaluacion, c.nota, e.ponderacion
                FROM calificacion c
                JOIN aprendiz ap ON c.id_aprendiz = ap.id_aprendiz
                JOIN usuario u ON ap.id_usuario = u.id_usuario
                JOIN evaluacion e ON c.id_evaluacion = e.id_evaluacion
                JOIN asignatura a ON e.id_asignatura = a.id_asignatura
                ORDER BY u.nombre
            """)
            for r in cursor.fetchall():
                self.tree.insert("", "end", values=(
                    r['aprendiz'], r['asignatura'], r['evaluacion'],
                    f"{r['nota']:.2f}", f"{r['ponderacion']}%"
                ))
            conn.close()
            self.lbl_prom.config(text="📊 Promedios calculados automáticamente por ponderación")
        except Exception as e:
            print(f"Error: {e}")