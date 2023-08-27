
input_name = 'ESCLM1900000019184A.csv'
input_trend_name = 'ESCLM1900000019184A_trend.csv'
input_res_name = 'ESCLM1900000019184A_res.csv'
input_stats_name = 'ESCLM1900000019184A_stats.xlsx'
input_compare_name = 'ESCLM1900000019184A_compare.xlsx'
input_predict_name = 'ESCLM1900000019184A_predict.xlsx'

unit_dict = {
    'T. Max.': '[ºC]',
    'T. Min.': '[ºC]',
    'H. Max.': '[%]',
    'H. Min.': '[%]',
    'P. Max.': '[hPa]',
    'P. Min.': '[hPa]',
    'Vel.': '[Km/h]',
    'Precipitación': '[l/m2]'
}

input_variable_groups = {
    'Temperature': ['date', 'T. Max.', 'T. Min.', 'T. med1.', 'T. Amp.'],
    'Humidity': ['date', 'H. Max.', 'H. Min.', 'H. med1.', 'H. Amp.'],
    'Pressure': ['date', 'P. Max.', 'P. Min.', 'P. med1.', 'P. Amp.'],
    'Wind': ['date', 'Vel.'],
    'Precipitation': ['date', 'Precipitación']
}

trend_variable_groups = {
    'Temperature': ['date', 'T. Max.', 'T. Min.', 'T. med1.', 'T. Amp.',
                    'Regresión T. Max.', 'Regresión T. Min.',
                    'Regresión T. med1.', 'Regresión T. Amp.'],
    'Humidity': ['date', 'H. Max.', 'H. Min.', 'H. med1.', 'H. Amp.'],
    'Pressure': ['date', 'P. Max.', 'P. Min.', 'P. med1.', 'P. Amp.'],
    'Wind': ['date', 'Vel.'],
    'Precipitation': ['date', 'Precipitación', 'Cuenta_lluvia', 'Cuenta_sequía']
}

logo_temperature = 'termometro.png'