import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Настройка страницы (заголовок вкладки браузера)
st.set_page_config(page_title="Курсы валют ЦБ РФ", layout="wide")

st.title("📈 Анализ валютных курсов ЦБ РФ")

# 2. Загрузка данных
@st.cache_data
def load_data():
    df = pd.read_excel("cbr_history.xlsx")
    
    # ЖЕСТКО превращаем дату в формат datetime
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    
    # ЖЕСТКО превращаем rate в числа (убираем запятые, если они есть)
    df['rate'] = df['rate'].astype(str).str.replace(',', '.').astype(float)
    
    # Сортируем по дате, чтобы линии не скакали
    df = df.sort_values(by='date')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Файл cbr_history.xlsx не найден! Запусти сначала cbr_parser.py")
    st.stop()

# 3. Фильтры
available_currencies = df['letter_code'].unique()
selected_currencies = st.multiselect(
    "Выберите валюты для отображения:",
    options=available_currencies,
    default=['USD', 'EUR']
)

filtered_df = df[df['letter_code'].isin(selected_currencies)]

# 4. Вывод графиков
if not filtered_df.empty:
    st.subheader("Динамика курсов")
    
    # Создаем график Plotly
    fig = px.line(
        filtered_df, 
        x='date', 
        y='rate', 
        color='letter_code', 
        markers=True,
        labels={'rate': 'Курс (руб)', 'date': 'Дата', 'letter_code': 'Валюта'}
    )
    
    # Настраиваем внешний вид (высота, фон, отступы)
    fig.update_layout(
        height=500, # Фиксированная высота, чтобы не растягивался по вертикали
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis=dict(
            autorange=True, # Автоматический масштаб оси Y
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        )
    )
    
    # use_container_width=True оставляем, но благодаря фиксированной высоте он будет аккуратным
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Текущие курсы (последняя дата)")
    latest = filtered_df.sort_values('date').groupby('letter_code').tail(1)
    st.dataframe(latest[['letter_code', 'name', 'rate', 'date']], hide_index=True)
else:
    st.warning("Выберите хотя бы одну валюту.")