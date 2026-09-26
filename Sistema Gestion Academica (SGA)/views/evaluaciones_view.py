"""
Vista del módulo de Evaluaciones - CU04.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.evaluacion_controller import EvaluacionController
from datetime import datetime


class EvaluacionesView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="📝 Programación de Evaluaciones",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Nueva Evaluación",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Asignatura:", bg="#f1f5f9").grid(row=0, column=0, sticky="w")
        self.combo_asig = ttk.Combobox(form, width=28, state="readonly")
        self.combo_asig.grid(row=0, column=1, padx=5)
        self._cargar_asignaturas()

        tk.Label(form, text="Nombre:", bg="#f1f5f9").grid(row=0, column=2, sticky="w")
        self.e_nombre = tk.Entry(form, width=25)
        self.e_nombre.grid(row=0, column=3, padx=5)

        tk.Label(form, text="Ponderación %:", bg="#f1f5f9").grid(row=0, column=4, sticky="w")
        self.e_pond = tk.Entry(form, width=10)
        self.e_pond.grid(row=0, column=5, padx=5)

        tk.Label(form, text="Fecha (YYYY-MM-DD):", bg="#f1f5f9").grid(row=0, column=6, sticky="w")
        self.e_fecha = tk.Entry(form, width=15)
        self.e_fecha.grid(row=0, column=7, padx=5)
        self.e_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))

        tk.Button(form, text="➕ Programar", bg="#f59e0b", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._crear).grid(row=0, column=8, padx=15)

        cols = ("ID", "Evaluación", "Asignatura", "Ponderación", "Fecha")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _cargar_asignaturas(self):
        asigs = EvaluacionController.listar_asignaturas()
        self.combo_asig['values'] = [f"{a['id_asignatura']} - {a['nombre']}" for a in asigs]
        if asigs:
            self.combo_asig.current(0)

    def _cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for e in EvaluacionController.listar_evaluaciones():
            self.tree.insert("", "end", values=(
                e['id_evaluacion'], e['nombre'], e['asignatura'],
                f"{e['ponderacion']}%", e['fecha']
            ))

    def _crear(self):
        try:
            id_asig = int(self.combo_asig.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Seleccione una asignatura.")
            return

        exito, msg = EvaluacionController.crear_evaluacion(
            id_asig, 1, self.e_nombre.get().strip(),
            self.e_pond.get().strip(), self.e_fecha.get().strip()
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.e_nombre.delete(0, "end")
            self.e_pond.delete(0, "end")
            self._cargar()
        else:
            messagebox.showerror("Error", msg)