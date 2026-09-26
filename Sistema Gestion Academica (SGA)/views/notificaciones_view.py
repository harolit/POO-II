"""
Vista del módulo de Notificaciones - CU11.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from controllers.usuario_controller import UsuarioController
from datetime import datetime


class NotificacionesView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="📧 Envío de Notificaciones Académicas",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Nueva Notificación",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Destinatario:", bg="#f1f5f9").grid(row=0, column=0, sticky="w")
        self.combo_user = ttk.Combobox(form, width=30, state="readonly")
        self.combo_user.grid(row=0, column=1, padx=5)

        usuarios = UsuarioController.listar_usuarios()
        self.combo_user['values'] = [f"{u['id_usuario']} - {u['nombre']}" for u in usuarios]
        if usuarios:
            self.combo_user.current(0)

        tk.Label(form, text="Mensaje:", bg="#f1f5f9").grid(row=0, column=2, sticky="w")
        self.e_msg = tk.Entry(form, width=45)
        self.e_msg.grid(row=0, column=3, padx=5)

        tk.Button(form, text="📤 Enviar", bg="#8b5cf6", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._enviar).grid(row=0, column=4, padx=10)

        cols = ("ID", "Destinatario", "Mensaje", "Fecha", "Leído")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT n.id_notificacion, u.nombre, n.mensaje, n.fecha_envio, n.leido
            FROM notificacion n JOIN usuario u ON n.id_usuario = u.id_usuario
            ORDER BY n.fecha_envio DESC
        """)
        for r in cursor.fetchall():
            self.tree.insert("", "end", values=(
                r['id_notificacion'], r['nombre'], r['mensaje'],
                r['fecha_envio'], "Sí" if r['leido'] else "No"
            ))
        conn.close()

    def _enviar(self):
        try:
            id_user = int(self.combo_user.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Seleccione destinatario.")
            return
        msg = self.e_msg.get().strip()
        if not msg:
            messagebox.showwarning("Aviso", "Escriba un mensaje.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notificacion (id_usuario, mensaje, fecha_envio)
            VALUES (?, ?, ?)
        """, (id_user, msg, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Notificación enviada.")
        self.e_msg.delete(0, "end")
        self._cargar()