"""
Vista del módulo de Calificaciones - CU05.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.calificacion_controller import CalificacionController


class CalificacionesView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(self.parent, text="📋 Registro de Calificaciones",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Registrar Calificación",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Evaluación:", bg="#f1f5f9").grid(row=0, column=0, sticky="w")
        self.combo_eval = ttk.Combobox(form, width=35, state="readonly")
        self.combo_eval.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Aprendiz:", bg="#f1f5f9").grid(row=0, column=2, sticky="w")
        self.combo_apre = ttk.Combobox(form, width=30, state="readonly")
        self.combo_apre.grid(row=0, column=3, padx=5)

        tk.Label(form, text="Nota (0-5):", bg="#f1f5f9").grid(row=0, column=4, sticky="w")
        self.e_nota = tk.Entry(form, width=10)
        self.e_nota.grid(row=0, column=5, padx=5)

        tk.Label(form, text="Observación:", bg="#f1f5f9").grid(row=0, column=6, sticky="w")
        self.e_obs = tk.Entry(form, width=25)
        self.e_obs.grid(row=0, column=7, padx=5)

        tk.Button(form, text="💾 Guardar", bg="#8b5cf6", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._guardar).grid(row=0, column=8, padx=10)

        self._cargar_combos()

    def _cargar_combos(self):
        evals = CalificacionController.listar_evaluaciones()
        self.combo_eval['values'] = [f"{e['id_evaluacion']} - {e['nombre']} ({e['asignatura']})" for e in evals]
        if evals:
            self.combo_eval.current(0)

        apres = CalificacionController.listar_aprendices()
        self.combo_apre['values'] = [f"{a['id_aprendiz']} - {a['nombre']}" for a in apres]
        if apres:
            self.combo_apre.current(0)

    def _guardar(self):
        try:
            id_eval = int(self.combo_eval.get().split(" - ")[0])
            id_apre = int(self.combo_apre.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Seleccione evaluación y aprendiz.")
            return

        exito, msg = CalificacionController.registrar_calificacion(
            id_eval, id_apre, self.e_nota.get(), self.e_obs.get()
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.e_nota.delete(0, "end")
            self.e_obs.delete(0, "end")
        else:
            messagebox.showerror("Error", msg)