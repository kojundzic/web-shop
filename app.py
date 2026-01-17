import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. PRIJEVODI I ARTIKLI ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛍️ Vaša Košarica",
        "cart_empty": "Vaša košarica je prazna.", 
        "note_vaga": "⚖️ **Napomena:** Navedene cijene su informativne. Točan iznos bit će poznat nakon vaganja.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i broj*",
        "form_country": "Država*", "btn_order": "✅ POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom",
        "horeca_title": "Profesionalna usluga", "horeca_text": "Posebne pogodnosti za restorane i hotele.",
        "horeca_mail": "Kontakt:", "haccp_title": "HACCP Standardi", "haccp_text": "Proizvodnja po najvišim standardima 2026.",
        "info_title": "Tradicija Kojundžić", "info_text": "Domaće meso iz okolice Siska, pripremljeno na tradicionalan način.",
        "shipping_data": "Podaci za dostavu:",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", 
        "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti", 
        "p7": "Dimljene nogice mix", "p8": "Panceta", "p9": "Dimljeni vrat (BK)", 
        "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Čvarci"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 B2B SERVICE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP | 2026.", "cart_title": "🛍️ Your Cart", "cart_empty": "Empty cart.",
        "note_vaga": "⚖️ Final price after weighing.", "total": "Total approx.",
        "form_name": "Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "ZIP*",
        "form_addr": "Address*", "form_country": "Country*", "btn_order": "✅ CONFIRM", "success": "Success!",
        "unit_kg": "kg", "unit_pc": "pcs", "horeca_title": "B2B", "horeca_text": "Wholesale prices.",
        "horeca_mail": "Contact:", "haccp_title": "HACCP", "haccp_text": "Safety 2026.",
        "info_title": "Tradition", "info_text": "Traditional meat processing from Sisak.",
        "shipping_data": "Shipping:", "p1": "Smoked bacon", "p2": "Smoked hock", "p3": "Smoked brisket",
        "p4": "Sausage", "p5": "Salami", "p6": "Bones", "p7": "Feet", "p8": "Pancetta",
        "p9": "Smoked neck", "p10": "Smoked loin", "p11": "Tenderloin", "p12": "Pork rinds"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 3. LOGIKA ZA EMAIL ---
def posalji_email(ime, telefon, grad, adr, detalji, ukupno, jezik, country, ptt):
    predmet = f"🔴 NOVA NARUDŽBA 2026: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nZemlja: {country}\nLokacija: {ptt} {grad}\nAdresa: {adr}\n\nArtikli:\n{detalji}\nUkupno: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 4. DIZAJN ---
st.markdown("""<style>
    .brand-name { color: #8B0000; font-size: 35px; font-weight: 900; text-align: center; margin:0; }
    .brand-sub { color: #333; font-size: 14px; text-align: center; margin-bottom: 15px; }
    .product-card { background: #ffffff; border-radius: 8px; padding: 10px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .qty-display { font-size: 18px; font-weight: bold; color: #8B0000; }
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 5. NAVIGACIJA ---
izabrani_jezik = st.sidebar.selectbox("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
choice = st.sidebar.radio("Meni", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

# --- 6. TRGOVINA ---
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)
    col_proizvodi, col_desno = st.columns([0.65, 0.35])
    proizvodi = [
        {"id": 1, "name": T["p1"], "price": 12.0, "type": "kg"}, {"id": 2, "name": T["p2"], "price": 8.0, "type": "pc"},
        {"id": 3, "name": T["p3"], "price": 9.0, "type": "pc"}, {"id": 4, "name": T["p4"], "price": 16.0, "type": "kg"},
        {"id": 5, "name": T["p5"], "price": 25.0, "type": "kg"}, {"id": 6, "name": T["p6"], "price": 2.5, "type": "kg"},
        {"id": 7, "name": T["p7"], "price": 2.5, "type": "kg"}, {"id": 8, "name": T["p8"], "price": 17.0, "type": "kg"},
        {"id": 9, "name": T["p9"], "price": 15.0, "type": "kg"}, {"id": 10, "name": T["p10"], "price": 15.0, "type": "kg"},
        {"id": 11, "name": T["p11"], "price": 20.0, "type": "kg"}, {"id": 12, "name": T["p12"], "price": 10.0, "type": "pc"}
    ]
    with col_proizvodi:
        cols = st.columns(2)
        for idx, p in enumerate(proizvodi):
            with cols[idx % 2]:
                st.markdown(f'<div class="product-card"><h4>{p["name"]}</h4><p>{p["price"]} € / {T["unit_kg"] if p["type"]=="kg" else T["unit_pc"]}</p></div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1,1,1])
                if c1.button("➖", key=f"m_{p['id']}"):
                    if p['id'] in st.session_state.cart and st.session_state.cart[p['id']] > 0:
                        st.session_state.cart[p['id']] -= 1
                c2.markdown(f'<div style="text-align:center" class="qty-display">{st.session_state.cart.get(p["id"], 0)}</div>', unsafe_allow_html=True)
                if c3.button("➕", key=f"p_{p['id']}"):
                    st.session_state.cart[p['id']] = st.session_state.cart.get(p['id'], 0) + 1
    with col_desno:
        st.subheader(T["cart_title"])
        ukupno, detalji = 0.0, ""
        for p in proizvodi:
            kol = st.session_state.cart.get(p["id"], 0)
            if kol > 0:
                st.write(f"✅ {p['name']} x {kol} = {kol * p['price']:.2f} €")
                ukupno += kol * p['price']; detalji += f"{p['name']} x {kol}\n"
        if ukupno > 0:
            st.markdown(f"### Ukupno: {ukupno:.2f} €"); st.caption(T["note_vaga"])
            with st.form("order_form"):
                ime = st.text_input(T["form_name"]); tel = st.text_input(T["form_tel"])
                adr = st.text_input(T["form_addr"]); grad = st.text_input(T["form_city"])
                ptt = st.text_input(T["form_zip"]); country = st.text_input(T["form_country"])
                if st.form_submit_button(T["btn_order"]):
                    if ime and tel and grad:
                        if posalji_email(ime, tel, grad, adr, detalji, ukupno, izabrani_jezik, country, ptt):
                            st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
        else: st.info(T["cart_empty"])

elif choice == T["nav_info"]:
    st.header(T["info_title"]); st.write(T["info_text"])
