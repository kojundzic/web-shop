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

# --- 2. MASTER PRIJEVODI (PRECIZNI I POTPUNI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je prazna",
        "note_vaga": """⚖️ **NAPOMENA O VAGANJU:** Cijene proizvoda su fiksne po jedinici mjere, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Trudimo se da odstupanja od naručene količine budu minimalna.""",
        "note_delivery": """🚚 **DOSTAVA I PLAĆANJE:** Proizvode šaljemo u termo-izoliranoj ambalaži. Plaćanje se vrši **isključivo pouzećem** (gotovinom prilikom preuzimanja).""",
        "horeca_title": "HoReCa Partnerstvo 2026.",
        "horeca_text": "Kao obiteljska manufaktura, nudimo beskompromisnu kvalitetu sirovine. Naša ponuda uključuje tradicionalno dimljenje na bukvi, vlastitu hladnjaču i stabilnost cijena za restorane.",
        "suppliers_title": "🚜 Podrijetlo sirovine",
        "suppliers_text": "Ponosni smo što naše meso dolazi isključivo s domaćih pašnjaka **Banovine, Posavine i Lonjskog polja**. Kratak lanac opskrbe jamči vrhunsku svježinu.",
        "haccp_title": "🛡️ Sigurnost hrane (HACCP)",
        "haccp_text": "U 2026. godini primjenjujemo najnovije tehnologije nadzora. Svaki komad mesa ima potpunu sljedivost od farme do Vašeg stola pod veterinarskim nadzorom.",
        "info_title": "ℹ️ O nama",
        "info_text": "Obitelj Kojundžić u srcu Siska čuva vještinu tradicionalne pripreme mesa bez aditiva, uz korištenje domaćih začina i dima bukve i graba.",
        "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos računa", "shipping_info": "📍 POTPUNI PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is empty",
        "note_vaga": """⚖️ **WEIGHT NOTE:** Prices are fixed per unit, but the exact total will be determined after precise weighing just before packaging.""",
        "note_delivery": """🚚 **SHIPPING & PAYMENT:** Products are shipped in thermo-insulated packaging. Payment is **Cash on Delivery (COD)** only.""",
        "horeca_title": "HoReCa Partnership 2026", "horeca_text": "We offer premium raw materials, traditional beech smoking, and cold-chain logistics for the hospitality sector.",
        "suppliers_title": "🚜 Meat Origin", "suppliers_text": "Our meat comes exclusively from domestic pastures of **Banovina, Posavina, and Lonjsko Polje**.",
        "haccp_title": "🛡️ Food Safety (HACCP)", "haccp_text": "Every piece of meat has full digital traceability from farm to table.",
        "info_title": "ℹ️ About Us", "info_text": "The Kojundžić family in Sisak preserves traditional meat preparation using heritage recipes.",
        "form_name": "Full Name*", "form_tel": "Phone Number*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & Number*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Invoice Total", "shipping_info": "📍 COMPLETE DELIVERY DETAILS"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Warenkorb ist leer",
        "note_vaga": """⚖️ **WIEGEHINWEIS:** Die Preise pro Einheit sind fest, aber der genaue Betrag wird erst nach dem Wiegen ermittelt.""",
        "note_delivery": """🚚 **LIEFERUNG & ZAHLUNG:** Versand in Thermoverpackung. Die Zahlung erfolgt **ausschließlich per Nachnahme**.""",
        "horeca_title": "HoReCa Partnerschaft 2026", "horeca_text": "Wir bieten erstklassige Rohstoffe und traditionelle Buchenräucherung für die Gastronomie.",
        "suppliers_title": "🚜 Herkunft des Fleisches", "suppliers_text": "Fleisch ausschließlich von heimischen Weiden aus **Banovina, Posavina und Lonjsko Polje**.",
        "haccp_title": "🛡️ Lebensmittelsicherheit", "haccp_text": "Im Jahr 2026 ist jedes Stück Fleisch vom Bauernhof bis zum Tisch rückverfolgbar.",
        "info_title": "ℹ️ Über uns", "info_text": "Familie Kojundžić bewahrt die Kunst der traditionellen Fleischzubereitung in Sisak.",
        "form_name": "Name*", "form_tel": "Telefonnummer*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "🚀 BESTELLUNG SENDEN", "success": "BESTELLUNG ERFOLGREICH!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Informativ Rechnungsbetrag", "shipping_info": "📍 VOLLSTÄNDIGE LIEFERDATEN"
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

# Glavni layout: Sredina (65%) | Desno (35%)
col_main, col_side = st.columns([0.65, 0.35])

# --- LIJEVA STRANA: ARTIKLI I RUBRIKE ---
with col_main:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # SHOP
        cols_shop = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_shop[idx % 2]:
                st.subheader(T.get(p["id"], p["id"]))
                st.write(f"Cijena: **{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                
                # LOGIKA: 0 -> 1.0 (na prvi klik) -> 1.5...
                if p["unit"] == "kg":
                    val = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5, value=0.0, key=f"shop_{p['id']}")
                    if 0.1 <= val <= 0.5: 
                        val = 1.0
                else:
                    val = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=1.0, value=0.0, key=f"shop_{p['id']}")
                
                if val > 0: st.session_state.cart[p["id"]] = val
                elif p["id"] in st.session_state.cart: del st.session_state.cart[p["id"]]

    with tabs[1]: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs[2]: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs[3]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs[4]: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA: NAPOMENE, KOŠARICA I DOSTAVA (FIKSNO VIDLJIVO) ---
with col_side:
    # 1. Napomene na vrhu
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    # 2. Košarica i Informativni iznos
    st.markdown(f"### {T['cart_title']}")
    total_val = 0.0
    if not st.session_state.cart:
        st.write(T["cart_empty"])
    else:
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_val += sub
            st.write(f"✅ **{T.get(pid, pid)}**: {qty} {T['unit_'+p_inf['unit']]} = {sub:.2f} €")
        
        st.divider()
        st.metric(label=T["total"], value=f"{total_val:.2f} €")
    
    # 3. Potpuni podaci za dostavu
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("sidebar_form"):
        name = st.text_input(T["form_name"])
        tel = st.text_input(T["form_tel"])
        city = st.text_input(T["form_city"])
        zip_c = st.text_input(T["form_zip"])
        addr = st.text_input(T["form_addr"])
        
        if st.form_submit_button(T["btn_order"]):
            if name and tel and addr and st.session_state.cart:
                # E-mail narudžba
                body = f"NOVA NARUDŽBA 2026\n\nKupac: {name}\nTel: {tel}\nAdresa: {addr}, {zip_c} {city}\n\nArtikli:\n"
                for pid, q in st.session_state.cart.items():
                    body += f"- {T.get(pid, pid)}: {q}\n"
                body += f"\nInformativni iznos: {total_val:.2f} EUR"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(body); msg['Subject'] = f"Narudžba 2026 - {name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except: st.error("Sustav e-pošte trenutno nije dostupan.")
            elif not st.session_state.cart:
                st.error("Košarica je prazna!")
            else:
                st.error("Ispunite obavezna polja (*).")
