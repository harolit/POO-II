"""
Vista del módulo de Usuarios y Roles - CU08.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController


class UsuariosView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="🔐 Gestión de Usuarios y Roles",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Crear Usuario",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Nombre:", bg="#f1f5f9").grid(row=0, column=0, sticky="w")
        self.e_nombre = tk.Entry(form, width=25)
        self.e_nombre.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Email:", bg="#f1f5f9").grid(row=0, column=2, sticky="w")
        self.e_email = tk.Entry(form, width=25)
        self.e_email.grid(row=0, column=3, padx=5)

        tk.Label(form, text="Contraseña:", bg="#f1f5f9").grid(row=0, column=4, sticky="w")
        self.e_pass = tk.Entry(form, width=18, show="●")
        self.e_pass.grid(row=0, column=5, padx=5)

        tk.Label(form, text="Rol:", bg="#f1f5f9").grid(row=0, column=6, sticky="w")
        self.combo_rol = ttk.Combobox(form, width=18, state="readonly")
        self.combo_rol.grid(row=0, column=7, padx=5)

        roles = UsuarioController.listar_roles()
        self.combo_rol['values'] = [f"{r['id_rol']} - {r['nombre_rol']}" for r in roles]
        if roles:
            self.combo_rol.current(0)

        tk.Button(form, text="➕ Crear", bg="#0ea5e9", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._crear).grid(row=0, column=8, padx=10)

        cols = ("ID", "Nombre", "Email", "Rol", "Estado")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for u in UsuarioController.listar_usuarios():
            self.tree.insert("", "end", values=(
                u['id_usuario'], u['nombre'], u['email'],
                u['nombre_rol'], "Activo" if u['estado'] else "Inactivo"
            ))

    def _crear(self):
        try:
            id_rol = int(self.combo_rol.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Seleccione un rol.")
            return

        exito, msg = UsuarioController.crear_usuario(
            self.e_nombre.get(), self.e_email.get(),
            self.e_pass.get(), id_rol
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            for e in (self.e_nombre, self.e_email, self.e_pass):
                e.delete(0, "end")
            self._cargar()
        else:
            messagebox.showerror("Error", msg)