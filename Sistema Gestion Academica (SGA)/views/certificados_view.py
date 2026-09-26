"""
Vista del módulo de Certificados - CU12.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.reporte_controller import ReporteController
from controllers.calificacion_controller import CalificacionController


class CertificadosView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(self.parent, text="🎓 Generación de Certificados de Notas",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        form = tk.LabelFrame(self.parent, text="Solicitar Certificado",
                             font=("Segoe UI", 11, "bold"), bg="#f1f5f9", padx=15, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Aprendiz:", bg="#f1f5f9").grid(row=0, column=0, sticky="w")
        self.combo_apre = ttk.Combobox(form, width=40, state="readonly")
        self.combo_apre.grid(row=0, column=1, padx=5)

        apres = CalificacionController.listar_aprendices()
        self.combo_apre['values'] = [f"{a['id_aprendiz']} - {a['nombre']}" for a in apres]
        if apres:
            self.combo_apre.current(0)

        tk.Button(form, text="🔍 Verificar y Generar", bg="#10b981", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._generar).grid(row=0, column=2, padx=10)

        self.resultado = tk.Text(self.parent, height=15, font=("Consolas", 11),
                                 bg="white", fg="#0f172a", padx=15, pady=15)
        self.resultado.pack(fill="both", expand=True, padx=20, pady=15)

    def _generar(self):
        try:
            id_apre = int(self.combo_apre.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Seleccione un aprendiz.")
            return

        exito, resultado = ReporteController.generar_certificado(id_apre)
        self.resultado.delete("1.0", "end")

        if not exito:
            self.resultado.insert("end", f"❌ CERTIFICADO DENEGADO\n\n{resultado}\n")
            return

        nombre = self.combo_apre.get().split(" - ")[1]
        texto = (
            f"╔══════════════════════════════════════════════════╗\n"
            f"║      CERTIFICADO ACADÉMICO OFICIAL - SGA         ║\n"
            f"╚══════════════════════════════════════════════════╝\n\n"
            f"  Aprendiz:        {nombre}\n"
            f"  Promedio:        {resultado['promedio']}\n"
            f"  Fecha emisión:   {resultado['fecha']}\n"
            f"  Código único:    {resultado['codigo']}\n\n"
            f"  ✅ Certificado verificado y aprobado.\n"
            f"  Este documento cuenta con código QR de autenticidad.\n"
        )
        self.resultado.insert("end", texto)