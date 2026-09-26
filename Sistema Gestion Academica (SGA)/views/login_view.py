"""
Vista de Inicio de Sesión - CU01.
"""
import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController


class LoginView:

    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("SGA - Inicio de Sesión")
        self.root.geometry("500x450")
        self.root.configure(bg="#1e293b")
        self.root.resizable(False, False)

        self._construir_ui()

    def _construir_ui(self):
        # Encabezado
        tk.Label(self.root, text="🎓 SGA", font=("Segoe UI", 32, "bold"),
                 bg="#1e293b", fg="#38bdf8").pack(pady=(30, 5))
        tk.Label(self.root, text="Sistema de Gestión Académica",
                 font=("Segoe UI", 12), bg="#1e293b", fg="#94a3b8").pack()

        # Marco central
        frame = tk.Frame(self.root, bg="#334155", padx=30, pady=30)
        frame.pack(pady=30, padx=40, fill="both")

        tk.Label(frame, text="Correo institucional", font=("Segoe UI", 10),
                 bg="#334155", fg="#cbd5e1").pack(anchor="w")
        self.entry_email = tk.Entry(frame, font=("Segoe UI", 11), width=35)
        self.entry_email.pack(pady=(2, 12), ipady=4)
        self.entry_email.insert(0, "admin@sga.edu.co")

        tk.Label(frame, text="Contraseña", font=("Segoe UI", 10),
                 bg="#334155", fg="#cbd5e1").pack(anchor="w")
        self.entry_password = tk.Entry(frame, font=("Segoe UI", 11), width=35, show="●")
        self.entry_password.pack(pady=(2, 12), ipady=4)
        self.entry_password.insert(0, "admin123")

        btn = tk.Button(frame, text="INICIAR SESIÓN", font=("Segoe UI", 11, "bold"),
                        bg="#0ea5e9", fg="white", relief="flat", cursor="hand2",
                        command=self._login)
        btn.pack(pady=10, ipadx=20, ipady=6)

        # Info de credenciales demo
        tk.Label(self.root, text="Demo: admin@sga.edu.co / admin123",
                 font=("Segoe UI", 9), bg="#1e293b", fg="#64748b").pack(side="bottom", pady=10)

        self.root.bind('<Return>', lambda e: self._login())

    def _login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        if not email or not password:
            messagebox.showwarning("Campos vacíos", "Ingrese correo y contraseña.")
            return

        exito, mensaje, datos = AuthController.login(email, password)
        if exito:
            messagebox.showinfo("Bienvenido", f"{mensaje}\nRol: {datos['rol']}")
            self.on_login_success(datos)
        else:
            messagebox.showerror("Error de autenticación", mensaje)