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

# --- 2. PROŠIRENI PRIJEVODI I PERSONALIZACIJA (2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je prazna.",
        "note_vaga": """⚖️ **NAPOMENA O VAGANJU:** U našoj mesnici poštujemo prirodni rez svakog komada. Cijene su fiksne po jedinici, ali konačan iznos računa formira se nakon preciznog vaganja neposredno prije pakiranja.""",
        "note_delivery": """🚚 **DOSTAVA I PLAĆANJE:** Pakete šaljemo u termo-izoliranoj ambalaži. Plaćanje je isključivo **pouzećem (gotovinom)** prilikom preuzimanja.""",
        "horeca_title": "HoReCa Partnerstvo 2026.",
        "horeca_text": "Vrhunsko meso s tradicionalnim dimljenjem na bukvi za restorane i hotele. Osigurana logistika hladnim lancem.",
        "suppliers_title": "🚜 Podrijetlo: Banovina, Posavina i Lonjsko polje",
        "suppliers_text": "Surađujemo isključivo s lokalnim OPG-ovima. Naše meso dolazi s ekološki očuvanih pašnjaka našeg kraja.",
        "haccp_title": "🛡️ Sigurnost i Sljedivost",
        "haccp_text": "Najstroži HACCP standardi u 2026. Svaki komad mesa ima dokumentiran put od pašnjaka do Vašeg stola.",
        "info_title": "ℹ️ O nama: Obitelj Kojundžić",
        "info_text": "Tradicija, sol i dim. Na tržnici u Sisku nudimo čisto domaće meso bez aditiva.",
        "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA USPJEŠNO PRIMLJENA!", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "📍 PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is empty.",
        "note_vaga": """⚖️ **WEIGHT NOTE:** Final prices are determined after precise weighing during packaging.""",
        "note_delivery": """🚚 **DELIVERY:** Shipped in thermo-boxes. Payment: **Cash on Delivery**.""",
        "horeca_title": "HoReCa Partnership", "horeca_text": "Premium meats for professional kitchens with beech-wood smoking.",
        "suppliers_title": "🚜 Origin", "suppliers_text": "Meat from Banovina, Posavina, and Lonjsko Polje regions.",
        "haccp_title": "🛡️ Safety", "haccp_text": "Strict 2026 HACCP standards and full digital traceability.",
        "info_title": "ℹ️ Our Story", "info_text": "Family tradition at Sisak Market. No additives, just natural smoke.",
        "form_name": "Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "btn_order": "🚀 ORDER", "success": "ORDER RECEIVED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "📍 SHIPPING DETAILS",
        "p1": "Smoked Bacon", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters", "p8": "Premium Pancetta", "p9": "Smoked Neck", "p10": "Smoked Loin", "p11": "Smoked Tenderloin", "p12": "Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Pork Head", "p18": "White Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Warenkorb ist leer.",
        "note_vaga": """⚖️ **WIEGEHINWEIS:** Endpreise werden nach dem Wiegen beim Verpacken ermittelt.""",
        "note_delivery": """🚚 **LIEFERUNG:** Versand in Thermoboxen. Zahlung per **Nachnahme**.""",
        "horeca_title": "HoReCa Partner", "horeca_text": "Premium-Fleisch für die Gastronomie mit Buchenholzrauch.",
        "suppliers_title": "🚜 Herkunft", "suppliers_text": "Fleisch aus Banovina, Posavina und Lonjsko Polje.",
        "haccp_title": "🛡️ Sicherheit", "haccp_text": "Strenge HACCP-Kontrollen und digitale Rückverfolgbarkeit.",
        "info_title": "ℹ️ Über uns", "info_text": "Familientradition in Sisak. Nur Salz, Gewürze und Rauch.",
        "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "🚀 BESTELLEN", "success": "BESTELLUNG ERHALTEN!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "📍 LIEFERDATEN",
        "p1": "Geräucherter Speck", "p2": "Geräucherte Stelze", "p3": "Geräucherte Spitzen", "p4": "Slawonische Wurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Schweinefüße", "p8": "Pancetta Premium", "p9": "Geräucherter Nacken", "p10": "Karree", "p11": "Lendenstück", "p12": "Grieben",
        "p13": "Schweineschmalz", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Schweinekopf", "p18": "Speck weiß"
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

# --- 4. UI STRUKTURA ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

col_left, col_right = st.columns([0.62, 0.38])

# --- LIJEVA STRANA: ARTIKLI I RUBRIKE ---
with col_left:
    st.title(T["title_sub"])
    tab_shop, tab_horeca, tab_suppliers, tab_haccp, tab_info = st.tabs([
        T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]
    ])
    
    with tab_shop:
        cols_shop = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_shop[idx % 2]:
                st.subheader(T[p["id"]])
                st.write(f"**{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                
                # Logika: kg kreće od 0, prvi klik je 1.0, dalje ide po 0.5
                if p["unit"] == "kg":
                    q = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5, value=0.0, key=f"s_{p['id']}")
                    if q == 0.5: # Ako korisnik klikne jednom na plus sa 0.0 na 0.5, force na 1.0
                        q = 1.0
                        st.info("Minimalna narudžba za ovaj artikl je 1 kg.")
                else:
                    q = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=1.0, value=0.0, key=f"s_{p['id']}")
                
                if q > 0: st.session_state.cart[p["id"]] = q
                elif p["id"] in st.session_state.cart: del st.session_state.cart[p["id"]]

    with tab_horeca: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tab_suppliers: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tab_haccp: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tab_info: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA: NAPOMENE, KOŠARICA I DOSTAVA (STALNO VIDLJIVO) ---
with col_right:
    # 1. Napomene na vrhu (uočljive)
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    st.markdown(f"### {T['cart_title']}")
    
    total_price = 0.0
    if not st.session_state.cart:
        st.write(T["cart_empty"])
    else:
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_price += sub
            st.write(f"🔸 **{T[pid]}**: {qty} {T['unit_'+p_inf['unit']]} = {sub:.2f} €")
        
        st.divider()
        st.metric(label=T["total"], value=f"{total_price:.2f} €")

    # 2. Podaci za dostavu ispod napomena i košarice
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("delivery_form_right"):
        f_name = st.text_input(T["form_name"])
        f_tel = st.text_input(T["form_tel"])
        f_city = st.text_input(T["form_city"])
        f_zip = st.text_input(T["form_zip"])
        f_addr = st.text_input(T["form_addr"])
        
        submit = st.form_submit_button(T["btn_order"])
        
        if submit:
            if f_name and f_tel and f_addr and st.session_state.cart:
                # Slanje narudžbe e-mailom
                body = f"NARUDŽBA 2026 - KOJUNDŽIĆ\n\nKupac: {f_name}\nTel: {f_tel}\nAdresa: {f_addr}, {f_zip} {f_city}\n\nStavke:\n"
                for pid, qty in st.session_state.cart.items():
                    body += f"- {T[pid]}: {qty}\n"
                body += f"\nUkupno (informativno): {total_price:.2f} EUR"

                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(body); msg['Subject'] = f"Narudžba {f_name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except Exception as e: st.error(f"Sustav trenutno nije dostupan. Greška: {e}")
            elif not st.session_state.cart:
                st.error("Vaša košarica je prazna!")
            else:
                st.error("Molimo ispunite sva polja označena zvjezdicom (*).")
