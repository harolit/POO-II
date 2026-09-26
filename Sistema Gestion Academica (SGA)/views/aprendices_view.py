"""
Vista del módulo de Aprendices - CU03.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.aprendiz_controller import AprendizController


class AprendicesView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="👥 Gestión de Aprendices",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Registrar Nuevo Aprendiz",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        campos = [("Nombre completo:", "e_nombre"), ("Correo:", "e_email"),
                  ("Documento:", "e_doc"), ("Ficha:", "e_ficha")]
        for i, (label, attr) in enumerate(campos):
            tk.Label(form, text=label, bg="#f1f5f9").grid(row=0, column=i*2, sticky="w", padx=5)
            entry = tk.Entry(form, width=22)
            entry.grid(row=0, column=i*2+1, padx=5)
            setattr(self, attr, entry)

        tk.Button(form, text="➕ Registrar", bg="#10b981", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._registrar).grid(row=0, column=8, padx=15)

        cols = ("ID", "Nombre", "Email", "Documento", "Ficha", "Estado")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for a in AprendizController.listar_aprendices():
            self.tree.insert("", "end", values=(
                a['id_aprendiz'], a['nombre'], a['email'],
                a['documento'], a['ficha'], a['estado']
            ))

    def _registrar(self):
        exito, msg = AprendizController.registrar_aprendiz(
            self.e_nombre.get(), self.e_email.get(),
            self.e_doc.get(), self.e_ficha.get()
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            for e in (self.e_nombre, self.e_email, self.e_doc, self.e_ficha):
                e.delete(0, "end")
            self._cargar()
        else:
            messagebox.showerror("Error", msg)