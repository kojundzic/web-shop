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

# --- 2. MASTER PRIJEVODI (AŽURIRANI S RUBRIKOM DOBAVLJAČI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA", "nav_suppliers": "🚜 DOBAVLJAČI",
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
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Meso pripremamo polako, uz korištenje isključivo domaćih začina, bez aditiva.\n📍 **Glavno prodajno mjesto:** Tržnica Sisak.\n🕒 **Radno vrijeme:** Pon-Sub: 07:00 - 13:00""",
        "suppliers_title": "Naši dobavljači i podrijetlo sirovine",
        "suppliers_text": "Ponosni smo na suradnju s lokalnim uzgajivačima. Svo meso koje prerađujemo dolazi isključivo s domaćih pašnjaka i farmi s područja **Banovine, Posavine i Lonjskog polja**. Ovakva kratka opskrbna ruta jamči svježinu i vrhunsku kvalitetu domaće sirovine.",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA! HVALA VAM NA POVJERENJU.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US", "nav_suppliers": "🚜 SUPPLIERS",
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
        "suppliers_title": "Our Suppliers and Origin",
        "suppliers_text": "We are proud of our cooperation with local farmers. All the meat we process comes exclusively from domestic pastures and farms in the regions of **Banovina, Posavina, and Lonjsko Polje**. This short supply chain guarantees freshness and the superior quality of local raw materials.",
        "form_name": "Full Name*", "form_tel": "Delivery Phone*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & Number*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED! THANK YOU.", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "SHIPPING DETAILS",
        "p1": "Smoked Hamburger", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters Mix", "p8": "Pancetta (Premium)", "p9": "Smoked Neck (Boneless)", "p10": "Smoked Pork Loin (Boneless)", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Pork Head", "p18": "White Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS", "nav_suppliers": "🚜 LIEFERANTEN",
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
        "suppliers_title": "Unsere Lieferanten und Herkunft",
        "suppliers_text": "Wir sind stolz auf die Zusammenarbeit mit lokalen Züchtern. Das gesamte von uns verarbeitete Fleisch stammt ausschließlich von heimischen Weiden und Bauernhöfen aus den Regionen **Banovina, Posavina und Lonjsko Polje**. Dieser kurze Lieferweg garantiert Frische und höchste Qualität der heimischen Rohstoffe.",
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
    {"id": "p9", "price": 12.50, "unit": "kg"}, {"id": "p10", "price": 13.50, "unit": "kg"},
    {"id": "p11", "price": 15.00, "unit": "kg"}, {"id": "p12", "price": 18.00, "unit": "kg"},
    {"id": "p13", "price": 10.00, "unit": "pc"}, {"id": "p14", "price": 9.00, "unit": "kg"},
    {"id": "p15", "price": 10.50, "unit": "kg"}, {"id": "p16", "price": 8.50, "unit": "kg"},
    {"id": "p17", "price": 5.00, "unit": "pc"}, {"id": "p18", "price": 9.00, "unit": "kg"}
]

# --- 4. SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- 5. UI ---
st.set_page_config(page_title="Kojundžić 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])

# --- SHOP TAB ---
with tabs[0]:
    st.header(T["title_sub"])
    st.info(T["note_vaga"])
    st.warning(T["note_delivery"])
    
    cols = st.columns(3)
    for idx, p in enumerate(PRODUCTS):
        with cols[idx % 3]:
            st.subheader(T[p["id"]])
            st.write(f"{p['price']:.2f} {T['curr']} / {T['unit_'+p['unit']]}")
            qty = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5 if p['unit']=='kg' else 1.0, key=f"in_{p['id']}")
            if qty > 0:
                st.session_state.cart[p['id']] = qty
            elif p['id'] in st.session_state.cart:
                del st.session_state.cart[p['id']]

    st.divider()
    st.title(T["cart_title"])
    if not st.session_state.cart:
        st.write(T["cart_empty"])
    else:
        total = 0
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total += sub
            st.write(f"✅ {T[pid]}: {qty} x {p_inf['price']} = {sub:.2f} €")
        
        st.metric(T["total"], f"{total:.2f} €")
        
        with st.form("order"):
            n = st.text_input(T["form_name"])
            t = st.text_input(T["form_tel"])
            c = st.text_input(T["form_city"])
            z = st.text_input(T["form_zip"])
            a = st.text_input(T["form_addr"])
            if st.form_submit_button(T["btn_order"]):
                st.success(T["success"])

# --- HORECA TAB ---
with tabs[1]:
    st.header(T["horeca_title"])
    st.write(T["horeca_text"])

# --- DOBAVLJAČI TAB ---
with tabs[2]:
    st.header(T["suppliers_title"])
    st.write(T["suppliers_text"])

# --- HACCP TAB ---
with tabs[3]:
    st.header(T["haccp_title"])
    st.write(T["haccp_text"])

# --- INFO TAB ---
with tabs[4]:
    st.header(T["info_title"])
    st.write(T["info_text"])
