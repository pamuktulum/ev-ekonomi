
import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Pro Finansal Yönetim Paneli", layout="wide", page_icon="🏦")
st.title("🏦 Pro Hanehalkı Finans ve Analiz Paneli (v2.0)")
st.markdown("Hane halkı bireylerinin gelir/gider dağılımlarını ve kişisel bilançolarını yönetin.")

# --- VERİ TABANI (SESSION STATE) ---
if 'uyeler' not in st.session_state:
    st.session_state.uyeler = ["Ortak Kasa", "Emir Kaan"] # Varsayılan üyeler
if 'bankalar' not in st.session_state:
    st.session_state.bankalar = []
if 'sahsi_borclar' not in st.session_state:
    st.session_state.sahsi_borclar = []
if 'gelirler' not in st.session_state:
    st.session_state.gelirler = []
if 'sabit_giderler' not in st.session_state:
    st.session_state.sabit_giderler = []

# --- YAN MENÜ (AYARLAR VE GİRDİLER) ---
st.sidebar.header("👨‍👩‍👧 1. Hane Halkı Bireyleri")
with st.sidebar.form("uye_ekle_form", clear_on_submit=True):
    yeni_uye = st.text_input("Yeni Kişi Ekle (Örn: Anne, Eş)")
    if st.form_submit_button("Kişiyi Sisteme Ekle"):
        if yeni_uye and yeni_uye not in st.session_state.uyeler:
            st.session_state.uyeler.append(yeni_uye)
            st.success(f"{yeni_uye} eklendi!")

st.sidebar.markdown("Mevcut Bireyler: " + ", ".join(st.session_state.uyeler))
st.sidebar.markdown("---")

st.sidebar.header("🌍 2. Güncel Piyasa Kurları")
kur_euro = st.sidebar.number_input("1 Euro (TL)", value=50.71, step=0.1)
kur_altin = st.sidebar.number_input("1 Cumhuriyet Altını (TL)", value=48342.0, step=100.0)
st.sidebar.markdown("---")

st.sidebar.header("➕ 3. Sisteme Veri Ekle")

# GELİR EKLEME FORMU
with st.sidebar.expander("Gelir Ekle"):
    with st.form("gelir_form", clear_on_submit=True):
        g_kisi = st.selectbox("Kimin Geliri?", st.session_state.uyeler)
        g_isim = st.text_input("Gelir Adı (Örn: Maaş)")
        g_tutar = st.number_input("Aylık Tutar (TL)", min_value=0, step=1000)
        g_gun = st.number_input("Yatış Günü", min_value=1, max_value=31, value=10)
        if st.form_submit_button("Ekle"):
            st.session_state.gelirler.append({"Kişi": g_kisi, "Adı": g_isim, "Tutar": g_tutar, "Gün": g_gun})

# BANKA VE KREDİ EKLEME FORMU
with st.sidebar.expander("Banka / Kredi / KMH Ekle"):
    with st.form("banka_form", clear_on_submit=True):
        b_kisi = st.selectbox("Kimin Üzerine?", st.session_state.uyeler)
        b_isim = st.selectbox("Banka", ["İş Bankası", "Yapı Kredi", "Ziraat Bankası", "Diğer"])
        b_tur = st.selectbox("Ürün", ["İhtiyaç Kredisi", "Ev Kredisi", "Kredi Kartı", "KMH (Ek Hesap)"])
        b_borc = st.number_input("Aylık Yük/Borç (TL)", min_value=0, step=1000)
        b_faiz = st.number_input("Faiz Oranı (%)", min_value=0.0, value=4.25, step=0.1)
        if st.form_submit_button("Ekle"):
            st.session_state.bankalar.append({"Kişi": b_kisi, "Banka": b_isim, "Tür": b_tur, "Aylık Yük": b_borc, "Faiz %": b_faiz})

# ŞAHSİ BORÇ EKLEME FORMU
with st.sidebar.expander("Şahsi Borç Ekle (Döviz/Altın)"):
    with st.form("sahsi_form", clear_on_submit=True):
        s_kisi = st.selectbox("Borçlu Kim?", st.session_state.uyeler)
        s_isim = st.text_input("Kime Borçlu? (Örn: Mahir)")
        s_tutar = st.number_input("Tutar", min_value=0.0, step=1.0)
        s_birim = st.selectbox("Birim", ["TL", "EUR", "Cumhuriyet Altını"])
        if st.form_submit_button("Ekle"):
            st.session_state.sahsi_borclar.append({"Kişi": s_kisi, "Kime": s_isim, "Tutar": s_tutar, "Birim": s_birim})

# SABİT GİDER EKLEME FORMU
with st.sidebar.expander("Sabit Gider Ekle"):
    with st.form("gider_form", clear_on_submit=True):
        sg_kisi = st.selectbox("Kimin Gideri? (Örn: Ortak Kasa veya Kişisel)", st.session_state.uyeler)
        sg_isim = st.text_input("Gider Adı (Örn: Elektrik, Kurs)")
        sg_tutar = st.number_input("Aylık Tutar (TL)", min_value=0, step=100)
        if st.form_submit_button("Ekle"):
            st.session_state.sabit_giderler.append({"Kişi": sg_kisi, "Adı": sg_isim, "Tutar": sg_tutar})

# --- ANA EKRAN VE ANALİZ MANTIKLARI ---
df_gelir = pd.DataFrame(st.session_state.gelirler) if st.session_state.gelirler else pd.DataFrame(columns=["Kişi", "Adı", "Tutar", "Gün"])
df_banka = pd.DataFrame(st.session_state.bankalar) if st.session_state.bankalar else pd.DataFrame(columns=["Kişi", "Banka", "Tür", "Aylık Yük", "Faiz %"])
df_sahsi = pd.DataFrame(st.session_state.sahsi_borclar) if st.session_state.sahsi_borclar else pd.DataFrame(columns=["Kişi", "Kime", "Tutar", "Birim"])
df_sabit = pd.DataFrame(st.session_state.sabit_giderler) if st.session_state.sabit_giderler else pd.DataFrame(columns=["Kişi", "Adı", "Tutar"])

toplam_aylik_gelir = df_gelir['Tutar'].sum() if not df_gelir.empty else 0
toplam_sabit_gider = df_sabit['Tutar'].sum() if not df_sabit.empty else 0
toplam_banka_aylik = df_banka['Aylık Yük'].sum() if not df_banka.empty else 0
aylik_zorunlu_cikis = toplam_sabit_gider + toplam_banka_aylik
net_nakit_akisi = toplam_aylik_gelir - aylik_zorunlu_cikis

# 1. TEMEL GÖSTERGELER (TÜM EVİN BİLANÇOSU)
st.subheader("🏠 Evin Toplam Bilançosu")
col1, col2, col3 = st.columns(3)
col1.metric("Evin Toplam Geliri", f"{toplam_aylik_gelir:,.0f} TL")
col2.metric("Evin Toplam Gideri (Banka+Sabit)", f"{aylik_zorunlu_cikis:,.0f} TL")
col3.metric("Evin Net Nakit Akışı", f"{net_nakit_akisi:,.0f} TL", delta=float(net_nakit_akisi))
st.markdown("---")

# 2. SEKMELER VE HANE HALKI ANALİZİ
tab1, tab2, tab3 = st.tabs(["👤 Hane Halkı (Kişi Bazlı) Analiz", "🏦 Banka ve Borçlar", "📝 Gelir/Gider Dökümü"])

with tab1:
    st.markdown("### Kişi Bazlı Finansal Performans")
    if not df_gelir.empty or not df_sabit.empty or not df_banka.empty:
        # Kişilere göre gelir toplama
        gelir_kisi = df_gelir.groupby("Kişi")["Tutar"].sum().reset_index() if not df_gelir.empty else pd.DataFrame(columns=["Kişi", "Tutar"])
        gelir_kisi.rename(columns={"Tutar": "Toplam Gelir"}, inplace=True)
        
        # Kişilere göre banka ve sabit giderleri toplama
        gider_banka_kisi = df_banka.groupby("Kişi")["Aylık Yük"].sum().reset_index() if not df_banka.empty else pd.DataFrame(columns=["Kişi", "Aylık Yük"])
        gider_sabit_kisi = df_sabit.groupby("Kişi")["Tutar"].sum().reset_index() if not df_sabit.empty else pd.DataFrame(columns=["Kişi", "Tutar"])
        
        # Giderleri birleştirme
        gider_df = pd.merge(gider_banka_kisi, gider_sabit_kisi, on="Kişi", how="outer").fillna(0)
        gider_df["Toplam Gider"] = gider_df["Aylık Yük"] + gider_df["Tutar"]
        
        # Gelir ve Gideri birleştirip Net Durumu bulma
        analiz_df = pd.merge(gelir_kisi, gider_df[["Kişi", "Toplam Gider"]], on="Kişi", how="outer").fillna(0)
        analiz_df["Net Durum"] = analiz_df["Toplam Gelir"] - analiz_df["Toplam Gider"]
        
        st.dataframe(analiz_df.style.highlight_min(subset=['Net Durum'], color='lightcoral').highlight_max(subset=['Net Durum'], color='lightgreen'), use_container_width=True)
        
        st.info("💡 **Yorumlama:** Yukarıdaki tablo evin içindeki yükün kimin omuzlarında olduğunu gösterir. 'Net Durum'u negatif olan kişi, evin diğer gelirlerinden veya Ortak Kasa'dan finanse edilmek zorundadır.")
    else:
        st.write("Henüz yeterli veri girilmedi.")

with tab2:
    st.markdown("### Tüm Banka ve Elden Borçlar")
    col_b, col_s = st.columns(2)
    with col_b:
        st.write("**Banka Portföyü**")
        st.dataframe(df_banka, use_container_width=True)
    with col_s:
        st.write("**Şahsi (Kur Riskli) Borçlar**")
        st.dataframe(df_sahsi, use_container_width=True)

with tab3:
    col_g, col_gd = st.columns(2)
    with col_g:
        st.write("**Tüm Gelirler**")
        st.dataframe(df_gelir, use_container_width=True)
    with col_gd:
        st.write("**Tüm Sabit Giderler**")
        st.dataframe(df_sabit, use_container_width=True)

if st.button("Tüm Verileri Temizle"):
    st.session_state.clear()
    st.rerun()
