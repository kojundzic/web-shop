import streamlit as st
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - ULTIMATE INTERNATIONAL EDITION
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
    div.stButton > button { border-radius: 10px !important; font-weight: bold; height: 3em; }
    .success-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0,0,0,0.9); z-index: 9999; display: flex; justify-content: center; align-items: center; }
    .success-modal { width: 15cm; height: 10cm; background: white; border: 10px solid #28a745; border-radius: 40px; text-align: center; padding: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- PROIZVODI ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"}
}

DRZAVE_LISTA = ["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Španjolska", "Švedska"]

# --- TEKSTOVI I PRIJEVODI ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚖️ INFORMACIJE", "nav_dob": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HIGIJENA", "nav_about": "ℹ️ O NAMA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "title": "KOJUNDŽIĆ", "subtitle": "MESNICA I PRERADA MESA SISAK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Plaćanje:** Isključivo pouzećem.",
        "vaga_text": """### ⚖️ Napomena o vaganim proizvodima\nKod artikala poput mesa i suhomesnatih proizvoda, zbog specifičnosti rezanja nemoguće je postići u gram preciznu težinu. Iz tog je razloga iznos u vašoj košarici informativne prirode. Prilikom pripreme vaše narudžbe nastojat ćemo maksimalno poštovati tražene količine kako bi konačan račun bio što bliži informativnom iznosu koji vidite u košarici. Točan iznos računa za meso i dostavu paketa znati ćete kada vam dostavna služba dostavi paket. Hvala na razumijevanju.""",
        "about_txt": """Obiteljski posao Kojundžić generacijama predstavlja simbol tradicije u Sisačko-moslavačkoj županiji. Naša proizvodnja temelji se isključivo na tradicionalnim metodama koje isključuju industrijsku masovnu preradu. Svaki komad mesa plod je strpljenja i ručnog rada, dimljen na prirodnom drvu bukve i grabovine, što našim proizvodima daje aromu djetinjstva. Ponosni smo na naš obiteljski pristup gdje je kvaliteta ispred kvantitete.""",
        "dob_txt": """Kvaliteta našeg asortimana započinje na nepreglednim pašnjacima **Parka prirode Lonjsko polje**, **Posavine** i **Banovine**. Ovi su krajevi poznati po stoljetnoj tradiciji stočarstva i netaknutoj prirodi. Surađujemo isključivo s lokalnim OPG-ovima koji dijele našu viziju slobodnog uzgoja stoke. Životinje borave na otvorenom tijekom cijele godine, hraneći se prirodnim plodovima zemlje bez GMO dodataka. Lonjsko polje, kao jedno od najvećih zaštićenih vlažnih staništa u Europi, daruje specifičnu mikroklimu koja meso čini mramoriranim i iznimno ukusnim. Podupiranjem uzgajivača s Banovine i Posavine izravno utječemo na očuvanje ruralnog života i tradicionalnih pasmina, osiguravajući vam sljedivost i sigurnost u podrijetlo svakog komada mesa koji kupite. Naš lanac opskrbe je kratak – od polja do naše obiteljske prerade put traje minimalno, čime zadržavamo svu nutritivnu vrijednost i svježinu sirovine.""",
        "haccp_txt": """Sigurnost hrane i besprijekorna higijena temelj su povjerenja koje gradimo s našim kupcima. U našem modernom pogonu u Sisku implementirali smo stroge HACCP standarde koji prate svaki korak – od ulaska sirovine do finalne dostave. Naš higijenski režim uključuje svakodnevnu rigoroznu dezinfekciju svih radnih površina i alata, te digitalni nadzor temperature u svakom trenutku. Razumijemo da rad sa svježim i suhomesnatim proizvodima zahtijeva maksimalnu odgovornost, stoga naši djelatnici prolaze redovite edukacije o sanitarnim protokolima. Čistoća naših prostora za zrenje i dimljenje jamči da tradicionalni procesi teku u sanitarno sigurnim uvjetima. Svaki paket koji šaljemo pripremljen je u kontroliranim uvjetima, uz neprekinuti hladni lanac, osiguravajući da do vašeg stola stigne proizvod koji je ne samo vrhunskog okusa, već i zdravstveno besprijekoran. Vaše zdravlje i zadovoljstvo naša su najveća nagrada.""",
        "success": "USPJEŠNO POSLANO!", "con_msg": "Kontaktirajte nas:", "con_btn": "Pošalji"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_info_tab": "⚖️ INFOS", "nav_dob": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HYGIENE", "nav_about": "ℹ️ ÜBER UNS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 SPRACHE",
        "title": "KOJUNDŽIĆ", "subtitle": "METZGEREI & FLEISCHVERARBEITUNG SISAK",
        "cart_title": "🛒 WARENKORB", "total": "Informativer Betrag", "btn_order": "BESTELLUNG SENDEN",
        "pay_note": "💳 **Zahlung:** Ausschließlich per Nachnahme.",
        "vaga_text": """### ⚖️ Hinweis zu gewogenen Produkten\nBei Fleisch- und Wurstwaren ist es aufgrund des Zuschnitts unmöglich, ein grammgenaues Gewicht zu erreichen. Der Betrag im Warenkorb ist informativ. Wir bemühen uns, die Mengen einzuhalten, damit die Endabrechnung so nah wie möglich am informativen Betrag liegt. Den genauen Betrag erfahren Sie bei der Lieferung. Vielen Dank.""",
        "about_txt": """Das Familienunternehmen Kojundžić steht seit Generationen für Tradition in der Gespanschaft Sisak-Moslavina. Unsere Produktion basiert auf traditionellen Methoden ohne industrielle Massenverarbeitung. Jedes Stück Fleisch ist das Ergebnis von Geduld und Handarbeit, geräuchert über Buchen- und Hainbuchenholz.""",
        "dob_txt": """Die Qualität beginnt auf den Weiden des **Naturparks Lonjsko Polje**, der **Posavina** und **Banovina**. Diese Regionen sind bekannt für ihre jahrhundertealte Tradition der Viehzucht. Wir arbeiten ausschließlich mit lokalen Bauernhöfen zusammen, die unsere Vision der Freilandhaltung teilen. Die Tiere fressen natürliches Futter ohne Gentechnik. Lonjsko Polje, eines der größten geschützten Feuchtgebiete Europas, bietet ein Mikroklima, das das Fleisch besonders schmackhaft macht. Durch die Unterstützung der Züchter in Banovina und Posavina sichern wir die Rückverfolgbarkeit und Sicherheit jedes Fleischstücks, das Sie kaufen. Unsere Lieferkette ist kurz – vom Feld bis zur Verarbeitung dauert es nur kurze Zeit, wodurch Nährwert und Frische erhalten bleiben.""",
        "haccp_txt": """Lebensmittelsicherheit und einwandfreie Hygiene sind die Basis des Vertrauens. In unserem Werk in Sisak haben wir strenge HACCP-Standards implementiert, die jeden Schritt überwachen. Unser Hygieneregime umfasst die tägliche rigorose Desinfektion aller Arbeitsflächen und Werkzeuge sowie eine digitale Temperaturüberwachung. Wir verstehen, dass die Arbeit mit frischen Produkten maximale Verantwortung erfordert. Die Sauberkeit unserer Reife- und Räucherräume garantiert, dass die traditionellen Prozesse unter sicheren Bedingungen ablaufen. Jedes Paket wird unter kontrollierten Bedingungen vorbereitet, um sicherzustellen, dass ein Produkt von höchster Qualität und Gesundheitssicherheit Ihren Tisch erreicht.""",
        "success": "ERFOLGREICH GESENDET!", "con_msg": "Kontaktieren Sie uns:", "con_btn": "Senden"
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
    time.sleep(3); st.session_state.order_done = False; st.rerun()

# --- UI HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">{L["title"]}</div><div class="luxury-subtitle">{L["subtitle"]}</div></div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs([L["nav_shop"], L["nav_info_tab"], L["nav_dob"], L["nav_haccp"], L["nav_about"], L["nav_con"], L["nav_lang"]])

# --- 1. SHOP & FIXIRANA KOŠARICA ---
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
                            st.write(f"**{info['cijena']:.2f} € / {info['jedinica']}**")
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
        if not st.session_state.cart: st.info("Prazno / Leer")
        else:
            for s, k in st.session_state.cart.items():
                st.write(f"**{s}** ({k}) = {k*PROIZVODI[s]['cijena']:.2f} €")
            st.divider()
            st.subheader(f"{L['total']}: {total:.2f} €")
            st.info(L["pay_note"])
            with st.form("order_form"):
                st.write("### Podaci za dostavu / Lieferdaten")
                ime = st.text_input("Ime i Prezime / Name")
                tel = st.text_input("Mobitel / Telefon")
                adr = st.text_area("Adresa / Adresse")
                grad = st.selectbox("Država / Land", DRZAVE_LISTA)
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr and tel:
                        msg = f"Kupac: {ime}\nTel: {tel}\nAdresa: {adr}, {grad}\n\nStavke: {st.session_state.cart}"
                        if posalji_email(f"Nova narudžba ({grad}) - {ime}", msg):
                            st.session_state.cart = {}; st.session_state.order_done = True; st.rerun()

with tabs[1]: st.markdown(L["vaga_text"])
with tabs[2]: st.header(L["nav_dob"]); st.write(L["dob_txt"])
with tabs[3]: st.header(L["nav_haccp"]); st.write(L["haccp_txt"])
with tabs[4]: st.header(L["nav_about"]); st.write(L["about_txt"])

with tabs[5]:
    st.header(L["nav_con"])
    c1, c2 = st.columns(2)
    with c1:
        st.write("📍 **Gradska tržnica Sisak / Stadtmarkt Sisak**")
        st.write("📞 +385 44 123 456")
        with st.form("contact_form"):
            c_ime = st.text_input("Ime / Name")
            c_msg = st.text_area("Poruka / Nachricht")
            if st.form_submit_button(L["con_btn"]):
                if posalji_email(f"Upit - {c_ime}", c_msg): st.success("Poslano! / Gesendet!")
    with c2:
        st.map(pd.DataFrame({'lat': [45.4851], 'lon': [16.3725]}))

with tabs[6]:
    novo = st.radio("Jezik / Sprache / Language:", ["HR 🇭🇷", "DE 🇩🇪", "EN 🇬🇧"])
    if novo != st.session_state.lang:
        st.session_state.lang = novo; st.rerun()
