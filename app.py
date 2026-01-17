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

# --- 2. MASTER PRIJEVODI (KORIGIRANI I PROŠIRENI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. Trudimo se da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "note_delivery": """🚚 **Dostava i plaćanje:** Naručene artikle šaljemo putem provjerene dostavne službe na kućnu adresu ili u najbliži paketomat, ovisno o Vašem izboru pri preusmjeravanju. Plaćanje se vrši **isključivo pouzećem** (gotovinom dostavljaču), čime jamčimo sigurnost transakcije.""",
        "suppliers_title": "Naši partneri: Snaga lokalnog uzgoja",
        "suppliers_text": """Kvaliteta mesa u Mesnici Kojundžić izravan je rezultat suradnje s malim obiteljskim gospodarstvima iz našeg neposrednog okruženja. Vjerujemo u kratke lance opskrbe i podršku lokalnoj zajednici.
\n**Područja s kojih nabavljamo sirovinu u 2026. godini:**
* **Banovina i Posavina:** Naši glavni izvori vrhunske svinjetine i junetine. Životinje se uzgajaju na tradicionalan način, uz prirodnu ishranu, što rezultira savršenom teksturom mesa.
* **Lonjsko polje:** Posebno smo ponosni na suradnju s uzgajivačima čija stoka boravi na slobodnoj ispaši u netaknutoj prirodi parka prirode.
* **Okolica Siska:** Svakodnevna suradnja s lokalnim farmerima osigurava da meso s polja do naše mesnice stigne u najkraćem mogućem roku, jamčeći maksimalnu svježinu.""",
        "horeca_title": "HoReCa Partnerstvo: Temelj vrhunskog ugostiteljstva",
        "horeca_text": """Kao obiteljski vođen posao, duboko poštujemo trud kolega u ugostiteljskom sektoru. Razumijemo da svaki vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom kvalitetom sirovine.
\n**Naša ponuda za partnere u 2026. godini uključuje:**
* **Tradicija dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba.
* **Logistička izvrsnost:** Vlastita flota vozila s kontroliranim temperaturnim režimom (hladnjače).
* **Veleprodajni standard:** Prioritetna obrada i personalizirani rezovi mesa.""",
        "haccp_title": "Sigurnost hrane i HACCP: Beskompromisni standardi",
        "haccp_text": """U Mesnici Kojundžić, higijena je temelj našeg obiteljskog ugleda. U 2026. godini primjenjujemo najnovije tehnologije nadzora kvalitete.
* **Potpuna sljedivost (Traceability):** Svaki komad mesa ima dokumentiran put – točno znamo s koje farme dolazi.
* **Moderni pogon:** Naš objekt u Sisku pod stalnim je veterinarskim nadzorom uz stroge HACCP protokole.""",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima. Meso pripremamo polako, uz korištenje isključivo domaćih začina, bez aditiva.\n📍 **Glavno prodajno mjesto:** Tržnica Sisak.\n🕒 **Radno vrijeme:** Pon-Sub: 07:00 - 13:00""",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljeni nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA! HVALA VAM NA POVJERENJU.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_suppliers": "🚜 SUPPLIERS", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "is empty",
        "note_vaga": """⚖️ **Weight Note:** Product prices are fixed, but the exact total of your invoice will be confirmed after precise weighing just before packaging. Final payment is made upon delivery (COD). We strive to minimize the difference between the estimated and final amount.""",
        "note_delivery": """🚚 **Shipping & Payment:** Ordered items are shipped via a verified delivery service to your address or parcel locker. Payment is **Cash on Delivery (COD)** only, ensuring transaction security.""",
        "suppliers_title": "Our Partners: Strength of Local Farming",
        "suppliers_text": """The meat quality at Kojundžić Butchery is a direct result of our cooperation with small family farms in our immediate vicinity. 
\n**Sourcing regions in 2026:**
* **Banovina & Posavina:** Our primary sources for premium pork and beef. Animals are raised traditionally with natural diets.
* **Lonjsko Polje:** We are proud to work with breeders whose livestock grazes freely in the nature park.
* **Sisak Area:** Daily cooperation with local farmers ensures the shortest time from field to butchery, guaranteeing maximum freshness.""",
        "horeca_title": "HoReCa Partnership: Foundation of Hospitality",
        "horeca_text": "We provide beech-smoked products, temperature-controlled logistics, and wholesale support with custom meat cuts for our 2026 partners.",
        "haccp_title": "Food Safety & HACCP: Uncompromising Standards",
        "haccp_text": "Full traceability and strict HACCP protocols in our modern facility in Sisak under constant veterinary supervision.",
        "info_title": "Our Story: Family, Sisak, and Quality",
        "info_text": "Generations of tradition in Sisak. We prepare meat slowly, using only natural spices and zero additives.\n📍 **Main Shop:** Sisak City Market.\n🕒 **Hours:** Mon-Sat: 07:00 - 13:00",
        "p1": "Smoked Hamburger", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters Mix", "p8": "Pancetta (Premium)", "p9": "Smoked Neck (Boneless)", "p10": "Smoked Pork Loin (Boneless)", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Pork Head", "p18": "White Bacon",
        "form_name": "Full Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "SHIPPING DETAILS"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_suppliers": "🚜 LIEFERANTEN", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "ist leer",
        "note_vaga": """⚖️ **Hinweis zum Wiegen:** Die Produktpreise sind fest, der genaue Betrag wird jedoch erst nach dem Wiegen ermittelt. Die Bezahlung erfolgt per Nachnahme bei Paketerhalt.""",
        "note_delivery": """🚚 **Lieferung:** Zustellung an Ihre Adresse oder Packstation. Die Zahlung erfolgt **ausschließlich per Nachnahme**.""",
        "suppliers_title": "Unsere Partner: Lokale Landwirtschaft",
        "suppliers_text": """Die Fleischqualität basiert auf der engen Zusammenarbeit mit kleinen Familienbetrieben aus unserer Region.
\n**Bezugsregionen im Jahr 2026:**
* **Banovina & Posavina:** Unsere Hauptquellen für Schweine- und Rindfleisch. Traditionelle Aufzucht sorgt für perfekte Fleischstruktur.
* **Lonjsko Polje:** Kooperation mit Züchtern, deren Vieh im Naturpark frei grast.
* **Umgebung von Sisak:** Tägliche Zusammenarbeit garantiert kürzeste Transportwege und maximale Frische.""",
        "horeca_title": "HoReCa-Partnerschaft",
        "horeca_text": "Buchenholzrauch-Spezialitäten und Kühltransporte mit individuellen Fleischschnitten für unsere Partner im Jahr 2026.",
        "haccp_title": "HACCP & Sicherheit",
        "haccp_text": "Lückenlose Rückverfolgbarkeit und strenge HACCP-Protokolle unter ständiger veterinärmedizinischer Aufsicht in Sisak.",
        "info_title": "Unsere Geschichte",
        "info_text": "Traditionelle Fleischzubereitung aus Sisak mit Naturgewürzen und ohne chemische Zusätze.\n📍 **Standort:** Stadtmarkt Sisak.",
        "p1": "Geräucherter Hamburger", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Geräucherte Schweinefüße Mix", "p8": "Pancetta (Premium)", "p9": "Geräucherter Nacken (o.K.)", "p10": "Geräuchertes Karree (o.K.)", "p11": "Geräuchertes Lendenstück", "p12": "Hausmacher Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Geräucherter Schweinekopf", "p18": "Speck (weiß)",
        "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Straße*",
        "btn_order": "🚀 SENDEN", "success": "ERFOLGREICH ÜBERMITTELT!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "LIEFERDATEN"
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
    menu = st.radio("Navigacija", [T["nav_shop"], T["nav_suppliers"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

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
        st.subheader(T["cart_title"])
        tot = 0; items_mail = []
        if st.session_state.cart:
            for pid, q in st.session_state.cart.items():
                pd = next(x for x in PRODUCTS if x['id'] == pid)
                sub = q * pd['price']; tot += sub
                p_name = T.get(pid, pid)
                st.write(f"✅ {p_name}: {q} {T['unit_'+pd['unit']]} = {sub:.2f} €")
                items_mail.append({'name': p_name, 'qty': q, 'unit': T['unit_'+pd['unit']]})
        else: st.write(f"({T['cart_empty']})")
        
        st.write(f"### {T['total']}: {tot:.2f} €")
        st.divider()
        st.info(T["note_vaga"])
        st.info(T["note_delivery"])
        st.divider()

        with st.form("checkout_form"):
            st.write(f"### {T['shipping_info']}")
            name = st.text_input(T.get("form_name", "Ime i Prezime*"))
            tel = st.text_input(T.get("form_tel", "Broj telefona*"))
            addr = st.text_input(T.get("form_addr", "Adresa*"))
            city = st.text_input(T.get("form_city", "Grad*"))
            zip_c = st.text_input(T.get("form_zip", "Poštanski broj*"))
            
            submit = st.form_submit_button(T["btn_order"])
            if submit:
                if not st.session_state.cart: st.error("Košarica je prazna!")
                elif name and tel and addr and city:
                    info = {"name": name, "tel": tel, "addr": addr, "city": city, "zip": zip_c, "total": tot}
                    if send_email(info, items_mail):
                        msg_placeholder = st.empty()
                        msg_placeholder.success(T["success"])
                        st.session_state.cart = {}
                        time.sleep(10)
                        msg_placeholder.empty()
                        st.rerun()
                else: st.error("Ispunite obavezna polja (*)")

elif menu == T["nav_info"]:
    st.title(T["info_title"])
    st.markdown(T["info_text"])
    st.subheader(f"📍 {T.get('info_text_ext', 'Lokacija: Tržnica Sisak')}")
    map_data = pd.DataFrame({'lat': [45.4853], 'lon': [16.3735]})
    st.map(map_data)
elif menu == T["nav_suppliers"]:
    st.title(T["suppliers_title"])
    st.markdown(T["suppliers_text"])
else:
    key_p = "horeca" if menu == T["nav_horeca"] else "haccp"
    st.title(T[f"{key_p}_title"])
    st.markdown(T[f"{key_p}_text"])
