import pandas as pd
import os

def read_excel(sheet_name):
    excel_file = os.getcwd() + '/Settings/Config.xlsx'
    df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=['UserName', 'DisplayName', 'bAutoRecord'])
    # print(df)
    return df