import panel as pn
import pandas as pd
import numpy as np
from holoviews import dim, opts
import holoviews as hv

import matplotlib.pyplot as plt

class Precipitation:
    def __init__(self, path_dict, df_input, excel_stats_dict, df_input_res, df_input_trend):
        self.df = df_input.copy()
        self.excel_stats_dict = excel_stats_dict
        self.df.index = pd.to_datetime(self.df.index)
        self.df_input_res = df_input_res.copy()
        self.df_input_trend = df_input_trend.copy()
        self.create_panel(path_dict)

    def contains_filter(self, df, lower, upper, column, df_ref):
        df.loc['Máxima acumulada en un día rel. (Rango sel.)', 'Fecha'] = \
            df_ref[(df_ref.index >= lower) & (df_ref.index <= upper)]['Precipitación'].idxmax()
        df.loc['Máxima acumulada en un día rel. (Rango sel.)', 'Precipitación [l/m2]'] = \
            df_ref[(df_ref.index >= lower) & (df_ref.index <= upper)]['Precipitación'].max()

        # Días con más lluvia seguidos
        df_ref = df_ref[(df_ref.index >= lower) & (df_ref.index <= upper)]
        df_ref['Prec. Acumulado'] = np.zeros([df_ref.shape[0], 1])
        rain_position = df_ref.columns.get_loc("Precipitación")
        arain_position = df_ref.columns.get_loc("Prec. Acumulado")
        for i in range(df_ref.shape[0]):
            if df_ref.iloc[i, rain_position] != 0:
                df_ref.iloc[i, arain_position] = '1'
                pass
        df_ref["Cuenta_lluvia"] = df_ref["Prec. Acumulado"].groupby(
            (df_ref["Prec. Acumulado"] == 0).cumsum()).cumcount()
        df_ref["Cuenta_sequía"] = df_ref["Prec. Acumulado"].groupby(
            (df_ref["Prec. Acumulado"] != 0).cumsum()).cumcount()
        df.loc['Máx. días seguidos de precipitación rel. (Rango sel.)', 'Días'] = df_ref["Cuenta_lluvia"].max()
        df.loc['Máx. días seguidos de precipitación rel. (Rango sel.)', 'Fecha'] = df_ref["Cuenta_lluvia"].idxmax()
        df.loc['Máx. días seguidos de sequía rel. (Rango sel.)', 'Días'] = df_ref["Cuenta_sequía"].max()
        df.loc['Máx. días seguidos de sequía rel. (Rango sel.)', 'Fecha'] = df_ref["Cuenta_sequía"].idxmax()

        return df
    def create_panel(self, path_dict):
        blank = pn.panel('')

        ### PRECIPITACIÓN PLOT MAX
        self.df.index = pd.to_datetime(self.df.index)
        date_subrange_rain = pn.widgets.DateRangeSlider(name='Date',
                                                        start=self.df.index[0],
                                                        end=self.df.index[-1])

        subset_dfi_rain = self.df.interactive(sizing_mode='stretch_width')
        filtered_subrange_rain = subset_dfi_rain[
            (subset_dfi_rain.index >= date_subrange_rain.param.value_start) &
            (subset_dfi_rain.index <= date_subrange_rain.param.value_end)]

        init_date = filtered_subrange_rain.index[0]
        end_date = self.df.index[-1]

        rain_max_chart = filtered_subrange_rain.hvplot(y=['Precipitación'], kind='line', ylabel='Precipitación [l/m2]',
                                                       xlabel='Fecha', title='Precipitación por día [l/m2]').opts(
            xrotation=45)

        ### PRECIPITACIÓN TABLA RECORDS
        rain_table_title_rel = pn.panel('#### Records relativos')
        rain_table_title_abs = pn.panel('#### Records absolutos')
        rain_table_text = pn.panel(
            '*** Los valores presentados correspondenden al rango de fechas seleccionado con los cursores anteriores.***')

        subset_dfi_rain = self.df.interactive(sizing_mode='stretch_width')
        df_stats_rel_rain = pd.DataFrame({'Estadísticas': ['Máxima acumulada en un día rel. (Rango sel.)',
                                                           'Máx. días seguidos de precipitación rel. (Rango sel.)',
                                                           'Máx. días seguidos de sequía rel. (Rango sel.)'],
                                          'Fecha': [0, 0, 0],
                                          'Precipitación [l/m2]': [0, '-', '-'],
                                          'Días': ['-', 0, 0]})

        df_stats_rel_rain = df_stats_rel_rain.set_index('Estadísticas')
        df_out_table_rel_rain = pn.widgets.Tabulator(df_stats_rel_rain, layout='fit_data_table')

        df_out_table_rel_rain.add_filter(pn.bind(self.contains_filter, lower=date_subrange_rain.param.value_start,
                                                 upper=date_subrange_rain.param.value_end, column='T. Min.',
                                                 df_ref=self.df))

        self.excel_stats_dict['stats_prec'] = self.excel_stats_dict['stats_prec'].set_index('Estadísticas')
        self.excel_stats_dict['stats_prec']['Fecha'] = self.excel_stats_dict['stats_prec']['Fecha'].dt.strftime('%Y-%m-%d')
        df_out_table_abs_rain = pn.widgets.Tabulator(self.excel_stats_dict['stats_prec'], layout='fit_data_table')

        ### PRECIPITACIÓN TABLA RESUMEN
        df_input_max_rain = self.excel_stats_dict['Precipitación mes']
        df_input_max_rain = df_input_max_rain.set_index(df_input_max_rain.columns[0])
        rain_table_max_text = pn.panel('### Precipitación acumulada por mes [l/m2]')
        df_table_max_rain = pn.widgets.Tabulator(df_input_max_rain, width=800,
                                                 selection=[df_input_max_rain.shape[0] - 1])

        max_rain_list = df_input_max_rain.columns.tolist()
        points = [
            (df_input_max_rain.columns.tolist()[i], df_input_max_rain.index.tolist()[j], df_input_max_rain.iloc[j, i])
            for i in range(12) for j in range(10)]
        heatmap_max_rain = hv.HeatMap(points)
        (heatmap_max_rain).opts(
            opts.HeatMap(toolbar='above', tools=['hover']),
            opts.Points(tools=['hover'], size=dim('z') * 0.3)).opts(colorbar=True, xlabel='Mes', ylabel='Año',
                                                                    width=500, height=400)
        heatmap_max_rain = hv.Layout(
            [heatmap_max_rain.relabel('Precipitación acumulada [l/m2]').opts(cmap=c) for c in ['blues']])

        block_rain = pn.Column(rain_max_chart,
                               rain_table_title_rel, rain_table_text, df_out_table_rel_rain,
                               rain_table_title_abs, df_out_table_abs_rain, blank,
                               rain_table_max_text, df_table_max_rain, heatmap_max_rain, )

        self.panel = pn.template.ReactTemplate(
            title='PRECIPITACIÓN',
            main=block_rain
        )

    def show(self):
        return self.panel.servable()