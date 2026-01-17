import streamlit as st
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import time

# --- 1. KONFIGURACIJA ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (DETALJNI I PROŠIRENI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "OBITELJSKA MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna. Molimo odaberite proizvode.",
        "note_vaga": """⚖️ **VAŽNA NAPOMENA O VAGANJU:** Cijene proizvoda su fiksne po jedinici mjere, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Trudimo se da odstupanja od naručene količine budu minimalna.""",
        "note_delivery": """🚚 **DOSTAVA I PLAĆANJE:** Proizvode šaljemo u specijaliziranoj termo-izoliranoj ambalaži. Plaćanje se vrši **isključivo pouzećem** (gotovinom prilikom preuzimanja paketa).""",
        "horeca_title": "HoReCa Partnerstvo: Vrhunska sirovina",
        "horeca_text": "Za restorane, hotele i ugostitelje nudimo posebne uvjete i stabilnost cijena. \n📬 **Sve upite i narudžbe za ugostitelje molimo dogovorite izravno putem e-maila:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Podrijetlo: Banovina, Posavina i Lonjsko polje",
        "suppliers_text": "Svo meso koje prerađujemo dolazi isključivo s domaćih pašnjaka i farmi s područja **Banovine, Posavine i Lonjskog polja**. Kratak lanac opskrbe jamči svježinu.",
        "haccp_title": "🛡️ Sigurnost hrane i HACCP",
        "haccp_text": "Primjenjujemo najstrože higijenske standarde uz potpunu digitalnu sljedivost od farme do Vašeg stola pod stalnim veterinarskim nadzorom.",
        "info_title": "ℹ️ O nama i Lokacija",
        "info_text": """Obitelj Kojundžić u Sisku čuva vještinu tradicionalne pripreme mesa bez aditiva, uz korištenje domaćih začina i prirodnog dima bukve.
        \n📍 **LOKACIJA:** Nalazimo se u Sisku, na Gradskoj tržnici Kontroba. Posjetite nas svakim radnim danom i subotom od 07:00 do 13:00 sati.""",
        "form_name": "Ime i Prezime primatelja*", "form_tel": "Kontakt telefon*", "form_country": "Država*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos računa", "shipping_info": "📍 PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek (svinjska koljenica)", "p3": "Dimljeni prsni vršci", "p4": "Domaća slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti za juhu",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska kvaliteta)", "p9": "Dimljeni svinjski vrat bez kosti", "p10": "Dimljeni svinjski kare bez kosti", "p11": "Dimljena svinjska pečenica", "p12": "Domaći čvarci",
        "p13": "Domaća svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha svinjska rebra", "p17": "Dimljena svinjska glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ FAMILY BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Shopping Cart", "cart_empty": "Your cart is empty.",
        "note_vaga": "⚖️ **WEIGHT NOTE:** Final prices are determined by exact weight measured during packaging.",
        "note_delivery": "🚚 **SHIPPING:** Thermo-insulated packaging. Payment is **Cash on Delivery (COD)**.",
        "horeca_title": "HoReCa Partnership", "horeca_text": "Please contact us via e-mail for business inquiries: [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Origin", "suppliers_text": "Meat from Banovina, Posavina and Lonjsko Polje pastures.",
        "haccp_title": "🛡️ HACCP Safety", "haccp_text": "Full traceability and highest hygiene standards.",
        "info_title": "ℹ️ About Us", "info_text": "📍 **LOCATION:** Sisak City Market (Kontroba).",
        "form_name": "Full Name*", "form_tel": "Phone*", "form_country": "Country*", "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Invoice Total", "shipping_info": "📍 SHIPPING DETAILS",
        "p1": "Smoked Hamburger Bacon", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters", "p8": "Premium Pancetta", "p9": "Smoked Neck (Boneless)", "p10": "Smoked Loin (Boneless)", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Pork Lard", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Pork Head", "p18": "White Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 ONLINE-SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Ihr Warenkorb", "cart_empty": "Ihr Warenkorb ist leer.",
        "note_vaga": "⚖️ **WIEGEHINWEIS:** Endpreise werden nach dem Wiegen kurz vor dem Versand ermittelt.",
        "note_delivery": "🚚 **LIEFERUNG:** Thermo-Verpackung. Zahlung per **Nachnahme**.",
        "horeca_title": "HoReCa Partnerschaft", "horeca_text": "Anfragen per E-Mail: [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Herkunft", "suppliers_text": "Fleisch aus Banovina, Posavina und Lonjsko Polje.",
        "haccp_title": "🛡️ HACCP Sicherheit", "haccp_text": "Vollständige Rückverfolgbarkeit vom Bauernhof bis zum Tisch.",
        "info_title": "ℹ️ Über uns", "info_text": "📍 **STANDORT:** Stadtmarkt Sisak (Kontroba).",
        "form_name": "Name*", "form_tel": "Telefon*", "form_country": "Staat*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "🚀 BESTELLUNG SENDEN", "success": "BESTELLUNG ERHALTEN!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Rechnungsbetrag", "shipping_info": "📍 LIEFERDATEN",
        "p1": "Geräucherter Speck", "p2": "Geräucherte Schweinshaxe", "p3": "Geräucherte Spitzen", "p4": "Hausmacher Hauswurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Geräucherte Füße", "p8": "Premium Pancetta", "p9": "Geräucherter Nacken", "p10": "Geräuchertes Karree", "p11": "Lendenstück", "p12": "Grieben",
        "p13": "Schweineschmalz", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Schweinekopf", "p18": "Weißer Speck"
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
st.set_page_config(page_title="Mesnica Kojundžić 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

# Glavna podjela ekrana
col_main, col_side = st.columns([0.65, 0.35])

# --- LIJEVA STRANA (ARTIKLI I RUBRIKE) ---
with col_main:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs: # SHOP
        cols_shop = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_shop[idx % 2]:
                st.subheader(T[p["id"]])
                st.write(f"Cijena: **{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                
                curr_q = st.session_state.cart.get(p["id"], 0.0)
                
                # LOGIKA ZA KILE (0 -> 1.0 -> 1.5)
                if p["unit"] == "kg":
                    val = st.number_input(f"Količina ({T['unit_kg']})", min_value=0.0, step=0.5, value=curr_q, key=f"s_{p['id']}")
                    if curr_q == 0.0 and val == 0.5:
                        val = 1.0
                        st.session_state.cart[p["id"]] = 1.0
                        st.rerun()
                else:
                    val = st.number_input(f"Količina ({T['unit_pc']})", min_value=0.0, step=1.0, value=curr_q, key=f"s_{p['id']}")
                
                if val > 0:
                    st.session_state.cart[p["id"]] = val
                elif p["id"] in st.session_state.cart:
                    del st.session_state.cart[p["id"]]

    with tabs: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA (KOŠARICA, IZNOS, NAPOMENE, PODACI - STALNO VIDLJIVO) ---
with col_side:
    st.markdown(f"### {T['cart_title']}")
    total_price = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, q in list(st.session_state.cart.items()):
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = q * p_inf["price"]
            total_price += sub
            st.write(f"✅ **{T[pid]}**: {q} {T['unit_'+p_inf['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    
    # Informativni iznos (stalno vidljiv)
    st.metric(label=T["total"], value=f"{total_price:.2f} €")
    
    # Napomene (stalno vidljive)
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    # Podaci za dostavu (stalno vidljivo)
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("delivery_final_2026"):
        f_name = st.text_input(T["form_name"])
        f_tel = st.text_input(T["form_tel"])
        f_country = st.text_input(T["form_country"], value="Hrvatska")
        f_city = st.text_input(T["form_city"])
        f_zip = st.text_input(T["form_zip"])
        f_addr = st.text_input(T["form_addr"])
        
        if st.form_submit_button(T["btn_order"]):
            if f_name and f_tel and f_addr and st.session_state.cart:
                # E-mail konstrukcija
                body = f"NARUDŽBA 2026\nKupac: {f_name}\nTel: {f_tel}\nDržava: {f_country}\nAdresa: {f_addr}, {f_zip} {f_city}\n\nArtikli:\n"
                for pid, q in st.session_state.cart.items():
                    u_type = next(i["unit"] for i in PRODUCTS if i["id"] == pid)
                    body += f"- {T[pid]}: {q} {T['unit_'+u_type]}\n"
                body += f"\nUkupno: {total_price:.2f} EUR"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(body); msg['Subject'] = f"Narudžba 2026 - {f_name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except: st.error("E-mail server nije dostupan.")
            elif not st.session_state.cart: st.error("Košarica je prazna!")
            else: st.error("Popunite obavezna polja (*).")
