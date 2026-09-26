"""
Vista del módulo de Planes de Estudio - CU02.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.plan_controller import PlanController


class PlanesView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar_planes()

    def _construir_ui(self):
        tk.Label(self.parent, text="📚 Gestión de Planes de Estudio",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        # Formulario
        form = tk.LabelFrame(self.parent, text="Nuevo Plan de Estudio",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Código:", bg="#f1f5f9").grid(row=0, column=0, sticky="w", pady=5)
        self.e_codigo = tk.Entry(form, width=25)
        self.e_codigo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Nombre:", bg="#f1f5f9").grid(row=0, column=2, sticky="w", pady=5)
        self.e_nombre = tk.Entry(form, width=35)
        self.e_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Versión:", bg="#f1f5f9").grid(row=0, column=4, sticky="w", pady=5)
        self.e_version = tk.Entry(form, width=10)
        self.e_version.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(form, text="➕ Registrar Plan", bg="#0ea5e9", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._crear_plan).grid(
            row=0, column=6, padx=15)

        # Tabla
        cols = ("ID", "Código", "Nombre", "Versión", "Fecha")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _cargar_planes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in PlanController.listar_planes():
            self.tree.insert("", "end", values=(
                p['id_plan'], p['codigo_plan'], p['nombre_plan'],
                p['version'], p['fecha_creacion']
            ))

    def _crear_plan(self):
        codigo = self.e_codigo.get().strip()
        nombre = self.e_nombre.get().strip()
        version = self.e_version.get().strip()
        exito, msg = PlanController.crear_plan(codigo, nombre, version)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.e_codigo.delete(0, "end")
            self.e_nombre.delete(0, "end")
            self.e_version.delete(0, "end")
            self._cargar_planes()
        else:
            messagebox.showerror("Error", msg)