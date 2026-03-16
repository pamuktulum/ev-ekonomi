import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Finansal Yönetim Paneli", layout="wide")
st.title("🏦 Akıllı Finansal Yönetim ve Optimizasyon Paneli")

# --- YAN PANEL (GİRDİLER) ---
st.sidebar.header("📊 1. Güncel Piyasa Verileri")
kur_euro = st.sidebar.number_input("1 Euro (TL)", value=50.71, step=0.1)
kur_altin = st.sidebar.number_input("1 Cumhuriyet Altını (TL)", value=48342.0, step=100.0)

st.sidebar.header("💰 2. Aylık Gelirler")
maas = st.sidebar.number_input("Maaş (TL)", value=140000)
emekli_maasi = st.sidebar.number_input("Emekli Maaşı (TL)", value=48000)
toplam_gelir = maas + emekli_maasi

st.sidebar.header("💸 3. Aylık Giderler (Taksit + Sabit)")
sabit_gider = st.sidebar.number_input("Aylık Sabit Giderler (Fatura, Kurs vb.)", value=18750)
kredi_taksit = st.sidebar.number_input("Aylık Kredi Taksitleri Toplamı", value=82500)
kart_asgari = st.sidebar.number_input("Kredi Kartı Asgarileri Toplamı", value=48500)
aylik_zorunlu_gider = sabit_gider + kredi_taksit + kart_asgari

st.sidebar.header("🤝 4. Şahsi Borçlar")
mahir_euro = st.sidebar.number_input("Mahir (Euro)", value=1100)
betul_altin = st.sidebar.number_input("Betül (Adet Altın)", value=4)
serkan_tl = st.sidebar.number_input("Serkan (TL)", value=70000)

# --- ANA EKRAN (ANALİZ VE SONUÇLAR) ---
net_nakit = toplam_gelir - aylik_zorunlu_gider

col1, col2, col3 = st.columns(3)
col1.metric("Toplam Aylık Gelir", f"{toplam_gelir:,.0f} TL")
col2.metric("Zorunlu Giderler", f"{aylik_zorunlu_gider:,.0f} TL")
col3.metric("Aylık Net Nakit Fazlası", f"{net_nakit:,.0f} TL", delta=float(net_nakit))

st.markdown("---")
st.subheader("📌 Öncelikli Ödeme Planı ve Strateji")

if net_nakit > 0:
    st.success(f"Harika! Her ay elinizde **{net_nakit:,.0f} TL** stratejik nakit gücü kalıyor. Bu gücü aşağıdaki sırayla kullanmalısınız:")
    
    # Şahsi borçların güncel TL karşılıkları
    mahir_tl = mahir_euro * kur_euro
    betul_tl = betul_altin * kur_altin
    
    st.markdown(f"""
    **1. SIRA: Gecikmeler (Varsa)**
    Kredi notunu korumak için sistemde geçmişten sarkan gecikme varsa önce o kapatılmalı.
    
    **2. SIRA: Mahir'in Euro Borcu (Açık Pozisyon Riski)**
    * **Güncel Tutar:** {mahir_tl:,.0f} TL ({mahir_euro} EUR)
    * **Aksiyon:** Aylık kalan {net_nakit:,.0f} TL ile her ay fiziki Euro alınarak bu kur riski hemen eritilmeli.
    
    **3. SIRA: Betül'ün Altın Borcu (Emtia Riski)**
    * **Güncel Tutar:** {betul_tl:,.0f} TL ({betul_altin} Altın)
    * **Aksiyon:** Mahir bittikten sonra kalan nakitle düzenli fiziki altın alınarak altın borcu kapatılmalı.
    
    **4. SIRA: Serkan'ın TL Borcu**
    * **Güncel Tutar:** {serkan_tl:,.0f} TL
    * **Aksiyon:** Enflasyon karşısında eridiği için en son sıraya bırakılmalı. (Eylül'de kredi bitince tek seferde ödenebilir).
    """)
    
    st.info("💡 **Hazine Yönetimi Kuralı:** Ayın 10'unda maaş yattığında, acil ödemeler dışındaki tüm parayı Ek Hesaba (KMH) yatırın. Ödeme günleri geldiğinde parayı KMH'tan kullanın. Bu sayede aylık binlerce lira faiz tasarrufu sağlarsınız.")

else:
    st.error(f"DİKKAT! Aylık nakit akışınız negatif ({net_nakit:,.0f} TL). Sistem her ay kendi kendine borç üretiyor. Giderleri kısmalı veya gelir artırıcı önlemler almalısınız.")
