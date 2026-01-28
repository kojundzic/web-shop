import streamlit as st
import streamlit.components.v1 as components
import smtplib
import time
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - UPDATED WITH INFO TAB
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
    
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.9); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 80%; max-width: 600px; background: white; border: 10px solid #28a745;
        border-radius: 40px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; text-align: center; padding: 40px;
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

# --- PRIJEVODI ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚠️ INFORMACIJE", "nav_info": "ℹ️ O NAMA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "title": "KOJUNDŽIĆ", "subtitle": "MESNICA I PRERADA MESA SISAK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "info_vaga": "### ⚖️ Vagana roba\nKod artikala poput voća, povrća ili mesa, gotovo je nemoguće pogoditi točnu gramažu (npr. tražite 500g, dobijete 520g), što mijenja konačnu cijenu.",
        "success": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_info_tab": "⚠️ INFORMATION", "nav_info": "ℹ️ ABOUT US", "nav_con": "📞 CONTACT", "nav_lang": "🌍 LANGUAGE",
        "title": "KOJUNDŽIĆ", "subtitle": "BUTCHERY & MEAT PROCESSING SISAK",
        "cart_title": "🛒 CART", "total": "Informative Total", "btn_order": "PLACE ORDER",
        "info_vaga": "### ⚖️ Weighted Goods\nFor items like meat, it is almost impossible to hit the exact weight (e.g., you ask for 500g, you get 520g), which changes the final price.",
        "success": "ORDER PLACED SUCCESSFULLY!<br><br>THANK YOU!"
    }
}

if 'lang' not in st.session_state: st.session_state.lang = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG[st.session_state.lang]

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.order_done = False
    st.rerun()

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">{L["title"]}</div><div class="luxury-subtitle">{L["subtitle"]}</div></div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs([L["nav_shop"], L["nav_info_tab"], L["nav_info"], L["nav_con"], L["nav_lang"]])

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
                            c1, c2, c3 = st.columns([1,1,1])
                            if c1.button("➖", key=f"m_{nz}"):
                                if nz in st.session_state.cart:
                                    st.session_state.cart[nz] -= (0.5 if info['jedinica'] == "kg" else 1.0)
                                    if st.session_state.cart[nz] <= 0: del st.session_state.cart[nz]
                                    st.rerun()
                            val = st.session_state.cart.get(nz, 0.0)
                            c2.markdown(f"<h3 style='text-align:center;margin:0;'>{val}</h3>", unsafe_allow_html=True)
                            if c3.button("➕", key=f"p_{nz}"):
                                st.session_state.cart[nz] = st.session_state.cart.get(nz, 0.0) + (0.5 if info['jedinica'] == "kg" else 1.0)
                                st.rerun()
    with col_k:
        st.header(L["cart_title"])
        ukupno = 0.0
        if not st.session_state.cart:
            st.info("Košarica je prazna.")
        else:
            for s, k in st.session_state.cart.items():
                iznos = k * PROIZVODI[s]["cijena"]
                ukupno += iznos
                st.write(f"**{s}** ({k} {PROIZVODI[s]['jedinica']}) = {iznos:.2f} €")
            st.divider()
            st.subheader(f"{L['total']}: {ukupno:.2f} €")
            with st.form("order_f"):
                ime = st.text_input("Ime i Prezime")
                mob = st.text_input("Mobitel")
                adr = st.text_area("Adresa")
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr and mob:
                        sadrzaj = f"Kupac: {ime}\nMob: {mob}\nAdresa: {adr}\n\nNarudžba:\n" + "\n".join([f"- {k}: {v}" for k, v in st.session_state.cart.items()])
                        if posalji_email(f"Narudžba: {ime}", sadrzaj):
                            st.session_state.cart = {}
                            st.session_state.order_done = True
                            st.rerun()

# --- 2. INFORMACIJE (Novo dodano) ---
with tabs[1]:
    st.header("⚖️ Informacije o vaganju")
    st.info(L["info_vaga"])

# --- 3. O NAMA ---
with tabs[2]:
    st.write("Obiteljska tradicija Kojundžić ponosni je nositelj kvalitete...")

# --- 4. KONTAKT ---
with tabs[3]:
    st.write("📍 Gradska tržnica Sisak | 📞 +385 44 123 456")

# --- 5. JEZIK ---
with tabs[4]:
    novo = st.radio("Jezik / Language", ["HR 🇭🇷", "EN 🇬🇧"], index=0 if st.session_state.lang == "HR 🇭🇷" else 1)
    if novo != st.session_state.lang:
        st.session_state.lang = novo
        st.rerun()
