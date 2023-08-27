import panel as pn
import param
from threading import Thread
import time

from path_io import get_path_dict, load_data

from Temperature import Temperature
from Pressure import Pressure
from Humidity import Humidity
from Precipitation import Precipitation


pn.extension(sizing_mode="stretch_width")

class StreamClass(param.Parameterized):
    value = param.Integer()

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

root = "C:\\Users\\jc_ce\\Desktop\\01Proyectos\\Meteoclimatic\\MeteoValde"
path_dict = get_path_dict(root)

df_input_dict, df_input_trend_dict, df_input_res,\
    excel_compare_dict, excel_predict_dict, excel_stats_dict = load_data(path_dict)

temperature = Temperature(path_dict,
                          df_input_dict['Temperature'],
                          excel_stats_dict,
                          df_input_res,
                          df_input_trend_dict['Temperature'])

humidity = Humidity(path_dict,
                    df_input_dict['Humidity'],
                    excel_stats_dict,
                    df_input_res,
                    df_input_trend_dict['Humidity'])

pressure = Pressure(path_dict,
                    df_input_dict['Pressure'],
                    excel_stats_dict,
                    df_input_res,
                    df_input_trend_dict['Pressure'])

precipitation = Precipitation(path_dict,
                    df_input_dict['Precipitation'],
                    excel_stats_dict,
                    df_input_res,
                    df_input_trend_dict['Precipitation'])
# wind = Wind()
# records = Records()
# prediction = Prediction()
# records = Records()
# distribution = Distribution()

def show_temperature():
    return pn.pane.Markdown("Contenido de temperatura")
def show_pressure():
    return pn.pane.Markdown("Contenido de presión")
def show_humidity():
    return pn.pane.Markdown("Contenido de humedad")

logo_temperature = pn.panel('C:\\Users\\jc_ce\\Desktop\\01Proyectos\\Meteoclimatic\\MeteoValde\\resources\\termometro.png', height=50)

# Crear el diccionario de rutas con enlaces personalizados
ROUTES = {
    "Temperatura": temperature.show(),
    "Presion": pressure.show(),
    "Humedad": humidity.show(),
    "Precipitacion": precipitation.show()
}

pn.serve(ROUTES, port=5010, autoreload=True)