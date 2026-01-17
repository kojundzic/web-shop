import streamlit as st
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import time

# --- 1. KONFIGURACIJA (FIKSNA I ZAKLJUČANA) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (UKLJUČUJUĆI ARTIKLE - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. Trudimo se da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "note_delivery": """🚚 **Dostava i plaćanje:** Naručene artikle šaljemo putem provjerene dostavne službe na kućnu adresu ili u najbliži paketomat, ovisno o Vašem izboru pri preusmjeravanju. Plaćanje se vrši **isključivo pouzećem** (gotovinom dostavljaču), čime jamčimo sigurnost transakcije.""",
        "horeca_title": "HoReCa Partnerstvo: Temelj vrhunskog ugostiteljstva",
        "horeca_text": """Kao obiteljski vođen posao, duboko poštujemo trud kolega u ugostiteljskom sektoru. Razumijemo da svaki vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom kvalitetom sirovine. 
\n**Naša ponuda za partnere u 2026. godini uključuje:**
* **Tradicija dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba, bez tekućih pripravaka.
* **Logistička izvrsnost:** Raspolažemo vlastitom flotom vozila s kontroliranim temperaturnim režimom (hladnjače).
* **Veleprodajni standard:** Redovnim partnerima nudimo prioritetnu obradu, personalizirane rezove mesa i stabilnost cijena tijekom cijele godine.""",
        "haccp_title": "Sigurnost hrane i HACCP: Beskompromisni standardi",
        "haccp_text": """U Mesnici Kojundžić, higijena nije samo zakonska obveza, već temelj našeg obiteljskog ugleda. U 2026. godini primjenjujemo najnovije tehnologije nadzora kvalitete.
* **Potpuna sljedivost (Traceability):** Svaki komad mesa ima dokumentiran put – točno znamo s koje farme dolazi i kada je prerađen.
* **Moderni pogon:** Naš objekt u Sisku pod stalnim je veterinarskim nadzorom.""",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima. Meso pripremamo polako, uz korištenje isključivo domaćih začina, bez aditiva.\n📍 **Glavno prodajno mjesto:** Tržnica Sisak.\n🕒 **Radno vrijeme:** Pon-Sub: 07:00 - 13:00""",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA! HVALA VAM NA POVJERENJU.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljeni nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "is empty",
        "note_vaga": """⚖️ **Weight Note:** Prices are fixed, but the final invoice amount will be determined after weighing just before packaging. You will pay the final amount upon delivery (COD). We aim for minimal differences between estimated and final weight.""",
        "note_delivery": """🚚 **Shipping & Payment:** We ship via a verified service to your home or a parcel locker. Payment is **exclusively Cash on Delivery (COD)**.""",
        "horeca_title": "HoReCa Partnership",
        "horeca_text": "We offer beech-smoked products, refrigerated delivery, and wholesale support for the hospitality sector in 2026.",
        "haccp_title": "Food Safety",
        "haccp_text": "Strict HACCP protocols and full traceability at our Sisak facility.",
        "info_title": "Our Story",
        "info_text": "Traditional meat preparation from Sisak. \n📍 **Main Shop:** Sisak City Market.",
        "form_name": "Full Name*", "form_tel": "Delivery Phone*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & Number*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED! THANK YOU.", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "SHIPPING DETAILS",
        "p1": "Smoked Hamburger", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters Mix", "p8": "Pancetta (Premium)", "p9": "Smoked Neck (Boneless)", "p10": "Smoked Pork Loin (Boneless)", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Pork Head", "p18": "White Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "ist leer",
        "note_vaga": """⚖️ **Hinweis zum Wiegen:** Die Preise sind fest, der genaue Betrag wird jedoch erst nach dem Wiegen ermittelt. Die Bezahlung erfolgt per Nachnahme bei Paketerhalt.""",
        "note_delivery": """🚚 **Lieferung & Zahlung:** Zustellung an Ihre Adresse oder Packstation. Die Zahlung erfolgt **ausschließlich per Nachnahme**.""",
        "horeca_title": "HoReCa-Partnerschaft",
        "horeca_text": "Traditionelle Räucherwaren und Kühltransporte für die Gastronomie im Jahr 2026.",
        "haccp_title": "Sicherheit",
        "haccp_text": "Strenge HACCP-Protokolle und Rückverfolgbarkeit in Sisak.",
        "info_title": "Unsere Geschichte",
        "info_text": "Traditionelle Fleischzubereitung aus Sisak. \n📍 **Hauptstandort:** Stadtmarkt Sisak.",
        "form_name": "Name*", "form_tel": "Telefonnummer*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Straße & Hausnummer*",
        "btn_order": "🚀 SENDEN", "success": "BESTELLUNG ERFOLGREICH ÜBERMITTELT!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "LIEFERDATEN",
        "p1": "Geräucherter Hamburger", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Geräucherte Schweinefüße Mix", "p8": "Pancetta (Premium)", "p9": "Geräucherter Nacken (o.K.)", "p10": "Geräuchertes Karree (o.K.)", "p11": "Geräuchertes Lendenstück", "p12": "Hausmacher Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Geräucherter Schweinekopf", "p18": "Speck (weiß)"
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

def send_email(info, cart_items):
    summary = "\n".join([f"- {i['name']}: {i['qty']} {i['unit']}" for i in cart_items])
    body = f"NARUDŽBA 2026\n\nKupac: {info['name']}\nTel: {info['tel']}\nAdresa: {info['addr']}, {info['zip']} {info['city']}\n\nSTAVKE:\n{summary}\n\nUKUPNO: {info['total']:.2f} €"
    msg = MIMEText(body); msg['Subject'] = f"Narudžba: {info['name']}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls(); s.login(MOJ_EMAIL, MOJA_LOZINKA); s.send_message(msg)
        return True
    except: return False

# --- 4. UI LOGIKA ---
st.set_page_config(page_title="Mesnica Kojundžić 2026", layout="wide")
if 'cart' not in st.session_state: st.session_state.cart = {}

with st.sidebar:
    lang_choice = st.selectbox("Language / Jezik", list(LANG_MAP.keys()))
    T = LANG_MAP[lang_choice]
    menu = st.radio("Navigacija", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if menu == T["nav_shop"]:
    st.title(T["title_sub"])
    col1, col2 = st.columns([1.6, 1])
    
    with col1:
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.container(border=True):
                    name_p = T.get(p["id"], p["id"])
                    st.write(f"**{name_p}**")
                    st.write(f"{p['price']:.2f} € / {T['unit_'+p['unit']]}")
                    step = 0.5 if p['unit'] == "kg" else 1.0
                    q = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=step, key=f"z_{p['id']}")
                    if q > 0: st.session_state.cart[p['id']] = q
                    elif p['id'] in st.session_state.cart: del st.session_state.cart[p['id']]

    with col2:
        # --- 1. KOŠARICA I INFORMATIVNI IZNOS (UVIJEK VIDLJIVO) ---
        st.subheader(T["cart_title"])
        tot = 0; items_mail = []
        if not st.session_state.cart:
            st.write(f"({T['cart_empty']})")
        else:
            for pid, q in st.session_state.cart.items():
                pd = next(x for x in PRODUCTS if x['id'] == pid)
                sub = q * pd['price']; tot += sub
                p_name = T.get(pid, pid)
                st.write(f"✅ {p_name}: {q} {T['unit_'+pd['unit']]} = {sub:.2f} €")
                items_mail.append({'name': p_name, 'qty': q, 'unit': T['unit_'+pd['unit']]})
        
        # Informativni iznos je sada izvan "if st.session_state.cart" bloka
        st.write(f"### {T['total']}: {tot:.2f} €")
        
        st.divider()

        # --- 2. STALNE NAPOMENE ---
        st.info(T["note_vaga"])
        st.info(T["note_delivery"])
        st.divider()

        # --- 3. PODACI ZA DOSTAVU (FIKSNI OBRAZAC) ---
        with st.form("checkout_form"):
            st.write(f"### {T['shipping_info']}")
            name = st.text_input(T.get("form_name", "Ime i Prezime*"))
            tel = st.text_input(T.get("form_tel", "Broj telefona*"))
            addr = st.text_input(T.get("form_addr", "Adresa*"))
            city = st.text_input(T.get("form_city", "Grad*"))
            zip_c = st.text_input(T.get("form_zip", "Poštanski broj*"))
            
            submit = st.form_submit_button(T["btn_order"])
            if submit:
                if not st.session_state.cart:
                    st.error("Vaša košarica je prazna!")
                elif name and tel and addr and city:
                    info = {"name": name, "tel": tel, "addr": addr, "city": city, "zip": zip_c, "total": tot}
                    if send_email(info, items_mail):
                        msg_placeholder = st.empty()
                        msg_placeholder.success(T["success"])
                        st.session_state.cart = {}
                        time.sleep(10)
                        msg_placeholder.empty()
                        st.rerun()
                else:
                    st.error("Molimo ispunite obavezna polja (*)")

elif menu == T["nav_info"]:
    st.title(T["info_title"])
    st.markdown(T["info_text"])
    st.subheader("📍 Lokacija: Tržnica Sisak")
    map_data = pd.DataFrame({'lat': [45.4853], 'lon': [16.3735]})
    st.map(map_data)
else:
    key_p = "horeca" if menu == T["nav_horeca"] else "haccp"
    st.title(T[f"{key_p}_title"])
    st.markdown(T[f"{key_p}_text"])
