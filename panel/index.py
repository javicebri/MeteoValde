import panel as pn
import param
from threading import Thread
import time

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

temperature = Temperature()
humidity = Humidity()
# pressure = Pressure()
# precipitation = Precipitation()
# wind = Wind()
# records = Records()
# prediction = Prediction()
# records = Records()
# distribution = Distribution()


ROUTES = {
    "temperatura": temperature.show(),
    "humedad": humidity.show(),
    # "presion": pressure.show(),
    # "precipitacion": precipitation.show(),
    # "viento": wind.show(),
    # "prediccion": prediction.show(),
    # "records": records.show(),
    # "distribucion": distribution.show()
}
pn.serve(ROUTES, port=5010, autoreload=True)