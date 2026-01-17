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

# --- 2. MASTER PRIJEVODI (POTPUNI I DETALJNI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "OBITELJSKA MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "note_vaga": "⚖️ **VAŽNA NAPOMENA O VAGANJU:** Cijene su fiksne po jedinici, no točan iznos računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja.",
        "note_delivery": "🚚 **DOSTAVA I PLAĆANJE:** Pakete šaljemo u termo-izoliranoj ambalaži. Plaćanje je isključivo **pouzećem** (gotovinom dostavljaču).",
        "horeca_title": "HoReCa Partnerstvo",
        "horeca_text": "Za ugostitelje nudimo posebne uvjete i tradicionalno dimljene proizvode. \n📬 Upite šaljite na: [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Podrijetlo: Banovina, Posavina i Lonjsko polje",
        "suppliers_text": "Meso dolazi isključivo s domaćih pašnjaka i farmi s područja Banovine, Posavine i Lonjskog polja.",
        "haccp_title": "🛡️ Sigurnost hrane i HACCP",
        "haccp_text": "Najviši higijenski standardi uz potpunu digitalnu sljedivost od farme do Vašeg stola.",
        "info_title": "ℹ️ O nama i lokacija",
        "info_text": "Obitelj Kojundžić čuva tradiciju bez aditiva. \n📍 **LOKACIJA:** Gradska tržnica Kontroba, Sisak.",
        "form_name": "Ime i Prezime primatelja*", "form_tel": "Kontakt telefon*", "form_country": "Država*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI KONAČNU NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos računa", "shipping_info": "📍 POTPUNI PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek (svinjska koljenica)", "p3": "Dimljeni prsni vršci", "p4": "Domaća slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti za juhu",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska kvaliteta)", "p9": "Dimljeni vrat bez kosti", "p10": "Dimljeni kare bez kosti", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (tradicionalne)", "p15": "Pečenice za roštilj", "p16": "Suha svinjska rebra", "p17": "Dimljena svinjska glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is empty.",
        "note_vaga": "⚖️ Final prices are determined after weighing before packaging.",
        "note_delivery": "🚚 Thermo-insulated shipping. Payment: Cash on Delivery.",
        "horeca_title": "HoReCa", "horeca_text": "Inquiries: [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Origin", "suppliers_text": "Meat from Banovina, Posavina and Lonjsko Polje.",
        "haccp_title": "🛡️ HACCP", "haccp_text": "Highest safety standards.",
        "info_title": "ℹ️ About Us", "info_text": "📍 LOCATION: Sisak City Market.",
        "form_name": "Full Name*", "form_tel": "Phone*", "form_country": "Country*", "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "📍 SHIPPING DETAILS",
        "p1": "Smoked Bacon", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Soup Bones",
        "p7": "Smoked Trotters", "p8": "Premium Pancetta", "p9": "Smoked Neck", "p10": "Smoked Loin", "p11": "Smoked Tenderloin", "p12": "Cracklings",
        "p13": "Pork Lard", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Pork Head", "p18": "White Bacon"
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

# --- 4. SESSION STATE LOGIKA (FIKSIRANO) ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- 5. UI SETUP ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

col_main, col_side = st.columns([0.65, 0.35])

# --- SREDINA: ARTIKLI I RUBRIKE ---
with col_main:
    st.header(T["title_sub"])
    tab_shop, tab_horeca, tab_suppliers, tab_haccp, tab_info = st.tabs([
        T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]
    ])
    
    with tab_shop:
        cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols[idx % 2]:
                st.subheader(T.get(p["id"], p["id"]))
                st.write(f"Cijena: **{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                
                # JEDINSTVENA LOGIKA ZA KILOGRAME
                curr_val = st.session_state.cart.get(p["id"], 0.0)
                
                if p["unit"] == "kg":
                    val = st.number_input(f"Količina ({T['unit_kg']})", min_value=0.0, step=0.5, value=curr_val, key=f"inp_{p['id']}")
                    # Ako skoči s 0.0 na 0.5, force na 1.0
                    if curr_val == 0.0 and val == 0.5:
                        val = 1.0
                        st.rerun() # Forsira osvježavanje s novom vrijednošću
                else:
                    val = st.number_input(f"Količina ({T['unit_pc']})", min_value=0.0, step=1.0, value=curr_val, key=f"inp_{p['id']}")
                
                if val > 0:
                    st.session_state.cart[p["id"]] = val
                elif p["id"] in st.session_state.cart:
                    del st.session_state.cart[p["id"]]

    with tab_horeca: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tab_suppliers: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tab_haccp: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tab_info: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA: KOŠARICA, IZNOS I DOSTAVA (FIKSNO) ---
with col_side:
    st.markdown(f"### {T['cart_title']}")
    total_val = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, qty in list(st.session_state.cart.items()):
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_val += sub
            st.write(f"✅ **{T.get(pid, pid)}**: {qty} {T['unit_'+p_inf['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    
    # Iznos i Napomene
    st.metric(label=T["total"], value=f"{total_val:.2f} €")
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    # PODACI ZA DOSTAVU
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("delivery_2026"):
        f_name = st.text_input(T["form_name"])
        f_tel = st.text_input(T["form_tel"])
        f_country = st.text_input(T["form_country"], value="Hrvatska")
        f_city = st.text_input(T["form_city"])
        f_zip = st.text_input(T["form_zip"])
        f_addr = st.text_input(T["form_addr"])
        
        if st.form_submit_button(T["btn_order"]):
            if f_name and f_tel and f_addr and st.session_state.cart:
                # Slanje
                mail_body = f"NARUDŽBA 2026\nKupac: {f_name}\nTel: {f_tel}\nDržava: {f_country}\nAdresa: {f_addr}, {f_zip} {f_city}\n\nArtikli:\n"
                for pid, q in st.session_state.cart.items():
                    u = next(i["unit"] for i in PRODUCTS if i["id"] == pid)
                    mail_body += f"- {T.get(pid, pid)}: {q} {T['unit_'+u]}\n"
                mail_body += f"\nUkupno: {total_val:.2f} EUR"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(mail_body); msg['Subject'] = f"Narudžba {f_name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except: st.error("Greška s e-mail serverom.")
            elif not st.session_state.cart: st.error("Košarica je prazna!")
            else: st.error("Popunite sva obavezna polja (*).")
