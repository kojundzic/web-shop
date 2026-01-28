import streamlit as st
import streamlit.components.v1 as components
import smtplib
import time
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - ULTIMATE EMAIL & CONTACT EDITION
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica i prerada mesa", 
    page_icon="🥩", 
    layout="wide"
)

# --- KONFIGURACIJA EMAILA (Secrets) ---
# Na Streamlit Cloudu dodaj u Secrets:
# moj_email = "tvoj@email.com"
# moja_lozinka = "tvoja_aplikacijska_lozinka"

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
    
    /* Tamnozeleni gumb za narudžbu */
    div.stButton > button[key="btn_final_order"] {
        background-color: #1e4620 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 50px !important;
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

DRZAVE = sorted(["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Španjolska", "Švedska"])

# --- TEKSTOVI ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_ug": "🏨 ZA UGOSTITELJE", "nav_dob": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "title": "KOJUNDŽIĆ", "subtitle": "MESNICA I PRERADA MESA SISAK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "note": "### ⚖️ Važna napomena\nCijene su točne, a konačan iznos računa saznat ćete pri dostavi. Pokušat ćemo biti što bliži traženoj količini i informativnom iznosu u eurima (€).",
        "success": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!",
        "about_txt": "### O nama i Lokacija\nObiteljska tradicija Kojundžić ponosni je nositelj kvalitete u Sisačko-moslavačkoj županiji. Naša primarna lokacija i prodajno mjesto nalazi se na **Gradskoj tržnici Sisak**, gdje svakodnevno nudimo svježe i suhomesnate delicije. Naša vizija je povratak autentičnih okusa u svaki dom.",
        "ugostitelji_txt": "### Za ugostitelje\nNudimo specijalizirane rezove, dry-age zrenje i prioritetnu dostavu za restorane i hotele. Naša logistika osigurava svježinu u ranojutarnjim satima.",
        "dob_txt": "### Dobavljači\nSurađujemo isključivo s lokalnim OPG-ovima. Naša stoka se hrani prirodno, bez GMO dodataka, na otvorenim ispašama.",
        "haccp_txt": "### HACCP Sigurnost\nNaš pogon u Sisku implementira stroge HACCP standarde. Svaki korak proizvodnje je pod digitalnim nadzorom stručnjaka.",
        "con_txt": "### Kontaktirajte nas\nImate li pitanja? Pošaljite nam poruku izravno putem forme ispod ili nas nazovite na +385 44 123 456."
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_ug": "🏨 FOR CHEFS", "nav_dob": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US", "nav_con": "📞 CONTACT", "nav_lang": "🌍 LANGUAGE",
        "title": "KOJUNDŽIĆ", "subtitle": "BUTCHERY & MEAT PROCESSING SISAK",
        "cart_title": "🛒 CART", "total": "Informative Total", "btn_order": "PLACE ORDER",
        "note": "### ⚖️ Note\nPrices are accurate; final amount confirmed at delivery. We aim for precision in Euro (€).",
        "success": "ORDER PLACED SUCCESSFULLY!<br><br>THANK YOU!",
        "about_txt": "### About Us & Location\nKojundžić family tradition. Find us at the **Sisak City Market**. Our mission is bringing authentic flavors to your home.",
        "ugostitelji_txt": "### For Chefs\nCustom cuts and dry-aging for restaurants and hotels. Fast morning delivery.",
        "dob_txt": "### Suppliers\nExclusively local farms, GMO-free and natural feeding.",
        "haccp_txt": "### HACCP Safety\nOur facility follows strict HACCP guidelines for maximum food safety.",
        "con_txt": "### Contact Us\nSend us a direct message using the form below."
    }
}

if 'lang' not in st.session_state: st.session_state.lang = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG[st.session_state.lang]

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.order_done = False
    st.rerun()

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">{L["title"]}</div><div class="luxury-subtitle">{L["subtitle"]}</div></div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs([L["nav_shop"], L["nav_ug"], L["nav_dob"], L["nav_haccp"], L["nav_info"], L["nav_con"], L["nav_lang"]])

# --- TRGOVINA ---
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
                                curr = st.session_state.cart.get(nz, 0.0)
                                st.session_state.cart[nz] = 1.0 if curr == 0 and info['jedinica'] == "kg" else curr + (0.5 if info['jedinica'] == "kg" else 1.0)
                                st.rerun()

    with col_k:
        st.header(L["cart_title"])
        ttl = 0
        if not st.session_state.cart: st.warning("Vaša košarica je trenutno prazna.")
        else:
            for n, q in st.session_state.cart.items():
                s = q * PROIZVODI[n]["cijena"]
                ttl += s
                st.write(f"🥩 **{n}** ({q}{PROIZVODI[n]['jedinica']}) = {s:.2f} €")
            if st.button("🗑️ Obriši sve", key="clear"):
                st.session_state.cart = {}
                st.rerun()
        
        st.subheader(f"{L['total']}: {ttl:.2f} €")
        st.info(L["note"])
        st.divider()
        st.header("📍 Podaci")
        f_ime = st.text_input("Ime i prezime*")
        f_drz = st.selectbox("Država*", DRZAVE, index=DRZAVE.index("Hrvatska"))
        f_grd = st.text_input("Grad*")
        f_pbr = st.text_input("Poštanski broj*")
        f_adr = st.text_input("Adresa*")
        f_mob = st.text_input("Mobitel*")
        
        valid = all([f_ime, f_grd, f_pbr, f_adr, f_mob]) and len(st.session_state.cart) > 0
        if st.button(L["btn_order"], key="btn_final_order", disabled=not valid, use_container_width=True):
            detalji = f"KUPAC: {f_ime}\nADRESA: {f_adr}, {f_pbr} {f_grd}, {f_drz}\nMOB: {f_mob}\n\nROBA:\n"
            for n, q in st.session_state.cart.items(): detalji += f"- {n}: {q}\n"
            if posalji_email(f"Nova Narudžba: {f_ime}", detalji):
                st.session_state.order_done = True
                st.session_state.cart = {}
                st.rerun()
            else: st.error("Greška pri slanju maila.")

# --- OSTALI TABOVI ---
with tabs[1]: st.markdown(L["ugostitelji_txt"])
with tabs[2]: st.markdown(L["dob_txt"])
with tabs[3]: st.markdown(L["haccp_txt"])
with tabs[4]: 
    st.markdown(L["about_txt"])
    st.markdown("### 📍 Tržnica Sisak")
    components.html('<iframe src="https://www.google.com" width="100%" height="400" style="border:0; border-radius:15px;"></iframe>', height=420)
with tabs[5]:
    st.markdown(L["con_txt"])
    with st.form("contact"):
        c_ime = st.text_input("Vaše ime")
        c_mail = st.text_input("Vaš e-mail")
        c_msg = st.text_area("Poruka")
        if st.form_submit_button("POŠALJI UPIT"):
            if posalji_email(f"Upit od: {c_ime}", f"Od: {c_mail}\n\nPoruka:\n{c_msg}"):
                st.success("Upit poslan!")
            else: st.error("Greška.")
with tabs[6]:
    nova = st.radio("Jezik / Language:", list(LANG.keys()), index=list(LANG.keys()).index(st.session_state.lang))
    if nova != st.session_state.lang:
        st.session_state.lang = nova
        st.rerun()
