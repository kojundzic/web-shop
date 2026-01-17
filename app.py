import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. USIDRENA KONFIGURACIJA ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EU_DRZAVE = [
    "Hrvatska", "Austrija", "Belgija", "Bugarska", "Cipar", "Češka", "Danska", "Estonija", 
    "Finska", "Francuska", "Grčka", "Irska", "Italija", "Latvija", "Litva", "Luksemburg", 
    "Mađarska", "Malta", "Nizozemska", "Njemačka", "Poljska", "Portugal", "Rumunjska", 
    "Slovačka", "Slovenija", "Španjolska", "Švedska", "Druga država (upiši sam)"
]

T = {
    "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
    "title_sub": "OBITELJSKA MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
    "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
    "note_vaga": "⚖️ **VAŽNO:** Cijene su točne, dok je ukupni iznos informativan. Točan iznos znat ćete pri preuzimanju.",
    "note_delivery": "🚚 **DOSTAVA:** Proizvode šaljemo dostavom, plaćate ih pouzećem.",
    "form_fname": "Ime*", "form_lname": "Prezime*", "form_tel": "Kontakt telefon*", "form_country": "Država*", "form_city": "Grad/Mjesto*", "form_addr": "Ulica i kućni broj*",
    "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", 
    "err_fields": "🛑 Narudžba se ne može poslati dok ne ispunite sva obavezna polja!",
    "err_cart": "🛑 Vaša košarica je prazna! Dodajte artikle prije slanja.",
    "unit_kg": "kg", "unit_pc": "kom", "total": "Ukupni informativni iznos", "shipping_info": "📍 PODACI ZA DOSTAVU"
}

PRODUCTS = [
    {"id": "p1", "price": 9.50, "unit": "kg", "name": "Dimljeni hamburger"},
    {"id": "p2", "price": 7.80, "unit": "pc", "name": "Dimljeni buncek"},
    {"id": "p3", "price": 6.50, "unit": "pc", "name": "Dimljeni prsni vršci"},
    {"id": "p4", "price": 14.20, "unit": "kg", "name": "Slavonska kobasica"},
    {"id": "p5", "price": 17.50, "unit": "kg", "name": "Domaća salama"},
    {"id": "p6", "price": 3.80, "unit": "kg", "name": "Dimljene kosti"},
    {"id": "p7", "price": 4.50, "unit": "kg", "name": "Dimljene nogice mix"},
    {"id": "p8", "price": 16.90, "unit": "kg", "name": "Panceta"},
    {"id": "p9", "price": 12.50, "unit": "kg", "name": "Dimljeni vrat (BK)"},
    {"id": "p10", "price": 13.50, "unit": "kg", "name": "Dimljeni kare (BK)"},
    {"id": "p11", "price": 15.00, "unit": "kg", "name": "Dimljena pečenica"},
    {"id": "p12", "price": 18.00, "unit": "kg", "name": "Domaći čvarci"},
    {"id": "p13", "price": 10.00, "unit": "pc", "name": "Svinjska mast (kanta)"},
    {"id": "p14", "price": 9.00, "unit": "kg", "name": "Krvavice"},
    {"id": "p15", "price": 10.50, "unit": "kg", "name": "Pečenice za roštilj"},
    {"id": "p16", "price": 8.50, "unit": "kg", "name": "Suha rebra"},
    {"id": "p17", "price": 5.00, "unit": "pc", "name": "Dimljena glava"},
    {"id": "p18", "price": 9.00, "unit": "kg", "name": "Slanina sapunara"}
]

# --- 2. INICIJALIZACIJA ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
msg_placeholder = st.empty()

col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # SHOP
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        for i, p in enumerate(PRODUCTS):
            with (c1 if i % 2 == 0 else c2):
                st.subheader(p["name"])
                st.write(f"**{p['price']:.2f} €** / {T['unit_'+p['unit']]}")
                
                # KLJUČNA LOGIKA: Session state se koristi kao primarni izvor istine
                current_qty = st.session_state.cart.get(p["id"], 0.0)
                step = 0.5 if p["unit"] == "kg" else 1.0
                
                # Widget koji reagira na promjenu
                val = st.number_input(f"Količina ({T['unit_'+p['unit']]})", 
                                     min_value=0.0, step=step, value=float(current_qty), key=f"f_{p['id']}")
                
                # Logika vage za KG
                if p["unit"] == "kg":
                    if current_qty == 0.0 and val == 0.5: val = 1.0
                    elif current_qty == 1.0 and val == 0.5: val = 0.0

                # Ako je došlo do promjene, upiši u košaricu i ODMAH osvježi da se cijena izračuna
                if val != current_qty:
                    if val > 0: st.session_state.cart[p["id"]] = val
                    else: st.session_state.cart.pop(p["id"], None)
                    st.rerun()

with col_right:
    st.markdown(f"### {T['cart_title']}")
    ukupan_iznos = 0.0
    
    # IZRAČUN CIJENA - OVO SADA RADI U REALNOM VREMENU
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, qty in list(st.session_state.cart.items()):
            p_info = next((x for x in PRODUCTS if x["id"] == pid), None)
            if p_info:
                sub = qty * p_info["price"]
                ukupan_iznos += sub
                st.write(f"✅ **{p_info['name']}**: {qty} {T['unit_'+p_info['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{ukupan_iznos:.2f} €")
    
    with st.form("forma_dostave"):
        st.markdown(f"#### {T['shipping_info']}")
        c_n1, c_n2 = st.columns(2)
        with c_n1: ime = st.text_input(T["form_fname"])
        with c_n2: prezime = st.text_input(T["form_lname"])
        
        tel = st.text_input(T["form_tel"])
        drzava_izbor = st.selectbox(T["form_country"], options=EU_DRZAVE)
        drzava_final = drzava_izbor
        if drzava_izbor == "Druga država (upiši sam)":
            drzava_final = st.text_input("Upišite naziv države*")
        
        grad = st.text_input(T["form_city"])
        adresa = st.text_input(T["form_addr"])
        posalji = st.form_submit_button(T["btn_order"])
        
        if posalji:
            if not st.session_state.cart:
                msg_placeholder.error(T["err_cart"])
                time.sleep(5); msg_placeholder.empty()
            elif not (ime and prezime and tel and grad and adresa and drzava_final):
                msg_placeholder.error(T["err_fields"])
                time.sleep(5); msg_placeholder.empty()
            else:
                stavke = "".join([f"- {next(it['name'] for it in PRODUCTS if it['id']==pid)}: {q} {T['unit_'+next(it['unit'] for it in PRODUCTS if it['id']==pid)]}\n" for pid, q in st.session_state.cart.items()])
                poruka = f"Kupac: {ime} {prezime}\nTel: {tel}\nDržava: {drzava_final}\nGrad: {grad}\nAdresa: {adresa}\n\nNarudžba:\n{stavke}\nUkupno: {ukupan_iznos:.2f} €"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(poruka)
                    msg['Subject'] = f"Narudžba 2026 - {ime} {prezime}"
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    
                    msg_placeholder.success("### VAŠA NARUDŽBA JE ZAPRIMLJENA, HVALA!")
                    st.success(T["success"])
                    st.session_state.cart = {}
                    time.sleep(5); msg_placeholder.empty()
                    time.sleep(5); st.rerun()
                except Exception as e:
                    st.error(f"E-mail greška: {e}")
