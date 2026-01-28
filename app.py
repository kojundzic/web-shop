import streamlit as st
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - FIXED INDEX EDITION
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
    div.stButton > button { border-radius: 10px !important; }
    .success-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0,0,0,0.9); z-index: 9999; display: flex; justify-content: center; align-items: center; }
    .success-modal { width: 80%; max-width: 600px; background: white; border: 10px solid #28a745; border-radius: 40px; text-align: center; padding: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- PODACI O PROIZVODIMA ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"}
}

DRZAVE_LISTA = ["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Španjolska", "Švedska"]

# --- FUNKCIJA ZA DUGE TEKSTOVE ---
def GET_TEXT(tab, lang):
    hr_texts = {
        "about": """Obiteljski posao Kojundžić ponosno stoji kao simbol tradicije u Sisačko-moslavačkoj županiji...""",
        "suppliers": """Kvaliteta našeg mesa počinje na prostranim pašnjacima Parka prirode Lonjsko polje, Posavine i Banovine...""",
        "hygiene": """Higijena i sigurnost hrane u mesnici Kojundžić predstavljaju nulti prioritet..."""
    }
    en_texts = {
        "about": """The Kojundžić family business stands as a pillar of tradition in the Sisak-Moslavina County...""",
        "suppliers": """The quality of our meat starts in the vast pastures of the Lonjsko Polje Nature Park, Posavina, and Banovina...""",
        "hygiene": """Hygiene and food safety at the Kojundžić butchery are our zero-priority..."""
    }
    if lang == "Hrvatska": return hr_texts.get(tab, "")
    else: return en_texts.get(tab, "")

# --- PRIJEVODI ---
LANG = {
    "Hrvatska": {
        "nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚠️ INFORMACIJE", "nav_info": "ℹ️ O NAMA", "nav_supp": "🚜 DOBAVLJAČI", "nav_hyg": "🛡️ HIGIJENA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Način plaćanja:** Isključivo pouzećem.",
        "info_vaga": "### ⚖️ Napomena o vaganim proizvodima\n...",
        "success": "USPJEŠNO!<br><br>HVALA!", "client_info": "Podaci za dostavu",
        "con_msg": "Upit:", "con_btn": "Pošalji", "con_succ": "Poslano!"
    },
    # Dodajte ostale prijevode ovdje...
}

if 'lang' not in st.session_state: st.session_state.lang = "Hrvatska"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG.get(st.session_state.lang, LANG["Hrvatska"])

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(3); st.session_state.order_done = False; st.rerun()

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">KOJUNDŽIĆ</div><div class="luxury-subtitle">MESNICA I PRERADA MESA SISAK</div></div>', unsafe_allow_html=True)

# POPRAVAK: Definiranje tabova s indeksima
tabs = st.tabs([L["nav_shop"], L["nav_info_tab"], L["nav_info"], L.get("nav_supp", "🚜 DOBAVLJAČI"), L.get("nav_hyg", "🛡️ HIGIJENA"), L["nav_con"], L["nav_lang"]])

# --- 1. TRGOVINA ---
with tabs[0]:
    col_t, col_k = st.columns([1.5, 1], gap="large")
    with col_t:
        st.header(L["nav_shop"])
        itms = list(PROIZVODI.items())
        for i in range(0, len(itms), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(itms):
                    nz, info = itms[i+j]
                    with cols[j]:
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
                            c2.markdown(f"<h3 style='text-align:center;'>{val}</h3>", unsafe_allow_html=True)
                            if c3.button("➕", key=f"p_{nz}"):
                                st.session_state.cart[nz] = st.session_state.cart.get(nz, 0.0) + (0.5 if info['jedinica'] == "kg" else 1.0)
                                st.rerun()
    with col_k:
        st.header(L["cart_title"])
        ukupno = 0.0
        if not st.session_state.cart: st.info("Prazno")
        else:
            for s, k in st.session_state.cart.items():
                iznos = k * PROIZVODI[s]["cijena"]
                ukupno += iznos
                st.write(f"**{s}** ({k}) = {iznos:.2f} €")
            st.divider()
            st.subheader(f"{L['total']}: {ukupno:.2f} €")
            st.warning(L["pay_note"])
            with st.form("f_ord"):
                ime = st.text_input("Ime i Prezime")
                tel = st.text_input("Mobitel")
                adr = st.text_area("Adresa")
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr:
                        if posalji_email(f"Narudžba {ime}", f"Kupac: {ime}\nAdresa: {adr}\nTel: {tel}\nStavke: {st.session_state.cart}"):
                            st.session_state.cart = {}; st.session_state.order_done = True; st.rerun()

# --- 2. INFORMACIJE ---
with tabs[1]:
    st.markdown(L["info_vaga"])

# --- 3. O NAMA ---
with tabs[2]:
    st.header(L["nav_info"])
    st.write(GET_TEXT("about", st.session_state.lang))

# --- 4. DOBAVLJAČI ---
with tabs[3]:
    st.header(L.get("nav_supp", "🚜 DOBAVLJAČI"))
    st.write(GET_TEXT("suppliers", st.session_state.lang))

# --- 5. HIGIJENA ---
with tabs[4]:
    st.header(L.get("nav_hyg", "🛡️ HIGIJENA"))
    st.write(GET_TEXT("hygiene", st.session_state.lang))

# --- 6. KONTAKT ---
with tabs[5]:
    st.header(L["nav_con"])
    c1, c2 = st.columns()
    with c1:
        st.write("📍 **Gradska tržnica Sisak**")
        st.write("📞 +385 44 123 456")
        with st.form("contact_form"):
            c_ime = st.text_input("Ime")
            c_email = st.text_input("Email")
            c_poruka = st.text_area("Poruka")
            if st.form_submit_button(L.get("con_btn", "Pošalji")):
                if c_ime and c_email and c_poruka:
                    if posalji_email(f"Upit - {c_ime}", c_poruka):
                        st.success(L.get("con_succ", "Poslano!"))
    with c2:
        lokacija = pd.DataFrame({'lat': [45.4851], 'lon': [16.3725]})
        st.map(lokacija)

# --- 7. JEZIK ---
with tabs[6]:
    st.header(L["nav_lang"])
    odabir = st.selectbox("Država / Country", DRZAVE_LISTA, index=DRZAVE_LISTA.index(st.session_state.lang))
    if odabir != st.session_state.lang:
        st.session_state.lang = odabir
        st.rerun()
