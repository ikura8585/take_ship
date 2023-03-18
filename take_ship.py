import streamlit as st
import pandas as pd
import openpyxl

# 取引名の置換
def fukusuu_replace(lines):
    wawawa_dict = {
        '関光汽船': '',
        '産業運輸': '',
        'nan': '',
        '北九州100え':'',
        '北九州130え':'',
        '北九州130あ':'',
        '北九州130え':'',
        '小倉運送': '小倉',
        '曜日': '',
        '農業用フィルム':'フィルム'
    }
    
    for key, value in wawawa_dict.items():
        lines = lines.replace(key, value)
        
    return lines

st.title("乗船")

uploaded_file = st.file_uploader("ファイルアップロード", type='xlsx')

if uploaded_file is not None:
    book = openpyxl.load_workbook(uploaded_file)
    sheets = book.sheetnames

    # 九州向け
    df2_SHEET1 = []
    # if df_SHEET1.iat[11, 28] == "新門司港":
    df_SHEET1 = pd.read_excel(uploaded_file,sheet_name=sheets[0],header=None)
    
    n = 0
    for i in df_SHEET1.iloc[:,0]:
        if type(i) == int:
            df2_SHEET1.append(df_SHEET1.iat[n, 4] + " " + df_SHEET1.iat[n, 7] + " " + df_SHEET1.iat[n, 14] + " " + str(df_SHEET1.iat[n,27]))
        n += 1
    for i in range(len(df2_SHEET1)):
        df2_SHEET1[i] = fukusuu_replace(df2_SHEET1[i])
    

    # 徳島向けがある場合(二つ目のシートがある場合)
    df2_SHEET2 = []

    n = 0
    if len(sheets) == 2:
        df_SHEET2 = pd.read_excel(uploaded_file,sheet_name=sheets[1],header=None)
        
        for i in df_SHEET2.iloc[:,0]:
            if type(i) == int:
                df2_SHEET2.append(df_SHEET2.iat[n, 4] + " " + df_SHEET2.iat[n, 7] + " " + df_SHEET2.iat[n, 14] + " " + str(df_SHEET2.iat[n,27]))
            n += 1

        for i in range(len(df2_SHEET2)):
            df2_SHEET2[i] = fukusuu_replace(df2_SHEET2[i])

    if df2_SHEET2:
        date_number = (df_SHEET1.iat[10,3][5:].replace('曜日','').replace('月','/',1).replace('日','',1)+ " 乗船" + str(len(df2_SHEET1)+len(df2_SHEET2))+ "本")
    else:
        date_number = (df_SHEET1.iat[10,3][5:].replace('曜日','').replace('月','/',1).replace('日','',1)+ " 乗船" + str(len(df2_SHEET1))+ "本")
    st.text(date_number)
    if df_SHEET1.iat[11, 28] == "徳島港":
        st.text('徳島向け')
    for i in df2_SHEET1:
        st.text(i)
    if df2_SHEET2:
        st.text('徳島向け')
        for i in df2_SHEET2:
            st.text(i)