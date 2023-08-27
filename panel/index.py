import panel as pn
import param
from threading import Thread
import time
from path_io import get_path_dict, load_data

from Temperature import Temperature
from Humidity import Humidity


pn.extension(sizing_mode="stretch_width")

class StreamClass(param.Parameterized):
    value = param.Integer()

class MessageQueue(param.Parameterized):
    value = param.List()

    def append(self, asof, user, message):
        if message:
            self.value = [*self.value, (asof, user, message)]

ACCENT_COLOR = "#0072B5"
DEFAULT_PARAMS = {
    "site": "Panel Climático de Valdepeñas de la Sierra",
    "accent_base_color": ACCENT_COLOR,
    "header_background": ACCENT_COLOR,
}

def fastlisttemplate(title, *objects):
    """Returns a Panel-AI version of the FastListTemplate

    Returns:
        [FastListTemplate]: A FastListTemplate
    """
    return pn.template.FastListTemplate(**DEFAULT_PARAMS, title=title, main=[pn.Column(*objects)])

def get_shared_state():
    if not "stream" in pn.state.cache:
        state=pn.state.cache["stream"]=StreamClass()
        pn.state.cache["messages"]=MessageQueue()

        def update_state():
            while True:
                if state.value==100:
                    state.value=0
                else:
                    state.value+=1
                time.sleep(1)

        Thread(target=update_state).start()

    return pn.state.cache["stream"], pn.state.cache["messages"]

def show_messages(messages):
    result = ""
    for message in messages:
        result = f"- {message[0]} | {message[1]}: {message[2]}\n" + result
    if not result:
        result = "No Messages yet!"
    return result


# def page2():
#     _, messages = get_shared_state()
#
#     ishow_messages = pn.bind(show_messages, messages=messages.param.value)
#     return fastlisttemplate("Show Messages", pn.panel(ishow_messages, height=600),)
#
# def page3():
#     stream, _ = get_shared_state()
#
#     return fastlisttemplate("Show Streaming Value",stream.param.value,)

root = "C:\\Users\\jc_ce\\Desktop\\01Proyectos\\Meteoclimatic\\MeteoValde"
path_dict = get_path_dict(root)

df_input_dict, df_input_trend_dict, df_input_res,\
    excel_compare_dict, excel_predict_dict, excel_stats_dict = load_data(path_dict)

temperature = Temperature(path_dict, df_input_dict['Temperature'], excel_stats_dict,
                          df_input_res, df_input_trend_dict['Temperature'])

humidity = Humidity()
# pressure = Pressure()
# precipitation = Precipitation()
# wind = Wind()
# records = Records()
# prediction = Prediction()
# records = Records()
# distribution = Distribution()


# ROUTES = {
#     "temperatura": temperature.show(),
#     "humedad": humidity.show(),
#     # "presion": pressure.show(),
#     # "precipitacion": precipitation.show(),
#     # "viento": wind.show(),
#     # "prediccion": prediction.show(),
#     # "records": records.show(),
#     # "distribucion": distribution.show()
# }
# pn.serve(ROUTES, port=5010, autoreload=True)



# Definir las funciones que muestran los contenidos de temperatura y humedad
def show_temperature():
    return pn.pane.Markdown("Contenido de temperatura")

def show_humidity():
    return pn.pane.Markdown("Contenido de humedad")

# Crear enlaces con iconos y texto usando HTML
# temperature_link = '<a href="/temperatura" style="display: flex; align-items: center;"><img src="C:\\Users\\jc_ce\\Desktop\\01Proyectos\\Meteoclimatic\\MeteoValde\\resources\\termometro.png" alt="Temperatura" style="margin-right: 100px;">Temperatura</a>'
# humidity_link = '<a href="/humedad" style="display: flex; align-items: center;"><img src="icons/humidity.png" alt="Humedad" style="margin-right: 10px;">Humedad</a>'
# temperature_link = f'<a href="/temperatura" style="display: flex; align-items: center;"><img src="data:image/png;base64,C:\\Users\\jc_ce\\Desktop\\01Proyectos\\Meteoclimatic\\MeteoValde\\resources\\termometro.png" alt="Temperatura" style="margin-right: 10px;">Temperatura</a>'


# # Crear paneles de imágenes para los enlaces
# temperature_link = pn.pane.Image("C:/Users/jc_ce/Desktop/01Proyectos/Meteoclimatic/MeteoValde/resources/termometro.png", width=100, height=100)
# humidity_link = pn.pane.Image("C:/Users/jc_ce/Desktop/01Proyectos/Meteoclimatic/MeteoValde/resources/termometro.png", width=100, height=100)
#
# temperature_link = pn.widgets.Link(name="Enlace con ícono", icon="C:/Users/jc_ce/Desktop/01Proyectos/Meteoclimatic/MeteoValde/resources/termometro.png", url="https://www.ejemplo.com")
# humidity_link = pn.widgets.Link(name="Enlace con imagen", image="C:/Users/jc_ce/Desktop/01Proyectos/Meteoclimatic/MeteoValde/resources/termometro.png", url="https://www.ejemplo.com")


# # Crear un panel con Markdown y HTML para agregar enlaces con iconos e imágenes
# html = """
# <h1>Ejemplo de enlaces personalizados</h1>
#
# <a href="https://www.ejemplo.com">Enlace con ícono <i class="fa fa-check"></i></a>
# <br>
# <a href="https://www.ejemplo.com">Enlace con imagen <img src="https://www.ejemplo.com/imagen.jpg" alt="Imagen"></a>
# """
#
# # Crear un widget Markdown
# temperature_link = pn.pane.HTML(html)
# humidity_link = pn.pane.HTML(html)


logo_temperature = pn.panel('C:\\Users\\jc_ce\\Desktop\\01Proyectos\\Meteoclimatic\\MeteoValde\\resources\\termometro.png', height=50)

# Crear el diccionario de rutas con enlaces personalizados
ROUTES = {
    "Temperatura": temperature.show(),
    "Humedad": humidity.show(),
}

pn.serve(ROUTES, port=5010, autoreload=True)
# # Crear un panel con los enlaces
# links_panel = pn.Column(
#     pn.pane.Markdown("# Panel de Enlaces"),
#     pn.panel(temperature_link, width=300),
#     pn.panel(humidity_link, width=300)
# )

# Combinar el panel de enlaces y el panel de rutas en una disposición
# app_layout = pn.Row(links_panel, pn.serve(ROUTES, port=5010, autoreload=True))

# Mostrar la aplicación completa
# app_layout.servable()