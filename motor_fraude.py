"""Motor de inferencia por encadenamiento hacia adelante para detectar fraude."""

import tkinter as tk
from tkinter import messagebox, ttk


def motor_inferencia(hechos_iniciales, reglas, traza=None):
    """Aplica reglas hasta que no sea posible deducir hechos nuevos."""
    hechos = dict(hechos_iniciales)
    hubo_nuevos_hechos = True

    while hubo_nuevos_hechos:
        hubo_nuevos_hechos = False

        for regla in reglas:
            condiciones_cumplidas = all(
                hechos.get(nombre) == valor
                for nombre, valor in regla["condiciones"].items()
            )
            conclusion = regla["conclusion"]
            nombre_conclusion, valor_conclusion = next(iter(conclusion.items()))

            if condiciones_cumplidas and hechos.get(nombre_conclusion) != valor_conclusion:
                hechos[nombre_conclusion] = valor_conclusion
                hubo_nuevos_hechos = True
                mensaje = (
                    f'{regla["id"]} -> '
                    f"{nombre_conclusion} = {valor_conclusion}"
                )
                if traza is not None:
                    traza.append(mensaje)
                else:
                    print(mensaje)

    return hechos


# Hechos conocidos al iniciar la detección.
datos_transaccion = {
    "monto": 6500,
    "pais_extranjero": True,
    "hora_inusual": True,
    "cliente_desconoce": True,
}

hechos_iniciales = {
    **datos_transaccion,
    "monto_alto": datos_transaccion["monto"] > 5000,
}


# Las reglas representan implicaciones y se ejecutan mediante encadenamiento.
reglas = [
    {
        "id": "R1",
        "condiciones": {"monto_alto": True},
        "conclusion": {"transaccion_inusual": True},
    },
    {
        "id": "R2",
        "condiciones": {"transaccion_inusual": True, "pais_extranjero": True},
        "conclusion": {"riesgo_alto": True},
    },
    {
        "id": "R3",
        "condiciones": {"riesgo_alto": True, "cliente_desconoce": True},
        "conclusion": {"bloquear_tarjeta": True},
    },
    {
        "id": "R4",
        "condiciones": {"hora_inusual": True, "transaccion_inusual": True},
        "conclusion": {"generar_alerta": True},
    },
]


class AplicacionFraude(tk.Tk):
    """Interfaz de escritorio para ejecutar el motor de inferencia."""

    def __init__(self):
        super().__init__()
        self.title("Motor de Fraude Bancario")
        self.geometry("760x570")
        self.minsize(680, 500)
        self.configure(bg="#f4f6f8")
        self._crear_variables()
        self._crear_interfaz()

    def _crear_variables(self):
        self.monto = tk.StringVar(value="6500")
        self.pais_extranjero = tk.BooleanVar(value=True)
        self.hora_inusual = tk.BooleanVar(value=True)
        self.cliente_desconoce = tk.BooleanVar(value=True)
        self.resultado = tk.StringVar(value="Pendiente de análisis")

    def _crear_interfaz(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"), foreground="#17324d")
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10), foreground="#52606d")
        estilo.configure("Resultado.TLabel", font=("Segoe UI", 17, "bold"), padding=12)

        contenedor = ttk.Frame(self, padding=24)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(4, weight=1)

        ttk.Label(contenedor, text="Motor de Fraude Bancario", style="Titulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(
            contenedor,
            text="Analiza una transacción mediante encadenamiento hacia adelante.",
            style="Subtitulo.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 20))

        datos = ttk.LabelFrame(contenedor, text="Datos de la transacción", padding=14)
        datos.grid(row=2, column=0, columnspan=2, sticky="ew")
        datos.columnconfigure(1, weight=1)
        ttk.Label(datos, text="Monto:").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=5)
        ttk.Entry(datos, textvariable=self.monto, width=20).grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Checkbutton(datos, text="País extranjero", variable=self.pais_extranjero).grid(
            row=1, column=0, sticky="w", pady=5
        )
        ttk.Checkbutton(datos, text="Hora inusual", variable=self.hora_inusual).grid(
            row=1, column=1, sticky="w", pady=5
        )
        ttk.Checkbutton(datos, text="Cliente desconoce la operación", variable=self.cliente_desconoce).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=5
        )

        ttk.Button(contenedor, text="Analizar transacción", command=self.analizar).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=18
        )

        salida = ttk.LabelFrame(contenedor, text="Traza del motor", padding=10)
        salida.grid(row=4, column=0, columnspan=2, sticky="nsew")
        salida.columnconfigure(0, weight=1)
        salida.rowconfigure(0, weight=1)
        self.texto_salida = tk.Text(
            salida, height=12, wrap="word", state="disabled", font=("Consolas", 10),
            background="#ffffff", foreground="#263238", relief="flat", padx=10, pady=8,
        )
        self.texto_salida.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(salida, orient="vertical", command=self.texto_salida.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.texto_salida.configure(yscrollcommand=barra.set)

        self.etiqueta_resultado = ttk.Label(
            contenedor, textvariable=self.resultado, style="Resultado.TLabel", anchor="center"
        )
        self.etiqueta_resultado.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(14, 0))

    def analizar(self):
        try:
            monto = float(self.monto.get().replace(",", "."))
            if monto < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato inválido", "Ingresa un monto numérico mayor o igual a cero.")
            return

        datos = {
            "monto": monto,
            "pais_extranjero": self.pais_extranjero.get(),
            "hora_inusual": self.hora_inusual.get(),
            "cliente_desconoce": self.cliente_desconoce.get(),
        }
        hechos = {**datos, "monto_alto": monto > 5000}
        traza = []
        memoria_final = motor_inferencia(hechos, reglas, traza)

        lineas = ["Hechos iniciales:"]
        lineas.extend(f"  {nombre} = {valor}" for nombre, valor in hechos.items())
        lineas.append("\nReglas activadas:")
        lineas.extend(f"  {paso}" for paso in traza)
        lineas.append("\nMemoria final:")
        lineas.extend(f"  {nombre} = {valor}" for nombre, valor in memoria_final.items())
        self._mostrar_salida("\n".join(lineas))

        bloqueada = memoria_final.get("bloquear_tarjeta", False)
        self.resultado.set("BLOQUEAR TARJETA" if bloqueada else "TRANSACCIÓN NO BLOQUEADA")
        self.etiqueta_resultado.configure(foreground="#b42318" if bloqueada else "#137333")

    def _mostrar_salida(self, contenido):
        self.texto_salida.configure(state="normal")
        self.texto_salida.delete("1.0", tk.END)
        self.texto_salida.insert("1.0", contenido)
        self.texto_salida.configure(state="disabled")


if __name__ == "__main__":
    AplicacionFraude().mainloop()
