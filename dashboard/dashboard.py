import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_hour_user_df(df):
    hour_user_df = df.groupby('hr')['cnt_y'].sum().reset_index().sort_values(by='cnt_y', ascending=False).reset_index(drop=True)
    
    return hour_user_df

def create_working_day_df(df):
    working_day_df = df.groupby('workingday_y')['cnt_y'].sum().reset_index()
    working_day_df['workingday_y'] = working_day_df['workingday_y'].replace({0: 'Hari Tidak Kerja', 1: 'Hari Kerja'})
    
    return working_day_df

def create_season_user_df(df):
    season_user_df = df.groupby('season_y')['cnt_y'].sum().reset_index()
    season = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season_user_df['season_y'].replace(season, inplace=True)
    season_user_df.rename(columns={'season_y': 'musim', 'cnt_y': 'total_pengguna'}, inplace=True)
    season_user_df = season_user_df.sort_values(by='total_pengguna', ascending=False)
    return season_user_df

all_data = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_data.sort_values(by="dteday", inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

min_date = all_data["dteday"].min()
max_date = all_data["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_data[(all_data["dteday"] >= str(start_date)) & 
                (all_data["dteday"] <= str(end_date))]

hour_user_df = create_hour_user_df(main_df)
working_day_df = create_working_day_df(main_df)
season_user_df = create_season_user_df(main_df)

st.header(':bike: Dashboard Hasil Analisis Bike Sharing :computer:')

#Menampilkan Penggunaan Sepeda per Jam dalam Sehari
st.subheader("Penggunaan Sepeda per Jam dalam Sehari")
most_rented_hour = hour_user_df.iloc[0]['hr']
total_rentals_most_hour = hour_user_df.iloc[0]['cnt_y']
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Jam dengan penggunaan sepeda tertinggi: **{most_rented_hour}**")
with col2:
    st.markdown(f"Total pengguna pada saat jam ini: **{total_rentals_most_hour:,}** Pengguna")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='hr', y='cnt_y', data=hour_user_df, ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Total Penggunaan')
ax.set_title('Penggunaan Sepeda per Jam dalam Sehari')

hourly_rentals_df_sorted = hour_user_df.sort_values(by='hr', ascending=True)
st.pyplot(fig)
plt.close()

#Menampilkan Perbandingan Penggunaan Sepeda antara Hari Kerja dan Hari Tidak Kerja
st.subheader("Perbandingan Penggunaan Sepeda antara Hari Kerja dan Hari Tidak Kerja")
most_rented_day_type = working_day_df.iloc[0]['workingday_y']
total_rentals_most_day_type = working_day_df.iloc[0]['cnt_y']
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Penggunaan sepeda paling tinggi pada saat: **{most_rented_day_type}**")
with col2:
    st.markdown(f"Total pengguna pada hari tersebut: **{total_rentals_most_day_type}** Pengguna")

fig, ax = plt.subplots(figsize=(8, 6))
palette = {'Hari Kerja': 'darkblue', 'Hari Tidak Kerja': 'lightsteelblue'}
sns.barplot(x='workingday_y', y='cnt_y', data=working_day_df, ax=ax, palette=palette)
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Total Pengguna')
ax.set_title('Perbandingan Penggunaan Sepeda Antara Hari Kerja dan Hari Tidak Kerja')
st.pyplot(fig)
plt.close()

#Menampilkan Penggunaan Sepeda Pada Setiap Musim
st.subheader("Penggunaan Sepeda pada Setiap Musim")
col1, col2 = st.columns(2)
with col1:
    max_rentals_season = season_user_df.iloc[0]
    st.markdown(f"Penggunaan sepeda paling tinggi terjadi pada musim: **{max_rentals_season['musim']}**")
with col2:
    st.markdown(f"Total pengguna pada musim ini: **{int(max_rentals_season['total_pengguna']):,}**")

fig, ax = plt.subplots(figsize=(10, 6))
palette = {'fall': 'darkblue', 'summer': 'lightsteelblue', 'winter': 'lightsteelblue', 'spring': 'lightsteelblue',}
sns.barplot(x='musim', y='total_pengguna', data=season_user_df, ax=ax, palette=palette)
ax.set_xlabel('Musim')
ax.set_ylabel('Total Peminjaman')
ax.set_title('Penggunaan Sepeda pada Setiap Musim')
st.pyplot(fig)
plt.close()