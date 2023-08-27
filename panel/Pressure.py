import panel as pn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Pressure:
    def __init__(self, path_dict, df_input, excel_stats_dict, df_input_res, df_input_trend):
        self.df = df_input.copy()
        self.excel_stats_dict = excel_stats_dict
        self.df.index = pd.to_datetime(self.df.index)
        self.df_input_res = df_input_res.copy()
        self.df_input_trend = df_input_trend.copy()
        self.create_panel(path_dict)
    def contains_filter(self,df, lower, upper, column, df_ref):
        df_ref_filtered = df_ref[(df_ref.index >= lower) & (df_ref.index <= upper)]
        df.loc['Mínima rel. (Rango sel.)', 'Presión [hPa]'] = df_ref_filtered['P. Min.'].min()
        df.loc['Mínima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['P. Min.'].idxmin()
        df.loc['Máxima rel. (Rango sel.)', 'Presión [hPa]'] = df_ref_filtered['P. Max.'].max()
        df.loc['Máxima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['P. Max.'].idxmax()
        return df
    def create_panel(self, path_dict):
        blank = pn.panel('')

        ### PRESIÓN PLOT MAX MIN
        date_subrange_press = pn.widgets.DateRangeSlider(name='Date',
                                                         start=self.df.index[0],
                                                         end=self.df.index[-1])

        subset_dfi_press = self.df.interactive(sizing_mode='stretch_width')
        filtered_subrange_press = subset_dfi_press[
            (subset_dfi_press.index >= date_subrange_press.param.value_start) &
            (subset_dfi_press.index <= date_subrange_press.param.value_end)]

        init_date = filtered_subrange_press.index[0]
        end_date = self.df.index[-1]

        press_maxmin_chart = filtered_subrange_press.hvplot(y=['P. Min.', 'P. Max.'], kind='line',
                                                            ylabel='Presión [hPa]', xlabel='Fecha',
                                                            title='Presión máxima y mínima por día [hPa]').opts(
            legend_position='top_right', xrotation=45)
        # press_ampl_chart = filtered_subrange.hvplot(y=['T. Amp.'], kind='line', ylabel='Temperatura [ºC]', xlabel='Fecha', title='Amplitud térmica por día [ºC]', color='y').opts(xrotation=45)

        ### PRESIÓN TABLA RECORDS
        press_table_title_rel = pn.panel('#### Records relativos')
        press_table_title_abs = pn.panel('#### Records absolutos')
        press_table_text = pn.panel(
            '*** Los valores presentados correspondenden al rango de fechas seleccionado con los cursores anteriores.***')

        subset_dfi_press = self.df.interactive(sizing_mode='stretch_width')
        df_stats_rel_press = pd.DataFrame({'Estadísticas': ['Mínima rel. (Rango sel.)', 'Máxima rel. (Rango sel.)'],
                                           'Fecha': [0, 0],
                                           'Presión [hPa]': [0, 0]})

        df_stats_rel_press = df_stats_rel_press.set_index('Estadísticas')
        df_out_table_rel_press = pn.widgets.Tabulator(df_stats_rel_press, layout='fit_data_table')

        df_out_table_rel_press.add_filter(pn.bind(self.contains_filter, lower=date_subrange_press.param.value_start,
                                                  upper=date_subrange_press.param.value_end, column='T. Min.',
                                                  df_ref=self.df))

        self.excel_stats_dict['stats_press'] = self.excel_stats_dict['stats_press'].set_index('Estadísticas')
        self.excel_stats_dict['stats_press']['Fecha'] = self.excel_stats_dict['stats_press']['Fecha'].dt.strftime('%Y-%m-%d')
        df_out_table_abs_press = pn.widgets.Tabulator(self.excel_stats_dict['stats_press'], layout='fit_data_table')

        ### PRESIÓN TABLA RESUMEN
        df_input_max_press = self.excel_stats_dict['P. Max. mes']
        df_input_min_press = self.excel_stats_dict['P. Min. mes']

        df_input_max_press = df_input_max_press.set_index(df_input_max_press.columns[0])
        df_input_min_press = df_input_min_press.set_index(df_input_min_press.columns[0])

        press_table_max_text = pn.panel('### Presión máxima media por mes [hPa]')
        press_table_min_text = pn.panel('### Presión mínima media por mes [hPa]')
        df_table_max_press = pn.widgets.Tabulator(df_input_max_press, width=800,
                                                  selection=[df_input_max_press.shape[0] - 1])
        df_table_min_press = pn.widgets.Tabulator(df_input_min_press, width=800,
                                                  selection=[df_input_max_press.shape[0] - 1])

        block_press = pn.Column(press_maxmin_chart,
                                press_table_title_rel, press_table_text, df_out_table_rel_press,
                                press_table_title_abs, df_out_table_abs_press, blank,
                                press_table_max_text, df_table_max_press,
                                press_table_min_text, df_table_min_press)

        self.panel = pn.template.ReactTemplate(
            title='PRESIÓN',
            main=block_press
        )

    def show(self):
        return self.panel.servable()