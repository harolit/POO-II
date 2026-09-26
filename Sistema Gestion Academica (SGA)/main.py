"""
SGA - Sistema de Gestión Académica
Punto de entrada principal de la aplicación.
"""
import tkinter as tk
from tkinter import messagebox

from database import init_database
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.planes_view import PlanesView
from views.aprendices_view import AprendicesView
from views.evaluaciones_view import EvaluacionesView
from views.calificaciones_view import CalificacionesView
from views.asistencia_view import AsistenciaView
from views.historial_view import HistorialView
from views.reportes_view import ReportesView
from views.usuarios_view import UsuariosView
from views.notificaciones_view import NotificacionesView
from views.certificados_view import CertificadosView


class SGAApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SGA - Sistema de Gestión Académica Integral")
        self.root.geometry("1280x760")
        self.root.configure(bg="#f1f5f9")
        self.usuario_actual = None
        self._mostrar_login()

    # ---------- LOGIN ----------
    def _mostrar_login(self):
        self._limpiar()
        self.root.geometry("500x450")
        LoginView(self.root, self._on_login)

    def _on_login(self, datos_usuario):
        self.usuario_actual = datos_usuario
        self._mostrar_app_principal()

    # ---------- APP PRINCIPAL ----------
    def _mostrar_app_principal(self):
        self._limpiar()
        self.root.geometry("1280x760")

        # Barra lateral
        sidebar = tk.Frame(self.root, bg="#0f172a", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🎓 SGA", font=("Segoe UI", 20, "bold"),
                 bg="#0f172a", fg="#38bdf8").pack(pady=20)
        tk.Label(sidebar, text=self.usuario_actual['nombre'],
                 font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8").pack()
        tk.Label(sidebar, text=f"({self.usuario_actual['rol']})",
                 font=("Segoe UI", 9, "italic"), bg="#0f172a", fg="#64748b").pack(pady=(0, 20))

        # Botones de navegación según módulos
        modulos = [
            ("📊 Dashboard", self._vista_dashboard),
            ("📚 Planes de Estudio", self._vista_planes),
            ("👥 Aprendices", self._vista_aprendices),
            ("📝 Evaluaciones", self._vista_evaluaciones),
            ("📋 Calificaciones", self._vista_calificaciones),
            ("🗓 Asistencia", self._vista_asistencia),
            ("📖 Historial Académico", self._vista_historial),
            ("📊 Reportes", self._vista_reportes),
            ("🔐 Usuarios y Roles", self._vista_usuarios),
            ("📧 Notificaciones", self._vista_notificaciones),
            ("🎓 Certificados", self._vista_certificados),
        ]
        for texto, comando in modulos:
            tk.Button(sidebar, text=texto, font=("Segoe UI", 10), bg="#1e293b", fg="#e2e8f0",
                      relief="flat", anchor="w", padx=15, pady=8, cursor="hand2",
                      activebackground="#0ea5e9", activeforeground="white",
                      command=comando).pack(fill="x", pady=1)

        # Botón cerrar sesión
        tk.Button(sidebar, text="🚪 Cerrar Sesión", font=("Segoe UI", 10, "bold"),
                  bg="#dc2626", fg="white", relief="flat", pady=8, cursor="hand2",
                  command=self._cerrar_sesion).pack(side="bottom", fill="x", pady=10)

        # Contenedor principal
        self.contenedor = tk.Frame(self.root, bg="#f1f5f9")
        self.contenedor.pack(side="right", fill="both", expand=True)

        self._vista_dashboard()

    def _limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _limpiar_contenedor(self):
        for w in self.contenedor.winfo_children():
            w.destroy()

    # ---------- VISTAS ----------
    def _vista_dashboard(self):
        self._limpiar_contenedor()
        DashboardView(self.contenedor, self.usuario_actual)

    def _vista_planes(self):
        self._limpiar_contenedor()
        PlanesView(self.contenedor, self.usuario_actual)

    def _vista_aprendices(self):
        self._limpiar_contenedor()
        AprendicesView(self.contenedor, self.usuario_actual)

    def _vista_evaluaciones(self):
        self._limpiar_contenedor()
        EvaluacionesView(self.contenedor, self.usuario_actual)

    def _vista_calificaciones(self):
        self._limpiar_contenedor()
        CalificacionesView(self.contenedor, self.usuario_actual)

    def _vista_asistencia(self):
        self._limpiar_contenedor()
        AsistenciaView(self.contenedor, self.usuario_actual)

    def _vista_historial(self):
        self._limpiar_contenedor()
        HistorialView(self.contenedor, self.usuario_actual)

    def _vista_reportes(self):
        self._limpiar_contenedor()
        ReportesView(self.contenedor, self.usuario_actual)

    def _vista_usuarios(self):
        self._limpiar_contenedor()
        UsuariosView(self.contenedor, self.usuario_actual)

    def _vista_notificaciones(self):
        self._limpiar_contenedor()
        NotificacionesView(self.contenedor, self.usuario_actual)

    def _vista_certificados(self):
        self._limpiar_contenedor()
        CertificadosView(self.contenedor, self.usuario_actual)

    # ---------- SESIÓN ----------
    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar la sesión actual?"):
            self.usuario_actual = None
            self._mostrar_login()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # Inicializar base de datos (crea tablas y datos demo si es primera vez)
    init_database()
    app = SGAApp()
    app.run()