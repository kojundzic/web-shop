import streamlit as st
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - FINAL STABLE EDITION
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

# --- CUSTOM CSS (Tvoj izvorni stil) ---
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
DRZAVE = sorted(["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Španjolska", "Švedska"])

# --- PRIJEVODI I TEKSTOVI (200+ riječi) ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_ug": "🏨 ZA UGOSTITELJE", "nav_dob": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HIGIJENA", "nav_info": "ℹ️ O NAMA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "title": "KOJUNDŽIĆ", "subtitle": "MESNICA I PRERADA MESA SISAK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Plaćanje:** Isključivo pouzećem (gotovinom prilikom preuzimanja).",
        "note": "### ⚖️ Napomena o vaganim proizvodima\nKod artikala poput mesa i suhomesnatih proizvoda, zbog specifičnosti rezanja nemoguće je postići u gram preciznu težinu. Iz tog je razloga iznos u vašoj košarici informativne prirode. Prilikom pripreme vaše narudžbe nastojat ćemo maksimalno poštovati tražene količine kako bi konačan račun bio što bliži informativnom iznosu koji vidite u košarici. Točan iznos računa za meso i dostavu paketa znati ćete kada vam dostavna služba dostavi paket. Hvala na razumijevanju.",
        "about_txt": "Obiteljski posao Kojundžić ponosno stoji kao simbol tradicije u Sisačko-moslavačkoj županiji već generacijama. Naša proizvodnja temelji se isključivo na tradicionalnom načinu prerade mesa, onako kako su to radili naši stari, bez korištenja industrijskih kemikalija, umjetnih bojila ili ubrzanih procesa zrenja. Svaki komad mesa koji izađe iz naše obiteljske radionice u Sisku plod je ručnog rada, golemog strpljenja i dubokog poštovanja prema zanatu koji polako nestaje. Dimljenje obavljamo na prirodnom drvu bukve i grabovine, što našim proizvodima daje onu specifičnu, bogatu aromu i teksturu koju je nemoguće postići u modernim industrijskim pogonima. Kao obitelj, izravno smo uključeni u svaki korak procesa – od pažljivog odabira najbolje sirovine od lokalnih uzgajivača do finalnog pakiranja za naše vjerne kupce na gradskoj tržnici. Vjerujemo da se vrhunska kvaliteta ne može požuriti, zbog čega svaka kobasica, panceta ili hamburger prolaze kroz prirodan, spori proces sušenja. Naša misija je očuvanje autentičnih okusa sisačkog kraja te njihovo prenošenje budućim generacijama koje cijene pošten, domaći proizvod. Kojundžić ime jamči vam svježinu koja dolazi iz srca naše obitelji izravno na vaš stol.",
        "dob_txt": "Kvaliteta našeg mesa počinje na prostranim i čistim pašnjacima **Parka prirode Lonjsko polje**, **Posavine** i **Banovine**. Surađujemo isključivo s lokalnim OPG-ovima koji dijele našu viziju o etičkom i prirodnom uzgoju stoke. Naši dobavljači dolaze iz regija poznatih po netaknutoj prirodi, gdje životinje borave na otvorenom tijekom većeg dijela godine, hraneći se prirodnom ispašom bez GMO dodataka. Lonjsko polje pruža specifičnu mikroklimu koja našem mesu daje jedinstvenu mramoriranost i bogatstvo nutrijenata. Podržavanjem malih uzgajivača s Banovine i Posavine osiguravamo da novac ostaje u lokalnoj zajednici te potičemo opstanak ruralnih krajeva. Naš lanac opskrbe je kratak i transparentan – meso ne putuje tisućama kilometara u hladnjačama, već stiže svježe izravno s pašnjaka u našu preradu. Svaki kupac kupnjom kod nas izravno pomaže očuvanju tradicije stočarstva u ovim povijesnim hrvatskim regijama.",
        "haccp_txt": "Higijena i sigurnost hrane u mesnici Kojundžić predstavljaju nulti prioritet od kojeg nikada ne odstupamo. U našem modernom pogonu u Sisku implementirali smo stroge HACCP protokole koji prate svaki korak proizvodnog procesa, od ulaza sirovine do krajnje dostave na vaš prag. Naša predanost čistoći nadilazi puko ispunjavanje zakonskih normi – mi to vidimo kao moralnu obvezu prema našim kupcima. Svaki alat i radna površina dezinficiraju se svakodnevno, a procesi obrade odvijaju se u strogo kontroliranim temperaturnim uvjetima. Redovito vršimo mikrobiološka ispitivanja u ovlaštenim laboratorijima kako bismo osigurali apsolutnu zdravstvenu ispravnost. Vaše povjerenje gradimo na besprijekornoj čistoći i tehnologiji koja štiti tradiciju.",
        "success": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!",
        "con_msg": "Pošaljite nam upit izravno:", "con_btn": "Pošalji e-mail"
    }
}

# --- SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG.get(st.session_state.lang, LANG["HR 🇭🇷"])

# --- SUCCESS OVERLAY ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(4); st.session_state.order_done = False; st.rerun()

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">{L["title"]}</div><div class="luxury-subtitle">{L["subtitle"]}</div></div>', unsafe_allow_html=True)

# --- TABS (Popravljeno indeksiranje) ---
tabs = st.tabs([L["nav_shop"], L["nav_dob"], L["nav_haccp"], L["nav_info"], L["nav_con"], L["nav_lang"]])

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

# --- 2. DOBAVLJAČI ---
with tabs[1]:
    st.header(L["nav_dob"])
    st.write(L["dob_txt"])

# --- 3. HIGIJENA ---
with tabs[2]:
    st.header(L["nav_haccp"])
    st.write(L["haccp_txt"])

# --- 4. O NAMA & INFO VAGA ---
with tabs[3]:
    st.markdown(L["note"])
    st.divider()
    st.header(L["nav_info"])
    st.write(L["about_txt"])

# --- 5. KONTAKT & KARTA ---
with tabs[4]:
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

# --- 6. JEZIK ---
with tabs[5]:
    st.header(L["nav_lang"])
    novo = st.radio("Jezik:", ["HR 🇭🇷", "EN 🇬🇧"])
    if novo != st.session_state.lang:
        st.session_state.lang = novo; st.rerun()
