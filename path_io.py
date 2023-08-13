import os
import GLOBAL_VARS
import pandas as pd

def get_path_dict(root =os.sep):

    paht_dict = {"input_path": os.path.join(os.sep, root, 'data', GLOBAL_VARS.input_name),
                 "input_trend_path": os.path.join(os.sep, root, 'data', GLOBAL_VARS.input_trend_name),
                 "input_res_path": os.path.join(os.sep, root, 'data', GLOBAL_VARS.input_res_name),
                 "input_stats_path": os.path.join(os.sep, root, 'data', GLOBAL_VARS.input_stats_name),
                 "input_compare_path": os.path.join(os.sep, root, 'data', GLOBAL_VARS.input_compare_name),
                 "input_predict_path": os.path.join(os.sep, root, 'data', GLOBAL_VARS.input_predict_name)}

    return paht_dict
def load_data(paht_dict):

    df_input = pd.read_csv(paht_dict["input_path"], sep=';', index_col=[0])
    df_input.index = pd.to_datetime(df_input.index)

    df_input_trend = pd.read_csv(paht_dict["input_trend_path"], sep=';', index_col=[0])
    df_input_trend.index = pd.to_datetime(df_input_trend.index)

    df_input_res = pd.read_csv(paht_dict["input_res_path"], sep=';', index_col=[0])

    excel_compare_dict = pd.read_excel(paht_dict["input_compare_path"], sheet_name=None, index_col=None)
    excel_predict_dict = pd.read_excel(paht_dict["input_predict_path"], sheet_name=None, index_col=None)
    excel_stats_dict = pd.read_excel(paht_dict["input_stats_path"], sheet_name=None, index_col=None)

    return df_input, df_input_trend, df_input_res, excel_compare_dict, excel_predict_dict, excel_stats_dict

    def unique(lista):
        unique_list = []
        for x in lista:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list