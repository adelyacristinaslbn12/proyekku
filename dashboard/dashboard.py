import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Penyewaan Sepeda", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Contoh EDA Penyewaan Sepeda")
st.markdown("<style>h1{font-size: 2rem;}</style>", unsafe_allow_html=True)

df = pd.read_csv("dashboard/main_data.csv", encoding="ISO-8859-1")

print("Kolom yang tersedia:", df.columns.tolist())

df["dteday"] = pd.to_datetime(df["dteday"])
tanggalMulai = pd.to_datetime(df["dteday"]).min()
tanggalAkhir = pd.to_datetime(df["dteday"]).max()

col1, col2 = st.columns(2)
with col1:
    tanggal1 = pd.to_datetime(st.date_input("Tanggal Mulai", tanggalMulai))
with col2:
    tanggal2 = pd.to_datetime(st.date_input("Tanggal Akhir", tanggalAkhir))

df = df[(df["dteday"] >= tanggal1) & (df["dteday"] <= tanggal2)].copy()

st.sidebar.header("Pilih filter Anda:")

label_cuaca = {
    1: 'cerah',
    2: 'berkabut',
    3: 'hujan/salju ringan',
    4: 'hari kerja',
    5: 'hari libur'
}
df['weathersit_x'] = df['weathersit_x'].map(label_cuaca)
cuaca = st.sidebar.multiselect("Pilih cuaca", df["weathersit_x"].unique())
df2 = df[df["weathersit_x"].isin(cuaca)] if cuaca else df.copy()

df['label_hari_kerja'] = df['workingday_x'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

tab1, tab2 = st.tabs(["Analisis Cuaca", "Analisis Hari Kerja"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Total Pengguna Sepeda berdasarkan Cuaca")
        fig = px.bar(df2, x="weathersit_x", y="cnt_x", 
                    labels={"weathersit_x": "Cuaca", "cnt_x": "Total"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Persentase Pengguna berdasarkan Cuaca")
        fig = px.pie(df2, values="cnt_x", names="weathersit_x", 
                    labels={"weathersit_x": "Cuaca", "cnt_x": "Total"})
        fig.update_traces(textposition="inside")
        fig.update_layout(margin=dict(t=50))
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Total Pengguna Sepeda berdasarkan Jenis Hari")
        data_hari_kerja = df.groupby('label_hari_kerja')['cnt_x'].sum().reset_index()
        fig = px.bar(data_hari_kerja, x="label_hari_kerja", y="cnt_x",
                     labels={"label_hari_kerja": "Jenis Hari", "cnt_x": "Total Pengguna"},
                     color="label_hari_kerja")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Rata-rata Pengguna per Jam dan Jenis Hari")
        rata_rata_jam = df.groupby(['hr', 'label_hari_kerja'])['cnt_x'].mean().reset_index()
        fig = px.line(rata_rata_jam, x="hr", y="cnt_x", color="label_hari_kerja",
                      labels={"hr": "Jam", "cnt_x": "Rata-rata Pengguna", 
                             "label_hari_kerja": "Jenis Hari"})
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Tren Bulanan")
linechart_df2 = df2.groupby(df2["dteday"].dt.strftime("%b : %Y"))["cnt_x"].sum().reset_index()
linechart_df2["dteday"] = pd.to_datetime(linechart_df2["dteday"], format="%b : %Y")
linechart_df2 = linechart_df2.sort_values(by="dteday")
fig = px.line(linechart_df2, x="dteday", y="cnt_x", 
              labels={"dteday": "Tanggal", "cnt_x": "Total Pengguna"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Unduh Dataset Asli")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Unduh Data", data=csv, file_name="Dataset_Sepeda.csv", mime="text/csv")