import streamlit as st
import os 
import json
import io
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="Подбор участников каната", page_icon="🙋")
st.title('Подбор состава для каната ActionLab')
clean_PD = False #st.sidebar.checkbox('Скрывать персональные данные', False)
st.write('Скачайте шаблон файла слева страницы, заполните данные команды и загрузите через форму загрузки файлов слева')
max_team = st.sidebar.number_input('Количество участников', min_value=2, max_value=10, value=8)
max_weight = st.sidebar.number_input('Максимальный вес, кг.', min_value=100, max_value=1000, value=650)

df = pd.read_excel('Канат_people.xlsx')
weights = df['Вес'].astype(float).tolist()
names = df['Участник'].tolist()


# max_weight = 650
# max_team = 8


buffer = io.BytesIO()
df.to_excel(buffer, sheet_name='Sheet1', index=False)
download2 = st.sidebar.download_button(
    label="Шаблон для заполнения данных по команде",
    data=buffer,
    key=1,
    file_name=f'Канат_people.xlsx',
    mime='application/vnd.ms-excel'
)

uploaded_file = st.sidebar.file_uploader('Загрузите файл с составом учасников в соответствии с шаблоном', type={ "xlsx"})

if uploaded_file:
    # raw_text = docx2txt.process(uploaded_file)
    # df = pd.read_excel('rope_team/Канат_people.xlsx')
    df = pd.read_excel(uploaded_file)
    # st.write("dogovor.docx", uploaded_file.name)
    weights2 = df.apply(lambda x: x['Участник']+'_|'+str(x['Вес']), axis=1)
    results = {}
    output = ""
    for j in [max_team,max_team-1,max_team-2]:
        results[j] = []
        combi = combinations(weights2, j)
        variants = list(combi)
        for v in variants:
            w = sum([float(a.split('_|')[1]) for a in v])
            if w <= max_weight:
                results[j].append([j,w]+(sorted([a.split('_|')[0] for a in v])))
        d = results[j]
        d.sort(key=lambda x: x[1])
        tp = pd.DataFrame(d[::-1]).drop_duplicates()
        if len(tp)>0:
            d = tp.to_records(index=False).tolist()
            fr = f"""Подобрано {len(d)} вариантов состава для команды из {j} человек и максимальном весе {max_weight} кг."""
            output = output + fr + '\n'
            print(fr)
            for m in d[:20]:
                r = f"Суммарный вес {m[1]} кг. Состав:{', '.join(m[2:])}"
                output = output + r + '\n'
                print(r)
        else:
            fr = f"""Нет вариантов состава для команды из {j} человек и максимальном весе {max_weight} кг. :("""
            output = output + fr + '\n'
            print(fr)


    st.text_area('Результаты подборки: ', output, height=600)


