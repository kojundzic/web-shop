import streamlit as st
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - PROFESSIONAL FINAL EDITION
# =================================================================

st.set_page_config(page_title="KOJUNDŽIĆ Mesnica", page_icon="🥩", layout="wide")

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
    except: return False

# --- TEKSTOVI (Puna verzija 200+ riječi) ---
CONTENT = {
    "Hrvatska": {
        "about": """Obiteljska tradicija Kojundžić predstavlja stup kvalitete u Sisačko-moslavačkoj županiji već desetljećima. Naša priča duboko je ukorijenjena u tradicionalnim metodama prerade mesa koje su se prenosile s koljena na koljeno. U današnjem svijetu brze industrije, mi smo odabrali put strpljenja – ručnu obradu, prirodno dimljenje na drvu bukve i grabovine te prirodno zrenje bez umjetnih aditiva. Naš obiteljski posao jamči da svaki komad mesa koji izađe iz naše prerade posjeduje autentičan miris i okus domaćeg ognjišta. Proizvodnja se odvija u Sisku, gdje s posebnom pažnjom biramo najbolje komade sirovine kako bismo osigurali vrhunski gastronomski doživljaj za naše kupce na Gradskoj tržnici. Ponosni smo što možemo reći da u naše proizvode ne stavljamo ništa što ne bismo dali vlastitoj djeci. Transparentnost, povjerenje i neupitna svježina naši su prioriteti. Svaki hamburger, panceta ili kobasica nosi potpis naše obitelji, simbolizirajući spoj tradicije, poštenog rada i ljubavi prema zanatu koji polako izumire, a koji mi ljubomorno čuvamo za vas.""",
        "suppliers": """Kvaliteta našeg mesa počinje na prostranim i čistim pašnjacima Parka prirode Lonjsko polje, Posavine i Banovine. Surađujemo isključivo s lokalnim uzgajivačima i OPG-ovima koji dijele našu viziju slobodnog uzgoja stoke u prirodnom okruženju. Lonjsko polje, kao jedno od najvećih zaštićenih poplavnih područja u Europi, pruža specifičnu mikroklimu i bogatstvo ispaše koja rezultira mesom vrhunske teksture i nutritivne vrijednosti. Naši partneri iz Banovine i Posavine stočari su s višegodišnjim iskustvom, čija se stoka hrani isključivo domaćim žitaricama bez GMO dodataka. Ovakav kratki lanac opskrbe omogućuje nam maksimalnu svježinu – meso ne putuje tisućama kilometara, već stiže izravno s naših polja u našu preradu u Sisku. Podržavanjem lokalne poljoprivrede ne samo da osiguravamo najbolju sirovinu, već i aktivno sudjelujemo u očuvanju ruralnog života i tradicije našeg kraja. Svaki kupac kupnjom kod nas izravno pomaže opstanku malih domaćih proizvođača i očuvanju ekološke ravnoteže ovih predivnih regija.""",
        "hygiene": """U mesnici Kojundžić, higijena i sigurnost hrane nisu samo zakonska obveza, već temeljna vrijednost našeg poslovanja. Naš moderni pogon u Sisku implementirao je najstrože HACCP standarde sigurnosti hrane, osiguravajući besprijekornu čistoću u svakoj sekundi proizvodnog procesa. Od rigorozne kontrole pri ulasku sirovine do digitalno nadziranog hladnog lanca, svaki korak je pod stalnim nadzorom stručnjaka. Naša oprema se dezinficira svakodnevno najsuvremenijim metodama, a svi zaposlenici redovito prolaze edukacije o najvišim sanitarnim standardima. Razumijemo osjetljivost svježeg i suhomesnatog programa, stoga koristimo tehnologiju koja osigurava maksimalnu zaštitu od kontaminacije uz očuvanje tradicionalnog okusa. Redovita mikrobiološka testiranja u neovisnim laboratorijima jamče da je svaki naš proizvod zdravstveno ispravan i spreman za vaš stol bez ikakvog rizika. Vaše zdravlje naša je najveća briga, a naša nulta tolerancija na higijenske propuste osigurava da mesnica Kojundžić ostane sinonim za sigurnu i vrhunsku domaću hranu kojoj možete potpuno vjerovati."""
    }
}

# --- PRIJEVODI NAVIGACIJE ---
LANG = {
    "Hrvatska": {
        "nav_shop": "🏬 TRGOVINA", "nav_info": "ℹ️ O NAMA", "nav_supp": "🚜 DOBAVLJAČI", "nav_hyg": "🛡️ HIGIJENA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Plaćanje:** Isključivo pouzećem (gotovinom pri dostavi).",
        "info_vaga": "### ⚖️ Napomena o vaganju\nZbog specifičnosti rezanja mesa, nemoguće je postići točnu gramažu. Iznos je informativan, a točan račun saznat ćete pri dostavi.",
        "success": "USPJEŠNO POSLANO!", "client_data": "Podaci za dostavu", "con_send": "Pošalji e-mail"
    },
    "Njemačka": {
        "nav_shop": "🏬 SHOP", "nav_info": "ℹ️ ÜBER UNS", "nav_supp": "🚜 LIEFERANTEN", "nav_hyg": "🛡️ HYGIENE", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 SPRACHE",
        "cart_title": "🛒 WARENKORB", "total": "Informativer Betrag", "btn_order": "BESTELLEN",
        "pay_note": "💳 **Zahlung:** Nur per Nachnahme.",
        "info_vaga": "### ⚖️ Gewichtshinweis\nExaktes Gewicht ist beim Fleischzuschnitt nicht möglich. Der Betrag ist informativ.",
        "success": "ERFOLGREICH GESENDET!", "client_data": "Lieferdaten", "con_send": "E-Mail senden"
    }
}

# --- SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = "Hrvatska"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG.get(st.session_state.lang, LANG["Hrvatska"])
txt = CONTENT.get("Hrvatska") # (Za ostale jezike ovdje bi išla logika prijevoda)

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .main-header { text-align: center; padding: 30px; border-bottom: 3px solid #1e4620; }
    .luxury-title { font-family: 'Playfair Display', serif; font-size: 52px; text-transform: uppercase; }
    div.stButton > button { border-radius: 10px !important; font-weight: bold; background-color: #1e4620; color: white; }
    .stTabs [aria-selected="true"] { background-color: #1e4620 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">KOJUNDŽIĆ</div><p style="letter-spacing:4px;">TRADICIJSKA PRERADA MESA SISAK</p></div>', unsafe_allow_html=True)

tabs = st.tabs([L["nav_shop"], "⚠️ INFO", L["nav_info"], L["nav_supp"], L["nav_hyg"], L["nav_con"], L["nav_lang"]])

# --- 1. SHOP & CART (Sve vidljivo) ---
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
                                    st.session_state.cart[nz] -= 0.5
                                    if st.session_state.cart[nz] <= 0: del st.session_state.cart[nz]
                                    st.rerun()
                            c2.markdown(f"<h3 style='text-align:center;'>{st.session_state.cart.get(nz, 0.0)}</h3>", unsafe_allow_html=True)
                            if c3.button("➕", key=f"p_{nz}"):
                                st.session_state.cart[nz] = st.session_state.cart.get(nz, 0.0) + 0.5
                                st.rerun()
    with col_k:
        st.header(L["cart_title"])
        total = sum(k * PROIZVODI[s]["cijena"] for s, k in st.session_state.cart.items())
        if not st.session_state.cart: st.info("Košarica je prazna.")
        else:
            for s, k in st.session_state.cart.items():
                st.write(f"**{s}** ({k} kg/kom) = {k*PROIZVODI[s]['cijena']:.2f} €")
            st.divider()
            st.subheader(f"{L['total']}: {total:.2f} €")
            st.warning(L["pay_note"])
            with st.form("delivery_f"):
                st.write(f"### {L['client_data']}")
                ime = st.text_input("Ime i Prezime")
                tel = st.text_input("Mobitel")
                adr = st.text_area("Adresa dostave")
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr:
                        if posalji_email(f"Narudžba {ime}", f"Kupac: {ime}\nAdresa: {adr}\nNarudžba: {st.session_state.cart}"):
                            st.session_state.order_done = True
                            st.session_state.cart = {}
                            st.rerun()

# --- 2. INFORMACIJE O VAGANJU ---
with tabs[1]:
    st.markdown(L["info_vaga"])

# --- 3. O NAMA ---
with tabs[2]:
    st.header(L["nav_info"])
    st.write(txt["about"])

# --- 4. DOBAVLJAČI ---
with tabs[3]:
    st.header(L["nav_supp"])
    st.write(txt["suppliers"])

# --- 5. HIGIJENA ---
with tabs[4]:
    st.header(L["nav_hyg"])
    st.write(txt["hygiene"])

# --- 6. KONTAKT & DIREKTAN EMAIL ---
with tabs[5]:
    st.header(L["nav_con"])
    c1, c2 = st.columns(2)
    with c1:
        st.write("📍 **Gradska tržnica Sisak**")
        st.write("📞 +385 44 123 456")
        st.divider()
        st.subheader(L["con_send"])
        with st.form("contact_direct"):
            c_ime = st.text_input("Ime")
            c_email = st.text_input("Vaš E-mail")
            c_msg = st.text_area("Vaša poruka")
            if st.form_submit_button("POŠALJI PORUKU"):
                if posalji_email(f"Upit: {c_ime}", f"Od: {c_email}\n\n{c_msg}"):
                    st.success("Poruka poslana!")
    with c2:
        st.map(pd.DataFrame({'lat': [45.4851], 'lon': [16.3725]}))

# --- 7. JEZIK ---
with tabs[6]:
    st.header(L["nav_lang"])
    novo = st.selectbox("Odaberite državu", ["Hrvatska", "Njemačka", "Austrija", "Italija"])
    if novo != st.session_state.lang:
        st.session_state.lang = novo
        st.rerun()

# --- SUCCESS ---
if st.session_state.order_done:
    st.success(L["success"])
    time.sleep(3)
    st.session_state.order_done = False
    st.rerun()
