"""
Vista del módulo de Reportes - CU07.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.reporte_controller import ReporteController
import csv


class ReportesView:

    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self._construir_ui()
        self._cargar()

    def _construir_ui(self):
        tk.Label(self.parent, text="📊 Generación de Reportes Académicos",
                 font=("Segoe UI", 16, "bold"), bg="#f1f5f9", fg="#0f172a").pack(anchor="w", padx=20, pady=15)

        btn_frame = tk.Frame(self.parent, bg="#f1f5f9")
        btn_frame.pack(fill="x", padx=20)

        tk.Button(btn_frame, text="📥 Exportar a CSV (Excel)", bg="#10b981", fg="white",
                  font=("Segoe UI", 10, "bold"), command=self._exportar_csv).pack(side="left", padx=5)

        cols = ("Aprendiz", "Asignatura", "Evaluación", "Nota", "Ponderación")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=15)

    def _cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in ReporteController.generar_reporte_notas():
            self.tree.insert("", "end", values=(
                r['aprendiz'], r['asignatura'], r['evaluacion'],
                f"{r['nota']:.2f}", f"{r['ponderacion']}%"
            ))

    def _exportar_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="reporte_sga.csv"
        )
        if not filepath:
            return
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Aprendiz", "Asignatura", "Evaluación", "Nota", "Ponderación"])
                for r in ReporteController.generar_reporte_notas():
                    writer.writerow([r['aprendiz'], r['asignatura'], r['evaluacion'],
                                     r['nota'], r['ponderacion']])
            messagebox.showinfo("Éxito", f"Reporte exportado a:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")