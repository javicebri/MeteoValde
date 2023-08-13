import holoviews as hv
import colorcet as cc
from holoviews import dim, opts
import numpy as np
N = 100
x = np.random.normal(size=N)
y = np.random.normal(size=N)
hv.Points((x, y))
import pandas as pd
import datetime
import os
import hvplot.pandas
import panel as pn
# import xlrd
# import datashader
# from bokeh.models.formatters import DatetimeTickFormatter
pn.extension('tabulator', css_files=[pn.io.resources.CSS_URLS['font-awesome']])
hv.extension('bokeh')

class Temperature:
    def __init__(self, path_dict, df_input, excel_stats_dict):
        self.df = df_input.copy()
        self.excel_stats_dict = excel_stats_dict

        self.df.index = pd.to_datetime(self.df.index)
    def contains_filter(df, lower, upper, column, df_ref):
        df_ref_filtered = df_ref[(df_ref.index >= lower) & (df_ref.index <= upper)]
        df.loc['Media td1 mínima rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. med1.'].min()
        df.loc['Media td1 mínima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. med1.'].idxmin()
        df.loc['Media td1 máxima rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. med1.'].max()
        df.loc['Media td1 máxima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. med1.'].idxmax()
        df.loc['Mínima rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. Min.'].min()
        df.loc['Mínima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. Min.'].idxmin()
        df.loc['Mínima Max. rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. Min.'].max()
        df.loc['Mínima Max. rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. Min.'].idxmax()
        df.loc['Máxima rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. Max.'].max()
        df.loc['Máxima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. Max.'].idxmax()
        df.loc['Máxima Min. rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. Max.'].min()
        df.loc['Máxima Min. rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. Max.'].idxmin()
        df.loc['Min. amplitud rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. Amp.'].min()
        df.loc['Min. amplitud rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. Amp.'].idxmin()
        df.loc['Max. amplitud rel. (Rango sel.)', 'Temperatura [ºC]'] = df_ref_filtered['T. Amp.'].max()
        df.loc['Max. amplitud rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['T. Amp.'].idxmax()

        return df
    def show_panel(self):
        date_subrange_temp = pn.widgets.DateRangeSlider(name='Date',
                                                        start=self.df.index[0],
                                                        end=self.df.index[-1])

        subset_dfi_temp = self.df.interactive(sizing_mode='stretch_width')
        filtered_subrange_temp = subset_dfi_temp[
            (subset_dfi_temp.index >= date_subrange_temp.param.value_start) &
            (subset_dfi_temp.index <= date_subrange_temp.param.value_end)]

        init_date = filtered_subrange_temp.index[0]
        end_date = self.df.index[-1]

        temperature_med1_chart = filtered_subrange_temp.hvplot(y=['T. med1.'], kind='line', ylabel='Temperatura [ºC]',
                                                               xlabel='Fecha',
                                                               title='Temperaturas medias Td1 = (MIN + MAX)/2 diaria [ºC]').opts(
            xrotation=45)
        temperature_maxmin_chart = filtered_subrange_temp.hvplot(y=['T. Min.', 'T. Max.'], kind='line',
                                                                 ylabel='Temperatura [ºC]', xlabel='Fecha',
                                                                 title='Temperaturas máximas y mínimas por día [ºC]').opts(
            legend_position='top_right', xrotation=45)
        temperature_ampl_chart = filtered_subrange_temp.hvplot(y=['T. Amp.'], kind='line', ylabel='Temperatura [ºC]',
                                                               xlabel='Fecha', title='Amplitud térmica por día [ºC]',
                                                               color='y').opts(xrotation=45)

        ### TEMPERATURA TABLA RECORDS
        temperature_table_title_rel = pn.panel('#### Records relativos')
        temperature_table_title_abs = pn.panel('#### Records absolutos')
        temperature_table_text = pn.panel(
            '*** Los valores presentados correspondenden al rango de fechas seleccionado con los cursores anteriores.***')

        subset_dfi_temp = self.df.interactive(sizing_mode='stretch_width')
        df_stats_rel_temp = pd.DataFrame(
            {'Estadísticas': ['Media td1 mínima rel. (Rango sel.)', 'Media td1 máxima rel. (Rango sel.)',
                              'Mínima rel. (Rango sel.)', 'Mínima Max. rel. (Rango sel.)',
                              'Máxima rel. (Rango sel.)', 'Máxima Min. rel. (Rango sel.)',
                              'Min. amplitud rel. (Rango sel.)', 'Max. amplitud rel. (Rango sel.)'],
             'Fecha': [0, 0, 0, 0, 0, 0, 0, 0],
             'Temperatura [ºC]': [0, 0, 0, 0, 0, 0, 0, 0]})

        df_stats_rel_temp = df_stats_rel_temp.set_index('Estadísticas')
        df_out_table_rel_temp = pn.widgets.Tabulator(df_stats_rel_temp, layout='fit_data_table')

        df_out_table_rel_temp.add_filter(pn.bind(self.contains_filter, lower=date_subrange_temp.param.value_start,
                                                 upper=date_subrange_temp.param.value_end, column='T. Min.',
                                                 df_ref=self.df))

        self.excel_stats_dict['stats_temp'] = self.excel_stats_dict['stats_temp'].set_index('Estadísticas')
        self.excel_stats_dict['stats_temp']['Fecha'] = self.excel_stats_dict['stats_temp']['Fecha'].dt.strftime('%Y-%m-%d')

        df_out_table_abs_temp = pn.widgets.Tabulator(self.excel_stats_dict['stats_temp'], layout='fit_data_table')

        ### TEMPERATURA TABLA RESUMEN Y HEATMAP
        df_input_med1_temp = pd.read_excel(input_stats_name, sheet_name='T. med1. mes', index_col=[0])
        df_input_max_temp = pd.read_excel(input_stats_name, sheet_name='T. Max. mes', index_col=[0])
        df_input_min_temp = pd.read_excel(input_stats_name, sheet_name='T. Min. mes', index_col=[0])
        temperature_table_med1_text = pn.panel('### Temperatura media td1 media por mes [ºC]')
        temperature_table_max_text = pn.panel('### Temperatura máxima media por mes [ºC]')
        temperature_table_min_text = pn.panel('### Temperatura mínima media por mes [ºC]')
        df_table_med1_temp = pn.widgets.Tabulator(df_input_med1_temp, width=800,
                                                  selection=[df_input_med1_temp.shape[0] - 1])
        df_table_max_temp = pn.widgets.Tabulator(df_input_max_temp, width=800,
                                                 selection=[df_input_max_temp.shape[0] - 1])
        df_table_min_temp = pn.widgets.Tabulator(df_input_min_temp, width=800,
                                                 selection=[df_input_min_temp.shape[0] - 1])

        points = [(df_input_med1_temp.columns.tolist()[i], df_input_med1_temp.index.tolist()[j],
                   df_input_med1_temp.iloc[j, i]) for i in range(12) for j in range(10)]
        heatmap_med1_temp = hv.HeatMap(points)
        (heatmap_med1_temp).opts(
            opts.HeatMap(toolbar='above', tools=['hover']),
            opts.Points(tools=['hover'], size=dim('z') * 0.3)).opts(colorbar=True, xlabel='Mes', ylabel='Año',
                                                                    width=500, height=400)
        heatmap_med1_temp = hv.Layout(
            [heatmap_med1_temp.relabel('Temp Media td1. media [ºC]').opts(cmap=c) for c in ['coolwarm']])

        points = [
            (df_input_max_temp.columns.tolist()[i], df_input_max_temp.index.tolist()[j], df_input_max_temp.iloc[j, i])
            for i in range(12) for j in range(10)]
        heatmap_max_temp = hv.HeatMap(points)
        (heatmap_max_temp).opts(
            opts.HeatMap(toolbar='above', tools=['hover']),
            opts.Points(tools=['hover'], size=dim('z') * 0.3)).opts(colorbar=True, xlabel='Mes', ylabel='Año',
                                                                    width=500, height=400)
        heatmap_max_temp = hv.Layout([heatmap_max_temp.relabel('Temp Max. media [ºC]').opts(cmap=c) for c in ['Reds']])

        points = [
            (df_input_min_temp.columns.tolist()[i], df_input_min_temp.index.tolist()[j], df_input_min_temp.iloc[j, i])
            for i in range(12) for j in range(10)]
        heatmap_min_temp = hv.HeatMap(points)
        (heatmap_min_temp).opts(
            opts.HeatMap(toolbar='above', tools=['hover']),
            opts.Points(tools=['hover'], size=dim('z') * 0.3)).opts(colorbar=True, xlabel='Mes', ylabel='Año',
                                                                    width=500, height=400)
        heatmap_min_temp = hv.Layout(
            [heatmap_min_temp.relabel('Temp Min. media [ºC]').opts(cmap=list(reversed(cc.blues)))])

        temperature_trend_title = pn.panel('### Tendencias')
        temperature_trend_subtitle = pn.panel(
            'Análisis de la tendencia lineal en base al histórico. Se presenta la recta y=a+b·x entre los años 2015 a 2022')

        ### TENDENCIA DE LA MÁXIMA
        temperature_trend_max_text = pn.panel(
            '**Tendencia de las temperaturas máximas**' + ' y=' + str(df_input_res.loc['T. Max.', 'Intercept'])[
                                                                  :6] + '+' + str(df_input_res.loc['T. Max.', 'Slope'])[
                                                                              :6] + 'x')
        temperature_max_reg = df_input_trend.hvplot(y=['T. Max.', 'Regresión T. Max.'], kind='line',
                                                    ylabel='Temperatura [ºC]', xlabel='Fecha',
                                                    title='Tendencia de las temperaturas máximas',
                                                    color=['#fa4134', 'b']).opts(xrotation=45)

        ### TENDENCIA DE LA MÍNIMA
        temperature_trend_min_text = pn.panel(
            '**Tendencia de las temperaturas mínimas**' + ' y=' + str(df_input_res.loc['T. Min.', 'Intercept'])[
                                                                  :6] + '+' + str(df_input_res.loc['T. Min.', 'Slope'])[
                                                                              :6] + 'x')
        temperature_min_reg = df_input_trend.hvplot(y=['T. Min.', 'Regresión T. Min.'], kind='line',
                                                    ylabel='Temperatura [ºC]', xlabel='Fecha',
                                                    title='Tendencia de las temperaturas mínimas',
                                                    color=['#3480fa', 'r']).opts(xrotation=45)

        ### TENDENCIA DE LA MEDIA TD1
        temperature_trend_med1_text = pn.panel(
            '**Tendencia de la temperatura media Td_1**' + ' y=' + str(df_input_res.loc['T. med1.', 'Intercept'])[
                                                                   :6] + '+' + str(
                df_input_res.loc['T. med1.', 'Slope'])[:6] + 'x')
        temperature_med1_reg = df_input_trend.hvplot(y=['T. med1.', 'Regresión T. med1.'], kind='line',
                                                     ylabel='Temperatura [ºC]', xlabel='Fecha',
                                                     title='Tendencia de la temperatura media Td_1',
                                                     color=['y', 'g']).opts(xrotation=45)

        block_temperature = pn.Column(temperature_med1_chart, temperature_maxmin_chart, temperature_ampl_chart,
                                      temperature_table_title_rel, temperature_table_text, df_out_table_rel_temp,
                                      temperature_table_title_abs, df_out_table_abs_temp, blank,
                                      temperature_table_med1_text, df_table_med1_temp,
                                      temperature_table_max_text, df_table_max_temp,
                                      temperature_table_min_text, df_table_min_temp,
                                      heatmap_med1_temp, heatmap_max_temp, heatmap_min_temp,
                                      temperature_trend_title, temperature_trend_subtitle,
                                      temperature_trend_med1_text, temperature_med1_reg,
                                      temperature_trend_max_text, temperature_max_reg,
                                      temperature_trend_min_text, temperature_min_reg
                                      )

        accordion_temperature = pn.Accordion(('Temperaturas', block_temperature))
        temperature_row = pn.Row(logo_thermometer, accordion_temperature)


        # self.latitud_box = pn.widgets.FloatInput(value=0, step=0.001, name="Latitud")
        # self.longitud_box = pn.widgets.FloatInput(value=0, step=0.001, name="Longitud")
        # self.boton = pn.widgets.Button(name="Mostrar en mapa")
        # self.mapa = pn.pane.HTML()

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