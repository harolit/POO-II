"""
Vista del módulo de Asistencia - CU09.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.asistencia_controller import AsistenciaController
from controllers.calificacion_controller import CalificacionController
from controllers.evaluacion_controller import EvaluacionController
from datetime import datetime


class AsistenciaView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="🗓 Control de Asistencia Diaria",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Registrar Asistencia",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Aprendiz:", bg="#f1f5f9").grid(row=0, column=0, sticky="w")
        self.combo_apre = ttk.Combobox(form, width=30, state="readonly")
        self.combo_apre.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Asignatura:", bg="#f1f5f9").grid(row=0, column=2, sticky="w")
        self.combo_asig = ttk.Combobox(form, width=30, state="readonly")
        self.combo_asig.grid(row=0, column=3, padx=5)

        tk.Label(form, text="Fecha:", bg="#f1f5f9").grid(row=0, column=4, sticky="w")
        self.e_fecha = tk.Entry(form, width=12)
        self.e_fecha.grid(row=0, column=5, padx=5)
        self.e_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))

        tk.Label(form, text="Estado:", bg="#f1f5f9").grid(row=0, column=6, sticky="w")
        self.combo_estado = ttk.Combobox(form, width=18, state="readonly",
                                         values=["Presente", "Falla", "Falla Justificada", "Retardo"])
        self.combo_estado.current(0)
        self.combo_estado.grid(row=0, column=7, padx=5)

        tk.Button(form, text="💾 Guardar", bg="#0ea5e9", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._guardar).grid(row=0, column=8, padx=10)

        self._cargar_combos()

        cols = ("ID", "Aprendiz", "Asignatura", "Fecha", "Estado")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _cargar_combos(self):
        apres = CalificacionController.listar_aprendices()
        self.combo_apre['values'] = [f"{a['id_aprendiz']} - {a['nombre']}" for a in apres]
        if apres:
            self.combo_apre.current(0)

        asigs = EvaluacionController.listar_asignaturas()
        self.combo_asig['values'] = [f"{a['id_asignatura']} - {a['nombre']}" for a in asigs]
        if asigs:
            self.combo_asig.current(0)

    def _cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for a in AsistenciaController.listar_asistencias():
            self.tree.insert("", "end", values=(
                a['id_asistencia'], a['aprendiz'], a['asignatura'],
                a['fecha'], a['estado']
            ))

    def _guardar(self):
        try:
            id_apre = int(self.combo_apre.get().split(" - ")[0])
            id_asig = int(self.combo_asig.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Seleccione aprendiz y asignatura.")
            return

        exito, msg = AsistenciaController.registrar_asistencia(
            id_apre, id_asig, self.e_fecha.get().strip(), self.combo_estado.get()
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._cargar()
        else:
            messagebox.showerror("Error", msg)