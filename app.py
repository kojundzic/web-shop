import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (TRAJNO ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (HR, EN, DE - TRAJNO ZAKLJUČANO) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🧺", "cart_empty": "Košarica je trenutno prazna. Odaberite domaće delicije iz ponude!",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo nakon vaganja. 
        Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. 
        Mi ćemo se truditi da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "note_delivery": """🚚 **Dostava i plaćanje:** Naručene artikle dostaviti će Vam dostavna služba na kućnu adresu. 
        Alternativno, možete ih preusmjeriti u najbliži paketomat. Plaćanja se vrše **isključivo pouzećem** (prilikom preuzimanja paketa).""",
        "total": "Informativni iznos", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "Zaprimljeno! Kontaktirat ćemo Vas uskoro.",
        "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "tax": "PDV uključen", "shipping_info": "PODACI ZA DOSTAVU",
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "horeca_text": """Kao obiteljski posao, duboko cijenimo rad naših kolega u ugostiteljstvu. Razumijemo da vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom sirovinom. 
        \n**Što nudimo našim HoReCa partnerima u 2026. godini:**
        \n* **Autentični miris dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba, što Vašim jelima daje onaj prepoznatljiv, domaći potpis.
        \n* **Sigurna dostava:** Raspolažemo vlastitim vozilima s kontroliranim temperaturnim režimom (hladnjače), jamčeći svježinu u svakoj isporuci.
        \n* **Veleprodajna podrška:** Redovnim partnerima osiguravamo prioritetnu obradu narudžbi i stabilne uvjete poslovanja.""",
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "haccp_text": """U mesnici Kojundžić, higijena nije samo zakonska obveza, već temelj našeg obraza. U 2026. godini primjenjujemo najstrože standarde kontrole kvalitete.
        \n* **Potpuna sljedivost:** Svaki komad mesa u našoj ponudi ima svoj 'rodni list'. Točno znamo s koje farme dolazi i tko ga je uzgojio.
        \n* **Strogi HACCP protokoli:** Naš moderni pogon u Sisku pod stalnim je nadzorom. Svaki korak – od prijema stoke, preko zrenja i dimljenja, do finalnog pakiranja – odvija se u sterilnim i temperaturno kontroliranim uvjetima.""",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima.
        \n**Zašto odabrati nas?**
        \nVjerujemo da se prava kvaliteta ne može postići industrijskom brzinom. Naša stoka dolazi isključivo od malih, provjerenih uzgajivača s pašnjaka Lonjskog polja, Banovine i Posavine. Meso pripremamo polako, uz prirodne začine i bez nepotrebnih aditiva.""",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 FOR CATERERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🧺", "cart_empty": "Your basket is currently empty.",
        "note_vaga": """⚖️ **Note on weighing:** Prices are fixed, but the exact total will be known after weighing. Final amount upon delivery.""",
        "note_delivery": """🚚 **Delivery:** Items delivered to your address. Payments are **exclusively cash on delivery**.""",
        "total": "Informative amount", "form_name": "Full Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "Zip*", "form_addr": "Street*", "form_country": "Country*", 
        "btn_order": "🚀 SEND ORDER", "success": "Received!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "tax": "VAT incl.", "shipping_info": "SHIPPING DETAILS",
        "horeca_title": "Partnership based on trust and tradition", "haccp_title": "Food Safety", "info_title": "Our Story",
        "horeca_text": "As a family business, we deeply value our catering colleagues. Authentic smoke and safe delivery in 2026.",
        "haccp_text": "In 2026, we apply the strictest standards and full traceability.",
        "info_text": "Located in Sisak, we preserve traditional skills and use local livestock.",
        "p1": "Smoked bacon", "p2": "Smoked pork hock", "p3": "Smoked brisket tips", "p4": "Slavonian sausage", "p5": "Homemade salami", "p6": "Smoked bones",
        "p7": "Pork feet mix", "p8": "Pancetta (Premium)", "p9": "Smoked neck", "p10": "Smoked loin", "p11": "Smoked tenderloin", "p12": "Pork rinds",
        "p13": "Pork lard", "p14": "Blood sausage", "p15": "Grill sausages", "p16": "Dry ribs", "p17": "Smoked head", "p18": "Soap bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 GASTRONOMIE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🧺", "cart_empty": "Ihr Korb ist leer.",
        "note_vaga": """⚖️ **Wiegehinweis:** Die Preise sind fest, der Endbetrag wird nach dem Wiegen ermittelt.""",
        "note_delivery": """🚚 **Lieferung:** Zustellung an Ihre Adresse. Zahlungen sind **ausschließlich per Nachnahme** möglich.""",
        "total": "Informativer Betrag", "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Straße*", "form_country": "Land*", 
        "btn_order": "🚀 BESTELLUNG SENDEN", "success": "Danke!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "tax": "Inkl. MwSt.", "shipping_info": "LIEFERDATEN",
        "horeca_title": "Vertrauen und Tradition", "haccp_title": "Lebensmittelsicherheit", "info_title": "Unsere Geschichte",
        "horeca_text": "Authentisches Raucharoma und Großhandelsunterstützung im Jahr 2026.",
        "haccp_text": "Vollständige Rückverfolgbarkeit und höchste Hygienestandards.",
        "info_text": "Seit Generationen in Sisak, verarbeiten wir Fleisch regionaler Bauern.",
        "p1": "Speck", "p2": "Stelze", "p3": "Brustspitzen", "p4": "Wurst", "p5": "Salami", "p6": "Knochen",
        "p7": "Füße mix", "p8": "Pancetta", "p9": "Nacken", "p10": "Karree", "p11": "Lende", "p12": "Grieben",
        "p13": "Schmalz", "p14": "Blutwurst", "p15": "Grillwürste", "p16": "Rippchen", "p17": "Kopf", "p18": "Seifenspeck"
    }
}

# --- 3. PODACI O PROIZVODIMA ---
PRODUCTS = [
    {"id": "p1", "price": 9.50, "unit": "kg"}, {"id": "p2", "price": 7.80, "unit": "pc"},
    {"id": "p3", "price": 6.50, "unit": "pc"}, {"id": "p4", "price": 14.20, "unit": "kg"},
    {"id": "p5", "price": 17.50, "unit": "kg"}, {"id": "p6", "price": 3.80, "unit": "kg"},
    {"id": "p7", "price": 4.50, "unit": "kg"}, {"id": "p8", "price": 16.90, "unit": "kg"},
    {"id": "p9", "price": 11.20, "unit": "kg"}, {"id": "p10", "price": 12.50, "unit": "kg"},
    {"id": "p11", "price": 15.00, "unit": "kg"}, {"id": "p12", "price": 19.50, "unit": "kg"},
    {"id": "p13", "price": 24.00, "unit": "pc"}, {"id": "p14", "price": 7.90, "unit": "kg"},
    {"id": "p15", "price": 9.20, "unit": "kg"}, {"id": "p16", "price": 8.90, "unit": "kg"},
    {"id": "p17", "price": 4.20, "unit": "kg"}, {"id": "p18", "price": 7.50, "unit": "kg"}
]

# --- 4. FUNKCIJA ZA EMAIL ---
def send_email(info, cart_items, lang):
    summary = "\n".join([f"- {i['name']}: {i['qty']} {i['unit']}" for i in cart_items])
    body = f"NARUDŽBA 2026\nKupac: {info['name']}\nTel: {info['tel']}\nAdresa: {info['addr']}, {info['city']}\n\nStavke:\n{summary}\n\nUkupno: {info['total']:.2f} €"
    msg = MIMEText(body); msg['Subject'] = f"Narudžba: {info['name']}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls(); s.login(MOJ_EMAIL, MOJA_LOZINKA); s.send_message(msg)
        return True
    except: return False

# --- 5. APP UI ---
st.set_page_config(page_title="Mesnica Kojundžić 2026", layout="wide")
if 'cart' not in st.session_state: st.session_state.cart = {}

with st.sidebar:
    lang_choice = st.selectbox("Izaberite jezik / Choose language", list(LANG_MAP.keys()))
    T = LANG_MAP[lang_choice]
    menu = st.radio("Izbornik", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if menu == T["nav_shop"]:
    st.title("🥩 " + T["title_sub"])
    col1, col2 = st.columns([1.8, 1])
    
    with col1:
        st.subheader(T["nav_shop"])
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.container(border=True):
                    st.write(f"**{T.get(p['id'], p['id'])}**")
                    st.write(f"{p['price']:.2f} € / {T['unit_'+p['unit']]}")
                    if p['unit'] == "pc":
                        q = st.number_input(f"{T['unit_pc']}", min_value=0.0, step=1.0, key=f"q_{p['id']}")
                    else:
                        if f"state_{p['id']}" not in st.session_state: st.session_state[f"state_{p['id']}"] = 0.0
                        q = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5, key=f"q_{p['id']}")
                        if q == 0.5 and st.session_state[f"state_{p['id']}"] == 0.0:
                            q = 1.0; st.session_state[f"state_{p['id']}"] = 1.0; st.rerun()
                        else: st.session_state[f"state_{p['id']}"] = q
                    if q > 0: st.session_state.cart[p['id']] = q
                    elif p['id'] in st.session_state.cart: del st.session_state.cart[p['id']]

    with col2:
        st.markdown(f"## {T['cart_title']}")
        total_price = 0; items_for_mail = []
        if not st.session_state.cart: st.info(T["cart_empty"])
        else:
            for pid, q in st.session_state.cart.items():
                p_data = next(x for x in PRODUCTS if x['id'] == pid)
                sub = q * p_data['price']; total_price += sub
                st.write(f"✅ {T.get(pid, pid)}: {q} {T['unit_'+p_data['unit']]} = {sub:.2f} €")
                items_for_mail.append({'name': T.get(pid, pid), 'qty': q, 'unit': T['unit_'+p_data['unit']]})
        
        st.divider()
        st.markdown(f"### {T['total']}: {total_price:.2f} €")
        st.markdown(f"""<div style="border: 1px solid #d5dbdb; border-left: 5px solid #5d6d7e; padding: 12px; background-color: #f4f6f6; border-radius: 4px;"><p style="color: #2c3e50; font-size: 0.9rem; line-height: 1.4; margin: 0;">{T['note_vaga']}</p></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""<div style="border: 1px solid #d5dbdb; border-left: 5px solid #5d6d7e; padding: 12px; background-color: #f4f6f6; border-radius: 4px;"><p style="color: #2c3e50; font-size: 0.9rem; line-height: 1.4; margin: 0;">{T['note_delivery']}</p></div>""", unsafe_allow_html=True)
        st.write("") 
        
        with st.form("order_form"):
            st.write(f"📋 **{T['shipping_info']}**")
            n = st.text_input(T["form_name"]); t = st.text_input(T["form_tel"]); a = st.text_input(T["form_addr"])
            c = st.text_input(T["form_city"]); z = st.text_input(T["form_zip"]); co = st.text_input(T["form_country"])
            if st.form_submit_button(T["btn_order"]):
                if not st.session_state.cart: st.error("Empty!")
                elif n and t and a:
                    if send_email({'name':n,'tel':t,'addr':a,'city':c,'total':total_price}, items_for_mail, lang_choice):
                        st.success(T["success"]); st.session_state.cart = {}
                        for p in PRODUCTS: 
                            if f"state_{p['id']}" in st.session_state: st.session_state[f"state_{p['id']}"] = 0.0
                        time.sleep(2); st.rerun()
                else: st.warning("!!!")

elif menu == T["nav_horeca"]:
    st.header(T["horeca_title"]); st.write(T["horeca_text"]); st.info(f"📧 Kontakt: {MOJ_EMAIL}")
elif menu == T["nav_haccp"]:
    st.header(T["haccp_title"]); st.write(T["haccp_text"])
elif menu == T["nav_info"]:
    st.header(T["info_title"]); st.write(T["info_text"])
