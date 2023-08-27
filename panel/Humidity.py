import panel as pn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Humidity:
    def __init__(self, path_dict, df_input, excel_stats_dict, df_input_res, df_input_trend):
        self.df = df_input.copy()
        self.excel_stats_dict = excel_stats_dict
        self.df.index = pd.to_datetime(self.df.index)
        self.df_input_res = df_input_res.copy()
        self.df_input_trend = df_input_trend.copy()
        self.create_panel(path_dict)
    def contains_filter(self, df, lower, upper, column, df_ref):
        df_ref_filtered = df_ref[(df_ref.index >= lower) & (df_ref.index <= upper)]
        if not lower or not upper:
            return df
        df.loc['Mínima rel. (Rango sel.)', 'Humedad [%]'] = df_ref_filtered['H. Min.'].min()
        df.loc['Mínima Max. rel. (Rango sel.)', 'Humedad [%]'] = df_ref_filtered['H. Min.'].max()
        df.loc['Mínima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['H. Min.'].idxmin()
        df.loc['Mínima Max. rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['H. Min.'].idxmax()
        df.loc['Máxima rel. (Rango sel.)', 'Humedad [%]'] = df_ref_filtered['H. Max.'].max()
        df.loc['Máxima rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['H. Max.'].idxmax()
        df.loc['Máxima Min. rel. (Rango sel.)', 'Humedad [%]'] = df_ref_filtered['H. Max.'].min()
        df.loc['Máxima Min. rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['H. Max.'].idxmin()
        df.loc['Máxima Min. rel. (Rango sel.)', 'Humedad [%]'] = df_ref_filtered['H. Amp.'].min()
        df.loc['Máxima Min. rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['H. Amp.'].idxmin()
        df.loc['Max. amplitud rel. (Rango sel.)', 'Humedad [%]'] = df_ref_filtered['H. Amp.'].max()
        df.loc['Max. amplitud rel. (Rango sel.)', 'Fecha'] = df_ref_filtered['H. Amp.'].idxmax()
        return df
    def create_panel(self, path_dict):
        blank = pn.panel('')

        ### HUMEDAD PLOT MAX MIN
        self.df.index = pd.to_datetime(self.df.index)
        date_subrange_hum = pn.widgets.DateRangeSlider(name='Date',
                                                       start=self.df.index[0],
                                                       end=self.df.index[-1])

        subset_dfi_hum = self.df.interactive(sizing_mode='stretch_width')
        filtered_subrange_hum = subset_dfi_hum[
            (subset_dfi_hum.index >= date_subrange_hum.param.value_start) &
            (subset_dfi_hum.index <= date_subrange_hum.param.value_end)]

        init_date = filtered_subrange_hum.index[0]
        end_date = self.df.index[-1]

        hum_maxmin_chart = filtered_subrange_hum.hvplot(y=['H. Min.', 'H. Max.'], kind='line', ylabel='Humedad [%]',
                                                        xlabel='Fecha',
                                                        title='Humedad máxima y mínima por día [%]').opts(
            legend_position='top_right', xrotation=45)

        ### HUMEDAD TABLA RECORDS
        hum_table_title_rel = pn.panel('#### Records relativos')
        hum_table_title_abs = pn.panel('#### Records absolutos')
        hum_table_text = pn.panel(
            '*** Los valores presentados correspondenden al rango de fechas seleccionado con los cursores anteriores.***')

        subset_dfi_hum = self.df.interactive(sizing_mode='stretch_width')
        df_stats_rel_hum = pd.DataFrame({'Estadísticas': ['Mínima rel. (Rango sel.)', 'Mínima Max. rel. (Rango sel.)',
                                                          'Máxima rel. (Rango sel.)', 'Máxima Min. rel. (Rango sel.)',
                                                          'Máxima Min. rel. (Rango sel.)',
                                                          'Max. amplitud rel. (Rango sel.)'],
                                         'Fecha': [0, 0, 0, 0, 0, 0],
                                         'Humedad [%]': [0, 0, 0, 0, 0, 0]})

        df_stats_rel_hum = df_stats_rel_hum.set_index('Estadísticas')
        df_out_table_rel_hum = pn.widgets.Tabulator(df_stats_rel_hum, layout='fit_data_table')

        df_out_table_rel_hum.add_filter(
            pn.bind(self.contains_filter, lower=date_subrange_hum.param.value_start, upper=date_subrange_hum.param.value_end,
                    column='T. Min.', df_ref=self.df))

        self.excel_stats_dict['stats_hum'] = self.excel_stats_dict['stats_hum'].set_index('Estadísticas')
        self.excel_stats_dict['stats_hum']['Fecha'] = self.excel_stats_dict['stats_hum']['Fecha'].dt.strftime('%Y-%m-%d')

        df_out_table_abs_hum = pn.widgets.Tabulator(self.excel_stats_dict['stats_hum'], layout='fit_data_table')

        ### HUMEDAD TABLA RESUMEN
        df_input_max_hum = self.excel_stats_dict['H. Max. mes']
        df_input_min_hum = self.excel_stats_dict['H. Min. mes']

        df_input_max_hum = df_input_max_hum.set_index(df_input_max_hum.columns[0])
        df_input_min_hum = df_input_min_hum.set_index(df_input_min_hum.columns[0])

        hum_table_max_text = pn.panel('### Humedad máxima media por mes [%]')
        hum_table_min_text = pn.panel('### Humedad mínima media por mes [%]')
        df_table_max_hum = pn.widgets.Tabulator(df_input_max_hum, width=800, selection=[df_input_max_hum.shape[0] - 1])
        df_table_min_hum = pn.widgets.Tabulator(df_input_min_hum, width=800, selection=[df_input_max_hum.shape[0] - 1])

        block_hum = pn.Column(hum_maxmin_chart,
                              hum_table_title_rel, hum_table_text, df_out_table_rel_hum,
                              hum_table_title_abs, df_out_table_abs_hum, blank,
                              hum_table_max_text, df_table_max_hum,
                              hum_table_min_text, df_table_min_hum)

        self.panel = pn.template.ReactTemplate(
            title='HUMEDAD',
            main=block_hum
        )

    def show(self):
        return self.panel.servable()