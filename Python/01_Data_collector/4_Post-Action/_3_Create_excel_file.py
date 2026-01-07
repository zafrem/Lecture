# pip install xlsxwriter
import _1_technical_analysis_Stochastic as stochastic
import pandas as pd
import os


if "__main__" == __name__:
    report_xlsx = './stochastic_report.xlsx'

    df = stochastic.init_pre_df()
    plt, df = stochastic.stochastic(df)

    if os.path.exists(report_xlsx):
        os.remove(report_xlsx)

    writer = pd.ExcelWriter(report_xlsx, engine='xlsxwriter')
    df.to_excel(writer)
    writer.close()