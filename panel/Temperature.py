import panel as pn
import numpy as np
import matplotlib.pyplot as plt

class Temperature:
    def __init__(self):
        self.latitud_box = pn.widgets.FloatInput(value=0, step=0.001, name="Latitud")
        self.longitud_box = pn.widgets.FloatInput(value=0, step=0.001, name="Longitud")
        self.boton = pn.widgets.Button(name="Mostrar en mapa")
        self.mapa = pn.pane.HTML()

        self.boton.on_click(self.mostrar_en_mapa)

        self.panel = pn.Column(self.latitud_box, self.longitud_box, self.boton, self.mapa)

    def mostrar_en_mapa(self, event):
        latitud = self.latitud_box.value
        longitud = self.longitud_box.value

        # Crear el mapa de Folium
        mapa_folium = folium.Map(location=[latitud, longitud], zoom_start=12)

        # Agregar un marcador en las coordenadas ingresadas
        folium.Marker(location=[latitud, longitud], popup="Ubicación").add_to(mapa_folium)

        # Generar el HTML del mapa y mostrarlo en el panel
        mapa_html = mapa_folium._repr_html_()
        self.mapa.object = mapa_html

    def show(self):
        return self.panel.servable()