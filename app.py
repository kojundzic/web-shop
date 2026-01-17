import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- APLIKACIJA ZA NARUČIVANJE: TRAJNO USIDRENI IZVORNI KOD (SISAK 2026) ---

# Fiksna konfiguracija (Usidreno)
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Fiksni tekstualni resursi s upozorenjima
T = {
    "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
    "title_sub": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
    "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
    "note_vaga": "⚖️ **VAŽNO:** Istaknute cijene proizvoda su točno navedene, dok je ukupni iznos u košarici informativne naravi. Budući da se naši proizvodi pripremaju i režu ručno, stvarna težina može malo odstupati.",
    "note_cod": "🚚 **Plaćanje pouzećem**",
    "form_fname": "Ime*", "form_lname": "Prezime*", "form_tel": "Kontakt telefon*", "form_city": "Grad/Mjesto*", "form_addr": "Ulica i kućni broj*",
    "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "✅ NARUDŽBA JE USPJEŠNO PREDANA!", 
    "err_fields": "🛑 NARUDŽBA SE NE MOŽE POSLATI: Niste ispunili sva obavezna polja za dostavu!",
    "err_cart": "🛑 NARUDŽBA SE NE MOŽE POSLATI: Vaša košarica je prazna!",
    "unit_kg": "kg", "unit_pc": "kom", "total": "Ukupni informativni iznos"
}

# Fiksni popis proizvoda
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

if 'cart' not in st.session_state:
    st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")

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
                cur_qty = st.session_state.cart.get(p["id"], 0.0)
                step = 0.5 if p["unit"] == "kg" else 1.0
                new_qty = st.number_input(f"Količina ({T['unit_'+p['unit']]})", 
                                         min_value=0.0, step=step, value=float(cur_qty), key=f"f_{p['id']}")
                if new_qty != cur_qty:
                    if new_qty > 0: st.session_state.cart[p["id"]] = new_qty
                    else: st.session_state.cart.pop(p["id"], None)
                    st.rerun()

with col_right:
    st.markdown(f"### {T['cart_title']}")
    ukupan_iznos = 0.0
    
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, q in list(st.session_state.cart.items()):
            p_inf = next((x for x in PRODUCTS if x["id"] == pid), None)
            if p_inf:
                sub = q * p_inf["price"]
                ukupan_iznos += sub
                st.write(f"✅ **{p_inf['name']}**: {q} {T['unit_'+p_inf['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{ukupan_iznos:.2f} €")
    st.warning(T["note_cod"])
    
    with st.form("forma_dostave", clear_on_submit=False):
        st.markdown("#### 📍 PODACI ZA DOSTAVU")
        f_ime = st.text_input(T["form_fname"])
        f_prezime = st.text_input(T["form_lname"])
        f_tel = st.text_input(T["form_tel"])
        f_grad = st.text_input(T["form_city"])
        f_adresa = st.text_input(T["form_addr"])
        
        # Gumb za slanje
        posalji = st.form_submit_button(T["btn_order"], use_container_width=True)
        
        if posalji:
            # VALIDACIJA 1: Prazna košarica
            if not st.session_state.cart:
                st.error(T["err_cart"])
            
            # VALIDACIJA 2: Neispunjena polja
            elif not (f_ime and f_prezime and f_tel and f_grad and f_adresa):
                st.error(T["err_fields"])
            
            # SVE JE ISPRAVNO: Slanje narudžbe
            else:
                stavke = "".join([f"- {next(it['name'] for it in PRODUCTS if it['id']==pid)}: {q} {T['unit_'+next(it['unit'] for it in PRODUCTS if it['id']==pid)]}\n" for pid, q in st.session_state.cart.items()])
                poruka = f"Kupac: {f_ime} {f_prezime}\nTel: {f_tel}\nGrad: {f_grad}\nAdresa: {f_adresa}\n\nNarudžba:\n{stavke}\nUkupno: {ukupan_iznos:.2f} €"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(poruka)
                    msg['Subject'] = f"Narudžba 2026 - {f_ime} {f_prezime}"
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    
                    st.success(T["success"])
                    st.session_state.cart = {}
                    time.sleep(3)
                    st.rerun()
                except Exception as e:
                    st.error(f"Sistemska greška: {e}")
