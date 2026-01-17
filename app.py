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

# --- 2. MASTER PRIJEVODI (PROŠIRENI I PERSONALIZIRANI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": """⚖️ **NAPOMENA O VAGANJU:** Cijene su fiksne, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Trudimo se da se pridržavamo naručenih količina.""",
        "note_delivery": """🚚 **DOSTAVA I PLAĆANJE:** Šaljemo putem dostavne službe. Plaćanje se vrši **isključivo pouzećem** (gotovinom dostavljaču).""",
        "horeca_title": "HoReCa Partnerstvo 2026.",
        "horeca_text": "Kao obiteljska manufaktura, nudimo beskompromisnu kvalitetu sirovine. Naša ponuda uključuje tradicionalno dimljenje na bukvi, vlastitu hladnjaču i stabilnost cijena za restorane.",
        "suppliers_title": "🚜 Naši Dobavljači",
        "suppliers_text": "Ponosni smo što naše meso dolazi isključivo s domaćih pašnjaka **Banovine, Posavine i Lonjskog polja**. Kratak lanac opskrbe jamči svježinu.",
        "haccp_title": "🛡️ HACCP Standardi",
        "haccp_text": "U 2026. godini primjenjujemo najnovije tehnologije nadzora. Svaki komad mesa ima potpunu sljedivost od farme do Vašeg stola.",
        "info_title": "ℹ️ O Nama",
        "info_text": "Obitelj Kojundžić u srcu Siska čuva vještinu tradicionalne pripreme mesa bez aditiva, uz korištenje domaćih začina i dima.",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "is empty",
        "note_vaga": "⚖️ **WEIGHT NOTE:** Final prices are determined after weighing before packaging.",
        "note_delivery": "🚚 **DELIVERY:** Cash on Delivery only.",
        "horeca_title": "HoReCa 2026", "horeca_text": "Premium meat for restaurants with traditional beech smoking.",
        "suppliers_title": "🚜 Suppliers", "suppliers_text": "Meat sourced from Banovina, Posavina, and Lonjsko Polje.",
        "haccp_title": "🛡️ HACCP", "haccp_text": "Full traceability and modern safety standards.",
        "info_title": "ℹ️ About Us", "info_text": "Traditional Sisak butchery using heritage recipes and natural spices.",
        "form_name": "Full Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "SHIPPING DETAILS"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "ist leer",
        "note_vaga": "⚖️ **WIEGEHINWEIS:** Endpreise werden nach dem Wiegen ermittelt.",
        "note_delivery": "🚚 **LIEFERUNG:** Zahlung per Nachnahme.",
        "horeca_title": "HoReCa 2026", "horeca_text": "Premium-Fleisch für die Gastronomie mit traditioneller Räucherung.",
        "suppliers_title": "🚜 Lieferanten", "suppliers_text": "Fleisch aus den Regionen Banovina, Posavina und Lonjsko Polje.",
        "haccp_title": "🛡️ HACCP", "haccp_text": "Vollständige Rückverfolgbarkeit und moderne Sicherheitsstandards.",
        "info_title": "ℹ️ Über uns", "info_text": "Traditionelle Metzgerei aus Sisak mit natürlichen Gewürzen.",
        "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "🚀 BESTELLEN", "success": "BESTELLUNG ERHALTEN!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "LIEFERDATEN"
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

# Glavni layout: Sredina (Artikli/Rubrike) i Desno (Košarica/Podaci)
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
                st.write(f"**{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                
                # Logika: 0 -> 1.0 -> 1.5...
                if p["unit"] == "kg":
                    val = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5, value=0.0, key=f"in_{p['id']}")
                    if 0.1 <= val <= 0.5: val = 1.0 # Force na 1kg na prvi klik
                else:
                    val = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=1.0, value=0.0, key=f"in_{p['id']}")
                
                if val > 0: st.session_state.cart[p["id"]] = val
                elif p["id"] in st.session_state.cart: del st.session_state.cart[p["id"]]

    with tabs[1]: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs[2]: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs[3]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs[4]: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNO: NAPOMENE, KOŠARICA I PODACI (STALNO VIDLJIVO) ---
with col_side:
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    st.markdown(f"### {T['cart_title']}")
    total_val = 0.0
    if not st.session_state.cart:
        st.write(T["cart_empty"])
    else:
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_val += sub
            st.write(f"🔸 **{T.get(pid, pid)}**: {qty} {T['unit_'+p_inf['unit']]} = {sub:.2f} €")
        
        st.divider()
        st.metric(label=T["total"], value=f"{total_val:.2f} €")
    
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("sidebar_form"):
        name = st.text_input(T["form_name"])
        tel = st.text_input(T["form_tel"])
        city = st.text_input(T["form_city"])
        zip_c = st.text_input(T["form_zip"])
        addr = st.text_input(T["form_addr"])
        
        if st.form_submit_button(T["btn_order"]):
            if name and tel and addr and st.session_state.cart:
                # E-mail logika
                body = f"NARUDŽBA 2026\nKupac: {name}\nTel: {tel}\nAdresa: {addr}, {zip_c} {city}\n\n"
                for pid, q in st.session_state.cart.items():
                    body += f"- {T.get(pid, pid)}: {q}\n"
                body += f"\nUkupno cca: {total_val:.2f} EUR"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(body); msg['Subject'] = f"Narudžba {name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except: st.error("Greška pri slanju.")
            else: st.error("Popunite podatke i dodajte artikle.")
