import streamlit as st
import smtplib
from email.mime.text import MIMEText

# =================================================================
# 🛡️ KOJUNDŽIĆ SISAK 2026. - FINALNA VERZIJA S VAGOM I OPISIMA
# =================================================================

MOJ_EMAIL = st.secrets["moj_email"]
MOJA_LOZINKA = st.secrets["moja_lozinka"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

st.set_page_config(page_title="KOJUNDŽIĆ Mesnica", page_icon="🥩", layout="wide")

# --- VIŠEJEZIČNI RJEČNIK ---
LANG = {
    "HR 🇭🇷": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "note_vaga": "⚖️ **VAŽNO:** Cijene su točne, ali zbog ručne obrade težina može minimalno odstupati. Račun s točnim iznosom dobivate u paketu.",
        "note_cod": "🚚 Plaćanje pouzećem (gotovina)",
        "form_title": "📍 PODACI ZA DOSTAVU",
        "btn_order": "🚀 POŠALJI NARUDŽBU",
        "about_txt": "### Obiteljska tradicija i vizija\nObitelj Kojundžić generacijama predstavlja sinonim za vrhunsku mesnu struku u Sisačko-moslavačkoj županiji...",
        "haccp_txt": "### Beskompromisna sigurnost hrane\nU pogonima Kojundžić sigurnost potrošača je imperativ. Implementirani HACCP sustav temelj je našeg poslovanja."
    }
}

# --- POPIS PROIZVODA ---
PROIZVODI = {
    "Dimljeni hamburger (1kg)": 15.00,
    "Panceta (1kg)": 12.00,
    "Čvarci (1kg)": 5.00,
    "Suha rebra (1kg)": 9.00,
    "Domaća mast (1kg)": 10.00,
    "Slavonska kobasica (1kg)": 8.50,
    "Dimljeni buncek (1kg)": 9.00
}

# --- IZBORNIK ---
sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", ["HR 🇭🇷"])
L = LANG[sel_lang]

tab1, tab2, tab3, tab4 = st.tabs([L["nav_shop"], L["nav_horeca"], L["nav_haccp"], L["nav_info"]])

with tab1:
    st.title(L["title"])
    st.info(L["note_vaga"])
    
    if 'cart' not in st.session_state:
        st.session_state.cart = {}

    cols = st.columns(3)
    for idx, (proizvod, cijena) in enumerate(PROIZVODI.items()):
        with cols[idx % 3]:
            st.write(f"### {proizvod}")
            st.write(f"Cijena: **{cijena:.2f} €**")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"➕ Dodaj", key=f"add_{proizvod}"):
                    trenutna = st.session_state.cart.get(proizvod, 0)
                    st.session_state.cart[proizvod] = 1.0 if trenutna == 0 else trenutna + 0.5
                    st.rerun()
            with c2:
                if st.button(f"➖ Smanji", key=f"rem_{proizvod}"):
                    trenutna = st.session_state.cart.get(proizvod, 0)
                    if trenutna > 1.0: st.session_state.cart[proizvod] = trenutna - 0.5
                    elif trenutna == 1.0: del st.session_state.cart[proizvod]
                    st.rerun()

            if proizvod in st.session_state.cart:
                st.success(f"U košarici: **{st.session_state.cart[proizvod]} kg**")

    st.divider()
    st.header(L["cart_title"])
    if not st.session_state.cart:
        st.write(L["cart_empty"])
    else:
        ukupno = 0
        detalji = ""
        for s, k in st.session_state.cart.items():
            iznos = k * PROIZVODI[s]
            ukupno += iznos
            st.write(f"✅ {s} x {k} = **{iznos:.2f} €**")
            detalji += f"- {s} x {k}\n"
        
        st.write(f"### Ukupno: {ukupno:.2f} €")
        
        with st.form("order_form"):
            st.write(L["form_title"])
            ime = st.text_input("Ime i Prezime*")
            adresa = st.text_input("Adresa i Grad*")
            tel = st.text_input("Mobitel*")
            st.warning(L["note_cod"])
            if st.form_submit_button(L["btn_order"]):
                if ime and adresa and tel:
                    try:
                        msg = MIMEText(f"KUPAC: {ime}\nADRESA: {adresa}\nTEL: {tel}\n\nROBA:\n{detalji}")
                        msg['Subject'] = f"Narudžba: {ime}"
                        msg['From'], msg['To'] = MOJ_EMAIL, MOJ_EMAIL
                        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                        s.starttls()
                        s.login(MOJ_EMAIL, MOJA_LOZINKA)
                        s.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                        s.quit()
                        st.balloons()
                        st.success("Narudžba poslana!")
                        st.session_state.cart = {}
                    except Exception as e: st.error(f"Greška: {e}")
                else: st.error("Ispunite polja!")

with tab2: st.write("### HORECA"); st.write("Kontaktirajte nas za ponudu za restorane.")
with tab3: st.write(L["haccp_txt"])
with tab4: st.write(L["about_txt"])
