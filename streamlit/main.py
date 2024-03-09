import streamlit as st

import pandas as pd
import pydeck as pdk


source_df = pd.read_csv("./data/out/vote_discrepancy.csv")
viz_df = pd.read_csv("./data/out/vote_discrepancy_viz.csv")

st.title("Perbedaan Jumlah Suara pada Pemilihan Presiden dan Wakil Presiden Indonesia 2024")

st.markdown("""Peta dibawah menunjukkan intensitas TPS yang memiliki perbedaan data antara jumlah total suara paslon
            dengan jumlah suara sah berdasarkan lokasi TPS. Data diambil dari hasil scraping laman resmi KPU untuk Pemilu 2024 [disini](https://data-pemilu.vercel.app/)""")

# Define a layer to display on a map
layer = pdk.Layer(
    "HeatmapLayer",
    data=viz_df,
    opacity=0.9,
    get_position=["longitude", "latitude"],
    threshold=0.5,
    aggregation=pdk.types.String("COUNT"),
    get_weight="weight",
    pickable=True,
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=106.82270,
    latitude=-6.17450,
    zoom=5,
    min_zoom=3,
    max_zoom=15,
    # pitch=40.5,
    # bearing=-27.36,
)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(r)

st.markdown("""Kesalahan yang terjadi mayoritas disebabkan oleh human-error dimana formulir C1 tidak diunggah pada kolom yang seharusnya. Kesalahan yang paling umum ditemui selama eksplorasi data
            adalah kesalahan halaman formulir C1, dimana kolom halaman 1 diisi dengan halaman 2 atau 3, selanjutnya aplikasi Sirekap masih menerima foto formulir dengan format yang tidak sesuai, 
            seperti horizontal atau terbalik 180 derajat. Hal ini tentunya mengganggu performa dari OCR yang digunakan""")

st.subheader("Sumber Data")

st.markdown("""Tabel dibawah adalah sumber data untuk membangun visualisasi diatas, anda dapat melihat perbedaan nilai pada kolom `manual_suara_sah` 
            yang merupakan hasil dari fungsi perhitungan (sum) dari kolom `suara_paslon_1`, `suara_paslon_2` dan `suara_paslon_3` dengan kolom `suara_sah` yang merupakan
            nilai asli dari KPU. Dimana pada beberapa baris data, total jumlah suara paslon melebihi suara sah yang tercatat""")

st.dataframe(
    source_df,
    column_config={
        "url_page": st.column_config.LinkColumn("URL Laman KPU"),
    }
)

st.markdown("""Data mentah sebelum diolah dapat ditemukan [disini](https://data-pemilu.vercel.app/data-presiden-wakil-presiden#ppwp_tps), sementara kode untuk pengolahan data dapat anda akses [disini](https://github.com/IqbalLx/pemilu2024-insight)""")

st.subheader("Keterbatasan")
st.markdown("Laman ini dibuat dengan keterbatasan waktu eksplorasi data sehingga informasi diatas tidak dapat dijadikan sumber rujukan, dan keterbatasan koordinat dari seluruh kelurahan/desa di Indonesia, sehingga data TPS untuk provinsi Papua Selatan, Papua Tengah, Papua Pegunungan, dan Papua Barat Daya tidak termasuk dalam visualisasi diatas")