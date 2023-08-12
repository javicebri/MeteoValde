import panel as pn
import numpy as np
import matplotlib.pyplot as plt

class Humidity:
    def __init__(self):
        self.text_box = pn.widgets.FloatInput(value=0, step=1)
        self.boton = pn.widgets.Button(name="Mostrar número")
        self.etiqueta = pn.widgets.StaticText()
        self.plot = pn.pane.Matplotlib()

        self.boton.on_click(self.mostrar_numero)

        self.panel = pn.Column(self.text_box, self.boton, self.etiqueta, self.plot)

    def mostrar_numero(self, event):
        numero = float(self.text_box.value)
        self.etiqueta.value = f"Número ingresado: {numero}"

        # Generar datos para el plot
        x = np.linspace(0, 10, 100)
        y = np.sin(numero * x)

        # Actualizar el plot
        fig, ax = plt.subplots()
        ax.plot(x, y)
        self.plot.object = fig

    def show(self):
        return self.panel.servable()