import streamlit as st
import smtplib
from email.mime.text import MIMEText

# =================================================================
# 🛡️ TRAJNO USIDRENA KONFIGURACIJA - KOJUNDŽIĆ SISAK 2026. FINAL
# =================================================================

MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EU_DRZAVE = [
    "Hrvatska", "Austrija", "Belgija", "Bugarska", "Cipar", "Češka", "Danska", 
    "Estonija", "Finska", "Francuska", "Njemačka", "Slovenija", "Italija"
]

# --- KOMPLETAN RJEČNIK SA SVIM ISPRAVCIMA ---
LANG = {
    "HR 🇭🇷": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je prazna.",
        "unit_kg": "kg", "note_vaga": "⚖️ Cijene su točne, odstupanja su minimalna zbog ručne obrade.",
        "form_title": "📍 PODACI ZA DOSTAVU",
        "fname": "Ime*", "lname": "Prezime*", "tel": "Kontakt telefon*", "country": "Država*", "city": "Grad*", "addr": "Ulica i broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success_msg": "Narudžba zaprimljena! Hvala na povjerenju.",
        "haccp_txt": "### Beskompromisna sigurnost hrane\nImplementirani HACCP sustav temelj je našeg poslovanja. Provodimo rigorozne kontrole u svakoj fazi – od ulaza sirovine do finalnog pakiranja.",
        "products": [
            "Dimljeni hamburger", "Dimljeni buncek", "Dimljeni prsni vršci", "Slavonska kobasica", 
            "Domaća salama", "Dimljene kosti", "Dimljene nogice mix", "Panceta", "Dimljeni vrat (BK)", 
            "Dimljeni kare (BK)", "Dimljena pečenica", "Domaći čvarci", "Svinjska mast (kanta)", 
            "Krvavice", "Pečenice za roštilj", "Suha rebra", "Dimljena glava", "Slanina sapunara"
        ]
    },
    "EN 🇬🇧": {
        "title": "KOJUNDŽIĆ Butchery | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "cart_title": "🛒 Your Cart", "cart_empty": "Cart is empty.",
        "unit_kg": "kg", "note_vaga": "⚖️ Prices are exact, weight may vary slightly due to manual processing.",
        "form_title": "📍 DELIVERY INFO",
        "fname": "First Name*", "lname": "Last Name*", "tel": "Phone*", "country": "Country*", "city": "City*", "addr": "Address*",
        "btn_order": "🚀 PLACE ORDER", "success_msg": "Order received! Thank you.",
        "haccp_txt": "### Uncompromising Food Safety\nThe implemented HACCP system is the foundation of our business. We conduct rigorous controls at every stage.",
        "products": [
            "Smoked Hamburger", "Smoked Pork Hock", "Smoked Brisket Tips", "Slavonian Sausage", 
            "Homemade Salami", "Smoked Bones", "Smoked Trotters Mix", "Pancetta", "Smoked Neck", 
            "Smoked Loin", "Smoked Tenderloin", "Pork Rinds", "Lard", "Blood Sausages", 
            "Grilling Sausages", "Dry Ribs", "Smoked Pig Head", "Bacon"
        ]
    }
}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide", page_icon="🥩")

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- NAVIGACIJA ---
sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", ["HR 🇭🇷", "EN 🇬🇧"])
L = LANG[sel_lang]
page = st.sidebar.radio("Navigacija", [L["nav_shop"], L["nav_horeca"], L["nav_haccp"], L["nav_info"]])

# --- TRGOVINA ---
if page == L["nav_shop"]:
    st.title(L["title"])
    st.info(L["note_vaga"])
    
    cols = st.columns(3)
    for i, prod in enumerate(L["products"]):
        with cols[i % 3]:
            st.write(f"**{prod}**")
            qty = st.number_input(f"{L['unit_kg']}", min_value=0.0, step=0.1, key=f"q_{prod}")
            if st.button(f"Dodaj", key=f"b_{prod}"):
                if qty > 0:
                    st.session_state.cart[prod] = qty
                    st.toast(f"✅ {prod}")

# --- HACCP ---
elif page == L["nav_haccp"]:
    st.title(L["nav_haccp"])
    st.markdown(L["haccp_txt"])

# --- O NAMA / HORECA ---
else:
    st.title(page)
    st.write("Tradicija i kvaliteta obitelji Kojundžić - Sisak 2026.")

# --- SIDEBAR KOŠARICA I SLANJE ---
st.sidebar.divider()
st.sidebar.header(L["cart_title"])

if not st.session_state.cart:
    st.sidebar.write(L["cart_empty"])
else:
    stavke_mail = ""
    for p, q in list(st.session_state.cart.items()):
        if q > 0:
            st.sidebar.write(f"🔹 {p}: {q} kg")
            stavke_mail += f"- {p}: {q} kg\n"
    
    if st.sidebar.button("🗑️ Isprazni"):
        st.session_state.cart = {}
        st.rerun()

    st.sidebar.divider()
    with st.sidebar.form("order_form"):
        fn = st.text_input(L["fname"])
        ln = st.text_input(L["lname"])
        ph = st.text_input(L["tel"])
        ct = st.selectbox(L["country"], EU_DRZAVE)
        city = st.text_input(L["city"])
        adr = st.text_input(L["addr"])
        
        if st.form_submit_button(L["btn_order"]):
            if all([fn, ln, ph, adr]):
                tijelo = f"NARUDŽBA 2026\n\nKupac: {fn} {ln}\nTel: {ph}\nAdresa: {adr}, {city}, {ct}\n\nStavke:\n{stavke_mail}"
                msg = MIMEText(tijelo)
                msg['Subject'] = f"Nova narudžba: {fn} {ln}"
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
