import streamlit as st
import smtplib
from email.mime.text import MIMEText

# =================================================================
# 🛡️ TRAJNO ZAKLJUČANA KONFIGURACIJA - KOJUNDŽIĆ SISAK 2026.
# =================================================================

MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EU_DRZAVE = [
    "Hrvatska", "Austrija", "Belgija", "Bugarska", "Cipar", "Češka", "Danska", "Estonija", 
    "Finska", "Francuska", "Grčka", "Irska", "Italija", "Latvija", "Litva", "Luksemburg", 
    "Mađarska", "Malta", "Nizozemska", "Njemačka", "Poljska", "Portugal", "Rumunjska", 
    "Slovačka", "Slovenija", "Španjolska", "Švedska", "Druga država / Other"
]

# --- VIŠEJEZIČNI RJEČNIK ---
LANG = {
    "HR 🇭🇷": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_info": "ℹ️ O NAMA",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "unit_kg": "kg", "form_title": "📍 PODACI ZA DOSTAVU",
        "fname": "Ime*", "lname": "Prezime*", "tel": "Kontakt telefon*", "country": "Država*", "city": "Grad*", "addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success_msg": "Vaša narudžba je zaprimljena, hvala!",
        "products": [
            "Dimljeni hamburger", "Dimljeni buncek", "Dimljeni prsni vršci", "Slavonska kobasica", 
            "Domaća salama", "Dimljene kosti", "Dimljene nogice mix", "Panceta", "Dimljeni vrat (BK)", 
            "Dimljeni kare (BK)", "Dimljena pečenica", "Domaći čvarci", "Svinjska mast (kanta)", 
            "Krvavice", "Pečenice za roštilj", "Suha rebra", "Dimljena glava", "Slanina sapunara"
        ]
    },
    "EN 🇬🇧": {
        "title": "KOJUNDŽIĆ Meat Shop & Processing | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_info": "ℹ️ ABOUT US",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is currently empty.",
        "unit_kg": "kg", "form_title": "📍 DELIVERY INFORMATION",
        "fname": "First Name*", "lname": "Last Name*", "tel": "Phone*", "country": "Country*", "city": "City*", "addr": "Street & Number*",
        "btn_order": "🚀 PLACE ORDER", "success_msg": "Your order has been received, thank you!",
        "products": [
            "Smoked Hamburger", "Smoked Pork Hock", "Smoked Brisket Tips", "Slavonian Sausage", 
            "Homemade Salami", "Smoked Bones", "Smoked Trotters Mix", "Pancetta", "Smoked Neck (BK)", 
            "Smoked Loin (BK)", "Smoked Tenderloin", "Homemade Pork Rinds", "Lard (Bucket)", 
            "Blood Sausages", "Grilling Sausages", "Dry Ribs", "Smoked Pig Head", "Soap Bacon"
        ]
    }
}

# --- POSTAVKE STRANICE ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide", page_icon="🥩")

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- SIDEBAR ---
st.sidebar.header("Meni / Menu")
sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", ["HR 🇭🇷", "EN 🇬🇧"])
L = LANG[sel_lang]
page = st.sidebar.radio("Navigacija", [L["nav_shop"], L["nav_info"]])

# --- STRANICA: TRGOVINA ---
if page == L["nav_shop"]:
    st.title(L["title"])
    st.divider()
    
    cols = st.columns(3)
    for i, prod in enumerate(L["products"]):
        with cols[i % 3]:
            st.subheader(prod)
            qty = st.number_input(f"{L['unit_kg']}", min_value=0.0, step=0.5, key=f"q_{prod}")
            if st.button(f"Dodaj / Add", key=f"b_{prod}"):
                if qty > 0:
                    st.session_state.cart[prod] = qty
                    st.toast(f"Dodano: {prod}")

# --- STRANICA: O NAMA ---
else:
    st.title(L["nav_info"])
    st.write("Obitelj Kojundžić - Tradicija kvalitete od pašnjaka do stola. Sisak 2026.")

# --- DESNI PANEL: KOŠARICA I SLANJE ---
st.sidebar.divider()
st.sidebar.header(L["cart_title"])

if not st.session_state.cart:
    st.sidebar.info(L["cart_empty"])
else:
    email_text = ""
    for p, q in list(st.session_state.cart.items()):
        if q > 0:
            st.sidebar.write(f"✅ {p}: {q} kg")
            email_text += f"- {p}: {q} kg\n"
    
    if st.sidebar.button("Isprazni košaricu"):
        st.session_state.cart = {}
        st.rerun()

    st.sidebar.divider()
    with st.sidebar.form("order_form"):
        st.write(L["form_title"])
        f_name = st.text_input(L["fname"])
        l_name = st.text_input(L["lname"])
        phone = st.text_input(L["tel"])
        country = st.selectbox(L["country"], EU_DRZAVE)
        city = st.text_input(L["city"])
        addr = st.text_input(L["addr"])
        
        if st.form_submit_button(L["btn_order"]):
            if f_name and l_name and phone and addr:
                # Logika slanja maila
                full_body = f"Nova narudžba 2026:\n\nKupac: {f_name} {l_name}\nTel: {phone}\nAdresa: {addr}, {city}, {country}\n\nStavke:\n{email_text}"
                msg = MIMEText(full_body)
                msg['Subject'] = f"NARUDŽBA: {f_name} {l_name}"
                msg['From'] = MOJ_EMAIL
                msg['To'] = MOJ_EMAIL
                
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
                    st.sidebar.error(f"Greška: {e}")
            else:
                st.sidebar.error("Popunite sva polja!")
