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

# --- 2. MASTER PRIJEVODI (DETALJNI I PROŠIRENI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je trenutno prazna",
        "note_vaga": """⚖️ **NAPOMENA O VAGANJU:** Cijene proizvoda su fiksne po jedinici mjere, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Trudimo se da odstupanja od naručene količine budu minimalna.""",
        "note_delivery": """🚚 **DOSTAVA I PLAĆANJE:** Proizvode šaljemo u specijaliziranoj termo-izoliranoj ambalaži koja čuva svježinu. Plaćanje se vrši **isključivo pouzećem** (gotovinom prilikom preuzimanja paketa).""",
        "horeca_title": "HoReCa Partnerstvo: Vrhunska sirovina za ugostiteljstvo",
        "horeca_text": """Za restorane, hotele i ostale ugostiteljske objekte nudimo posebne uvjete suradnje, stabilnost cijena i personalizirane rezove mesa. Naši proizvodi su tradicionalno dimljeni na hladnom dimu bukve i graba, što jamči autentičan okus Vaših jela. 
        \n📬 **Sve upite i narudžbe za ugostitelje molimo šaljite izravno na naš email:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)""",
        "suppliers_title": "🚜 Podrijetlo sirovine: Banovina, Posavina i Lonjsko polje",
        "suppliers_text": """Kvaliteta počinje na pašnjaku. Ponosni smo što naše meso dolazi isključivo od lokalnih uzgajivača s ekološki očuvanih područja **Banovine, Posavine i Lonjskog polja**. Ovakav pristup jamči kratak lanac opskrbe, vrhunsku svježinu i potporu domaćem ruralnom razvoju.""",
        "haccp_title": "🛡️ Sigurnost hrane i HACCP standardi",
        "haccp_text": """U našem pogonu primjenjujemo najstrože higijenske standarde. Svaki komad mesa ima potpunu sljedivost, što znači da u svakom trenutku znamo s koje farme sirovina potječe. Naš objekt je pod stalnim veterinarskim nadzorom kako bismo Vam osigurali najvišu razinu zdravstvene ispravnosti.""",
        "info_title": "ℹ️ O nama: Tradicija obitelji Kojundžić",
        "info_text": """Obitelj Kojundžić već naraštajima u Sisku čuva vještinu tradicionalne pripreme domaćih mesnih delicija. Naša filozofija je jednostavna: domaće meso, prirodni začini i strpljenje pri dimljenju bez ikakvih umjetnih dodataka ili aditiva.
        \n📍 **LOKACIJA:** Nalazimo se u samom srcu Siska, na Gradskoj tržnici Kontroba. Posjetite nas osobno i uvjerite se u kvalitetu naših proizvoda!""",
        "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos računa", "shipping_info": "📍 POTPUNI PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek (svinjska koljenica)", "p3": "Dimljeni prsni vršci", "p4": "Domaća slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti za juhu",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska kvaliteta)", "p9": "Dimljeni vrat bez kosti", "p10": "Dimljeni kare (kremenadl) bez kosti", "p11": "Dimljena pečenica", "p12": "Domaći čvarci (ručno rađeni)",
        "p13": "Domaća svinjska mast (kanta)", "p14": "Krvavice (tradicionalne domaće)", "p15": "Pečenice za roštilj", "p16": "Suha svinjska rebra", "p17": "Dimljena svinjska glava", "p18": "Slanina sapunara (bijela slanina)"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is currently empty",
        "note_vaga": "⚖️ **WEIGHT NOTE:** Final prices are based on exact weight measured during packaging. We aim for minimal deviation from your order.",
        "note_delivery": "🚚 **SHIPPING:** Thermo-insulated packaging used. Payment is **Cash on Delivery (COD)** only.",
        "horeca_title": "HoReCa Partnership",
        "horeca_text": "We offer premium smoked meats for restaurants. \n📬 **For business inquiries, please contact us at:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Origin: Banovina, Posavina and Lonjsko Polje",
        "suppliers_text": "Our meat is sourced exclusively from local family farms in ecologically preserved regions.",
        "haccp_title": "🛡️ Food Safety & HACCP", "haccp_text": "Strict hygiene standards with full traceability from farm to table.",
        "info_title": "ℹ️ About the Kojundžić Family",
        "info_text": "Generations of tradition in Sisak. \n📍 **LOCATION:** Sisak City Market (Kontroba).",
        "form_name": "Full Name*", "form_tel": "Phone Number*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Address*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "📍 COMPLETE DELIVERY DETAILS",
        "p1": "Smoked Bacon (Hamburger style)", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Soup Bones",
        "p7": "Smoked Pig Trotters", "p8": "Premium Pancetta", "p9": "Smoked Pork Neck (Boneless)", "p10": "Smoked Pork Loin (Boneless)", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Pork Ribs", "p17": "Smoked Pork Head", "p18": "White Fat Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Warenkorb ist leer",
        "note_vaga": "⚖️ **WIEGEHINWEIS:** Endpreise werden erst nach dem exakten Wiegen beim Verpacken ermittelt.",
        "note_delivery": "🚚 **LIEFERUNG:** Versand in Thermoverpackung. Zahlung erfolgt ausschließlich per **Nachnahme**.",
        "horeca_title": "HoReCa Partnerschaft",
        "horeca_text": "Premium-Produkte für die Gastronomie. \n📬 **Anfragen per E-Mail:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Herkunft: Banovina, Posavina und Lonjsko Polje",
        "suppliers_text": "Unser Fleisch stammt ausschließlich von heimischen Weiden lokaler Bauernhöfe.",
        "haccp_title": "🛡️ HACCP Standard", "haccp_text": "Höchste Hygienestandards und Rückverfolgbarkeit vom Bauernhof bis zum Tisch.",
        "info_title": "ℹ️ Über uns",
        "info_text": "Traditionelle Metzgerei aus Sisak. \n📍 **STANDORT:** Stadtmarkt Sisak (Kontroba).",
        "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "🚀 BESTELLUNG SENDEN", "success": "BESTELLUNG ERHALTEN!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "📍 LIEFERDATEN",
        "p1": "Geräucherter Hamburger-Speck", "p2": "Geräucherte Schweinshaxe", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Hauswurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Geräucherte Schweinefüße", "p8": "Premium Pancetta", "p9": "Geräucherter Schweinenacken", "p10": "Geräuchertes Karree (o.K.)", "p11": "Geräuchertes Lendenstück", "p12": "Hausmacher Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Geräucherter Schweinekopf", "p18": "Weißer Speck"
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

if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- 4. UI SETUP ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

col_main, col_side = st.columns([0.65, 0.35])

# --- SREDINA: ARTIKLI I RUBRIKE ---
with col_main:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # SHOP
        cols_shop = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_shop[idx % 2]:
                st.subheader(T.get(p["id"], p["id"]))
                st.write(f"Cijena: **{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                if p["unit"] == "kg":
                    val = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5, value=0.0, key=f"s_{p['id']}")
                    if 0.1 <= val <= 0.5: val = 1.0 # Logika 0 -> 1.0
                else:
                    val = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=1.0, value=0.0, key=f"s_{p['id']}")
                if val > 0: st.session_state.cart[p["id"]] = val
                elif p["id"] in st.session_state.cart: del st.session_state.cart[p["id"]]

    with tabs[1]: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs[2]: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs[3]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs[4]: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA: KOŠARICA, IZNOS, NAPOMENE I DOSTAVA ---
with col_side:
    st.markdown(f"### {T['cart_title']}")
    total_val = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_val += sub
            st.write(f"✅ **{T.get(pid, pid)}**: {qty} {T['unit_'+p_inf['unit']]} = {sub:.2f} €")
        
        st.divider()
        st.metric(label=T["total"], value=f"{total_val:.2f} €")

    # Napomene ISPOD košarice i iznosa
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("sidebar_form"):
        name = st.text_input(T["form_name"])
        tel = st.text_input(T["form_tel"])
        city = st.text_input(T["form_city"])
        zip_c = st.text_input(T["form_zip"])
        addr = st.text_input(T["form_addr"])
        
        if st.form_submit_button(T["btn_order"]):
            if name and tel and addr and st.session_state.cart:
                body = f"NARUDŽBA 2026\nKupac: {name}\nTel: {tel}\nAdresa: {addr}, {zip_c} {city}\n\nArtikli:\n"
                for pid, q in st.session_state.cart.items():
                    body += f"- {T.get(pid, pid)}: {q}\n"
                body += f"\nInformativni iznos: {total_val:.2f} EUR"
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(body); msg['Subject'] = f"Narudžba {name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except: st.error("Sustav trenutno nedostupan.")
            elif not st.session_state.cart: st.error("Košarica je prazna!")
            else: st.error("Ispunite obavezna polja (*).")
