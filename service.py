import pandas as pd
import streamlit as st
from catboost import CatBoostRegressor
from io import BytesIO

@st.cache(allow_output_mutation=True)
def load_model():
    model = CatBoostRegressor()
    model.load_model('test_model', format='cbm')
    return model

# @st.cache
# def convert_df(df):
#    return df.to_excel(index=False)

@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def load_data():
    uploaded_file = st.file_uploader(label='Выберите таблицу')
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        cat_features = [
            'material_type'
            ]
        for col in cat_features:
            data[col] = data[col].astype(str)
            data[col] = data[col].fillna('nan')
        return data
    else:
        return None


model = load_model()

st.title('Прогнозирование выживаемости клеток')
table = load_data()
result = st.button('Построить прогноз')
if result:
    preds = model.predict(table)
    table['viability'] = preds
    excel = to_excel(table)

    st.write('**Результаты скоринга**')

    st.download_button(
        "Press to Download",
        data=excel,
        file_name= 'data_with_preds.xlsx',
        key='download-xlsx'
    )
st.markdown(
    """
    ### Используемые признаки:   
    * material_type  
    * concentration  
    * time  
    * surface_charge  
    * diameter  
    * ionic_radius  
    * electronegativity  
    * no_of_cells  
    ### Целевая  
    * viability  
    """
    )