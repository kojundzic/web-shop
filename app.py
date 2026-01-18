import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# =================================================================
# TRAJNO USIDRENA KONFIGURACIJA - KOJUNDŽIĆ 2026.
# =================================================================

MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Resursi teksta i poruka sustava
T = {
    "nav_shop": "🏬 TRGOVINA", 
    "nav_horeca": "🏨 ZA UGOSTITELJE", 
    "nav_suppliers": "🚜 DOBAVLJAČI", 
    "nav_haccp": "🛡️ HACCP", 
    "nav_info": "ℹ️ O NAMA",
    "title_sub": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
    "cart_title": "🛒 Vaša košarica", 
    "cart_empty": "Vaša košarica je trenutno prazna.",
    "note_vaga": "⚖️ **VAŽNO:** Cijene su točne, ali zbog ručne obrade težina može minimalno odstupati.",
    "note_cod": "🚚 **Plaćanje pouzećem**",
    "form_fname": "Ime*", 
    "form_lname": "Prezime*", 
    "form_tel": "Kontakt telefon*", 
    "form_city": "Grad/Mjesto*", 
    "form_addr": "Ulica i kućni broj*",
    "btn_order": "🚀 POŠALJI NARUDŽBU", 
    "success": "✅ NARUDŽBA JE USPJEŠNO PREDANA!", 
    "err_fields": "🛑 NARUDŽBA ODBIJENA: Molimo ispunite sva polja označena zvjezdicom (*).",
    "err_cart": "🛑 NARUDŽBA ODBIJENA: Vaša košarica ne smije biti prazna!",
    "unit_kg": "kg", "unit_pc": "kom", "total": "Ukupni informativni iznos"
}

# Usidreni katalog proizvoda
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

# Inicijalizacija stanja
if 'cart' not in st.session_state:
    st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")

# LAYOUT
col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # Shop logika
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        for i, p in enumerate(PRODUCTS):
            with (c1 if i % 2 == 0 else c2):
                st.subheader(p["name"])
                st.write(f"**{p['price']:.2f} €** / {T['unit_'+p['unit']]}")
                cur_val = st.session_state.cart.get(p["id"], 0.0)
                step = 0.5 if p["unit"] == "kg" else 1.0
                new_val = st.number_input(f"Količina ({T['unit_'+p['unit']]})", 
                                         min_value=0.0, step=step, value=float(cur_val), key=f"in_{p['id']}")
                if new_val != cur_val:
                    if new_val > 0: st.session_state.cart[p["id"]] = new_val
                    else: st.session_state.cart.pop(p["id"], None)
                    st.rerun()

with col_right:
    st.markdown(f"### {T['cart_title']}")
    suma = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, q in list(st.session_state.cart.items()):
            p_inf = next((x for x in PRODUCTS if x["id"] == pid), None)
            if p_inf:
                sub = q * p_inf["price"]
                suma += sub
                st.write(f"✅ **{p_inf['name']}**: {q} {T['unit_'+p_inf['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{suma:.2f} €")
    st.warning(T["note_cod"])
    
    # FORMA ZA NARUDŽBU S USIDRENOM VALIDACIJOM
    with st.form("order_form", clear_on_submit=False):
        st.markdown("#### 📍 PODACI ZA DOSTAVU")
        f_ime = st.text_input(T["form_fname"])
        f_prezime = st.text_input(T["form_lname"])
        f_tel = st.text_input(T["form_tel"])
        f_grad = st.text_input(T["form_city"])
        f_adresa = st.text_input(T["form_addr"])
        
        submit_btn = st.form_submit_button(T["btn_order"], use_container_width=True)
        
        if submit_btn:
            if not st.session_state.cart:
                st.error(T["err_cart"]) # Crveni okvir za praznu košaricu
            elif not (f_ime and f_prezime and f_tel and f_grad and f_adresa):
                st.error(T["err_fields"]) # Crveni okvir za nepotpuna polja
            else:
                # Proces slanja
                detalji = "".join([f"- {next(it['name'] for it in PRODUCTS if it['id']==pid)}: {q}\n" for pid, q in st.session_state.cart.items()])
                email_body = f"Kupac: {f_ime} {f_prezime}\nTel: {f_tel}\nAdresa: {f_adresa}, {f_grad}\n\nNarudžba:\n{detalji}\nUKUPNO: {suma:.2f} €"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(email_body)
                    msg['Subject'] = f"Narudžba 2026: {f_ime} {f_prezime}"
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    
                    st.success(T["success"])
                    st.session_state.cart = {}
                    time.sleep(3)
                    st.rerun()
                except Exception as e:
                    st.error(f"Greška na serveru: {e}")
