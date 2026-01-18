import streamlit as st
import smtplib
from email.mime.text import MIMEText

# =================================================================
# 🛡️ FINALNA USIDRENA VERZIJA - KOJUNDŽIĆ SISAK 2026. (v.17.11.23:59)
# =================================================================

MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EU_DRZAVE = ["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Mađarska", "Slovačka", "Češka", "Poljska"]

# --- KOMPLETAN VIŠEJEZIČNI SUSTAV ---
LANG = {
    "HR 🇭🇷": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je prazna.",
        "unit_kg": "kg", "note_vaga": "⚖️ VAŽNO: Zbog ručne obrade, težina može minimalno odstupati.",
        "form_title": "📍 PODACI ZA DOSTAVU",
        "fname": "Ime*", "lname": "Prezime*", "tel": "Kontakt telefon*", "country": "Država*", "city": "Grad*", "addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success_msg": "Narudžba zaprimljena, hvala!",
        "horeca_txt": "### HORECA Partnerstvo\nNudimo precizno rezanje i stabilnu opskrbu za hotele i restorane uz kontrolirane temperaturne uvjete.",
        "haccp_txt": "### HACCP Standardi\nSvaki komad mesa je pod stalnim mikrobiološkim nadzorom. Sigurnost hrane je naš prioritet.",
        "products": [
            "Dimljeni hamburger", "Dimljeni buncek", "Slavonska kobasica", "Domaća salama", 
            "Panceta", "Domaći čvarci", "Svinjska mast (kanta)", "Krvavice", 
            "Dimljene kosti", "Dimljene nogice mix", "Pečenice za roštilj", "Suha rebra", "Dimljena glava"
        ]
    },
    "EN 🇬🇧": {
        "title": "KOJUNDŽIĆ Butchery & Processing | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is empty.",
        "unit_kg": "kg", "note_vaga": "⚖️ IMPORTANT: Weight may vary slightly due to manual cutting.",
        "form_title": "📍 DELIVERY INFO",
        "fname": "First Name*", "lname": "Last Name*", "tel": "Phone*", "country": "Country*", "city": "City*", "addr": "Address*",
        "btn_order": "🚀 PLACE ORDER", "success_msg": "Order received, thank you!",
        "horeca_txt": "### HORECA Partnership\nWe provide precision cutting and stable supply for hotels and restaurants.",
        "haccp_txt": "### HACCP Standards\nFull traceability and microbiological control of every product.",
        "products": [
            "Smoked Hamburger", "Smoked Pork Hock", "Slavonian Sausage", "Homemade Salami", 
            "Pancetta", "Pork Rinds", "Lard (Bucket)", "Blood Sausages", 
            "Smoked Bones", "Smoked Trotters Mix", "Grilling Sausages", "Dry Ribs", "Smoked Pig Head"
        ]
    },
    "DE 🇩🇪": {
        "title": "KOJUNDŽIĆ Metzgerei | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Warenkorb ist leer.",
        "unit_kg": "kg", "note_vaga": "⚖️ WICHTIG: Das Gewicht kann variieren.",
        "form_title": "📍 LIEFERDATEN",
        "fname": "Vorname*", "lname": "Nachname*", "tel": "Telefon*", "country": "Land*", "city": "Stadt*", "addr": "Straße*",
        "btn_order": "🚀 BESTELLEN", "success_msg": "Bestellung erhalten, danke!",
        "horeca_txt": "### HORECA Partnerschaft\nPräzisionsschnitt und stabile Versorgung für Gastronomie.",
        "haccp_txt": "### HACCP-Standards\nZertifizierte Prozesse und mikrobiologische Kontrolle.",
        "products": [
            "Geräucherter Hamburger", "Geräucherter Schinken", "Slavonische Wurst", "Hausgemachte Salami", 
            "Pancetta", "Grieben", "Schweineschmalz", "Blutwurst", 
            "Räucherknochen", "Schweinefüße Mix", "Grillwürste", "Trockenrippen", "Geräucherter Schweinekopf"
        ]
    }
}

# --- APLIKACIJSKO SUČELJE ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide", page_icon="🥩")

if "cart" not in st.session_state:
    st.session_state.cart = {}

# Sidebar navigacija
st.sidebar.title("KOJUNDŽIĆ 2026")
sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", list(LANG.keys()))
L = LANG[sel_lang]
page = st.sidebar.radio("Navigacija", [L["nav_shop"], L["nav_horeca"], L["nav_haccp"], L["nav_info"]])

# --- STRANICA TRGOVINA ---
if page == L["nav_shop"]:
    st.title(L["title"])
    st.info(L["note_vaga"])
    cols = st.columns(3)
    for i, prod in enumerate(L["products"]):
        with cols[i % 3]:
            st.subheader(prod)
            qty = st.number_input(f"Količina ({L['unit_kg']})", min_value=0.0, step=0.5, key=f"q_{prod}")
            if st.button(f"Dodaj / Add {prod}", key=f"b_{prod}"):
                if qty > 0:
                    st.session_state.cart[prod] = qty
                    st.toast(f"✅ {prod} dodan u košaricu")

# --- OSTALE SEKCIJE ---
elif page == L["nav_horeca"]:
    st.title(L["nav_horeca"])
    st.markdown(L["horeca_txt"])
elif page == L["nav_haccp"]:
    st.title(L["nav_haccp"])
    st.markdown(L["haccp_txt"])
else:
    st.title(L["nav_info"])
    st.write("Obiteljska tradicija Kojundžić - Sisak. Kvaliteta bez kompromisa od pašnjaka do stola.")

# --- SIDEBAR KOŠARICA I SLANJE ---
st.sidebar.divider()
st.sidebar.header(L["cart_title"])

if not st.session_state.cart:
    st.sidebar.write(L["cart_empty"])
else:
    order_summary = ""
    for p, q in list(st.session_state.cart.items()):
        if q > 0:
            st.sidebar.write(f"🥩 **{p}**: {q} kg")
            order_summary += f"- {p}: {q} kg\n"
    
    if st.sidebar.button("🗑️ Isprazni košaricu"):
        st.session_state.cart = {}
        st.rerun()

    st.sidebar.divider()
    with st.sidebar.form("order_form"):
        st.write(L["form_title"])
        fn, ln = st.text_input(L["fname"]), st.text_input(L["lname"])
        ph = st.text_input(L["tel"])
        ct = st.selectbox(L["country"], EU_DRZAVE)
        city = st.text_input(L["city"])
        adr = st.text_input(L["addr"])
        
        if st.form_submit_button(L["btn_order"]):
            if fn and ln and ph and adr:
                body = f"NARUDŽBA 2026\n\nKupac: {fn} {ln}\nTel: {ph}\nAdresa: {adr}, {city}, {ct}\n\nStavke:\n{order_summary}"
                msg = MIMEText(body)
                msg['Subject'] = f"Nova narudžba: {fn} {ln}"
                msg['From'], msg['To'] = MOJ_EMAIL, MOJ_EMAIL
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    st.sidebar.success(L["success_msg"])
                    st.session_state.cart = {}
                    st.balloons()
                except Exception as e:
                    st.sidebar.error(f"Slanje nije uspjelo: {e}")
            else:
                st.sidebar.warning("Popunite sva obavezna polja!")
