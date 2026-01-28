import streamlit as st
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - INFORMATION TAB UPDATE
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica i prerada mesa", 
    page_icon="🥩", 
    layout="wide"
)

# --- KONFIGURACIJA EMAILA ---
def posalji_email(predmet, poruka):
    try:
        primatelj = st.secrets["moj_email"]
        posiljatelj = st.secrets["moj_email"]
        lozinka = st.secrets["moja_lozinka"]
        msg = MIMEText(poruka, 'plain', 'utf-8')
        msg['Subject'] = predmet
        msg['From'] = posiljatelj
        msg['To'] = primatelj
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(posiljatelj, lozinka)
        server.sendmail(posiljatelj, primatelj, msg.as_string())
        server.quit()
        return True
    except:
        return False

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .main-header { text-align: center; padding: 30px; background: #fcfcfc; border-bottom: 3px solid #1e4620; margin-bottom: 20px; }
    .luxury-title { font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 900; color: #1a1a1a; text-transform: uppercase; }
    .luxury-subtitle { font-family: 'Lato', sans-serif; font-size: 16px; color: #1e4620; letter-spacing: 4px; }
    div.stButton > button[key="btn_final_order"] {
        background-color: #1e4620 !important; color: white !important;
        font-weight: bold !important; border-radius: 10px !important; height: 50px !important;
    }
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.9); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 15cm; height: 10cm; background: white; border: 10px solid #28a745;
        border-radius: 40px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; text-align: center; padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PODACI ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"}
}

# --- TEKSTOVI I PRIJEVODI ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚖️ INFORMACIJE", "nav_dob": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HIGIJENA", "nav_about": "ℹ️ O NAMA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "title": "KOJUNDŽIĆ", "subtitle": "MESNICA I PRERADA MESA SISAK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Plaćanje:** Isključivo pouzećem (gotovinom prilikom preuzimanja).",
        "vaga_text": """### ⚖️ Napomena o vaganim proizvodima
Kod artikala poput mesa i suhomesnatih proizvoda, zbog specifičnosti rezanja nemoguće je postići u gram preciznu težinu. Iz tog je razloga iznos u vašoj košarici informativne prirode. Prilikom pripreme vaše narudžbe nastojat ćemo maksimalno poštovati tražene količine kako bi konačan račun bio što bliži informativnom iznosu koji vidite u košarici. Točan iznos računa za meso i dostavu paketa znati ćete kada vam dostavna služba dostavi paket. Hvala na razumijevanju.""",
        "about_txt": "Obiteljski posao Kojundžić ponosno stoji kao simbol tradicije u Sisačko-moslavačkoj županiji već generacijama. Naša proizvodnja temelji se isključivo na tradicionalnom načinu prerade mesa, onako kako su to radili naši stari, bez korištenja industrijskih kemikalija, umjetnih bojila ili ubrzanih procesa zrenja. Svaki komad mesa koji izađe iz naše obiteljske radionice u Sisku plod je ručnog rada, golemog strpljenja i dubokog poštovanja prema zanatu koji polako nestaje...",
        "dob_txt": "Kvaliteta našeg mesa počinje na prostranim i čistim pašnjacima **Parka prirode Lonjsko polje**, **Posavine** i **Banovine**. Surađujemo isključivo s lokalnim OPG-ovima koji dijele našu viziju o etičkom i prirodnom uzgoju stoke...",
        "haccp_txt": "Higijena i sigurnost hrane u mesnici Kojundžić predstavljaju nulti prioritet od kojeg nikada ne odstupamo. U našem modernom pogonu u Sisku implementirali smo stroge HACCP protokole...",
        "success": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!",
        "con_msg": "Pošaljite nam upit izravno:", "con_btn": "Pošalji e-mail"
    }
}

if 'lang' not in st.session_state: st.session_state.lang = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG.get(st.session_state.lang, LANG["HR 🇭🇷"])

# --- SUCCESS OVERLAY ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(4); st.session_state.order_done = False; st.rerun()

# --- UI HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">{L["title"]}</div><div class="luxury-subtitle">{L["subtitle"]}</div></div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs([L["nav_shop"], L["nav_info_tab"], L["nav_dob"], L["nav_haccp"], L["nav_about"], L["nav_con"], L["nav_lang"]])

# --- 1. SHOP & CART ---
with tabs[0]:
    col_t, col_k = st.columns([1.4, 1], gap="large")
    with col_t:
        st.header(L["nav_shop"])
        itms = list(PROIZVODI.items())
        for i in range(0, len(itms), 2):
            r = st.columns(2)
            for j in range(2):
                if i+j < len(itms):
                    nz, info = itms[i+j]
                    with r[j]:
                        with st.container(border=True):
                            st.subheader(nz)
                            st.write(f"Cijena: **{info['cijena']:.2f} € / {info['jedinica']}**")
                            c1, c2, c3 = st.columns(3)
                            if c1.button("➖", key=f"m_{nz}"):
                                if nz in st.session_state.cart:
                                    st.session_state.cart[nz] -= (0.5 if info['jedinica'] == "kg" else 1.0)
                                    if st.session_state.cart[nz] <= 0: del st.session_state.cart[nz]
                                    st.rerun()
                            val = st.session_state.cart.get(nz, 0.0)
                            c2.markdown(f'<div style="text-align:center;font-weight:bold;font-size:20px;">{val}</div>', unsafe_allow_html=True)
                            if c3.button("➕", key=f"p_{nz}"):
                                st.session_state.cart[nz] = st.session_state.cart.get(nz, 0.0) + (0.5 if info['jedinica'] == "kg" else 1.0)
                                st.rerun()
    with col_k:
        st.header(L["cart_title"])
        total = sum(k * PROIZVODI[s]["cijena"] for s, k in st.session_state.cart.items())
        if not st.session_state.cart: st.info("Košarica je prazna.")
        else:
            for s, k in st.session_state.cart.items():
                st.write(f"**{s}** ({k}) = {k*PROIZVODI[s]['cijena']:.2f} €")
            st.divider()
            st.subheader(f"{L['total']}: {total:.2f} €")
            st.warning(L["pay_note"])
            with st.form("order_form"):
                ime = st.text_input("Ime i Prezime")
                tel = st.text_input("Mobitel")
                adr = st.text_area("Adresa dostave")
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr and tel:
                        msg = f"Kupac: {ime}\nTel: {tel}\nAdresa: {adr}\n\nStavke: {st.session_state.cart}"
                        if posalji_email(f"Nova narudžba - {ime}", msg):
                            st.session_state.cart = {}; st.session_state.order_done = True; st.rerun()

# --- 2. NOVI TAB: INFORMACIJE ---
with tabs[1]:
    st.header(L["nav_info_tab"])
    st.markdown(L["vaga_text"])

# --- 3. DOBAVLJAČI ---
with tabs[2]:
    st.header(L["nav_dob"])
    st.write(L["dob_txt"])

# --- 4. HIGIJENA ---
with tabs[3]:
    st.header(L["nav_haccp"])
    st.write(L["haccp_txt"])

# --- 5. O NAMA ---
with tabs[4]:
    st.header(L["nav_about"])
    st.write(L["about_txt"])

# --- 6. KONTAKT ---
with tabs[5]:
    st.header(L["nav_con"])
    c1, c2 = st.columns(2)
    with c1:
        st.write("📍 **Gradska tržnica Sisak**")
        st.write("📞 +385 44 123 456")
        st.divider()
        st.subheader(L["con_msg"])
        with st.form("direct_contact"):
            c_ime = st.text_input("Ime")
            c_email = st.text_input("Vaš E-mail")
            c_msg = st.text_area("Poruka")
            if st.form_submit_button(L["con_btn"]):
                if posalji_email(f"Upit - {c_ime}", f"Od: {c_email}\n\n{c_msg}"):
                    st.success("Poruka poslana!")
    with c2:
        st.map(pd.DataFrame({'lat': [45.4851], 'lon': [16.3725]}))

# --- 7. JEZIK ---
with tabs[6]:
    st.header(L["nav_lang"])
    novo = st.radio("Jezik:", ["HR 🇭🇷", "EN 🇬🇧"])
    if novo != st.session_state.lang:
        st.session_state.lang = novo; st.rerun()
