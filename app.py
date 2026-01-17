import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (TRAJNO ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. PRIJEVODI I ARTIKLI (TRAJNO ZAKLJUČANO) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛍️ Vaša Košarica",
        "cart_empty": "Vaša košarica je prazna.", 
        "note_vaga": "⚖️ **Napomena:** Navedene cijene proizvoda su točne, dok je ukupni iznos u košarici informativan. Točan iznos bit će poznat nakon vaganja proizvoda.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom",
        "horeca_title": "Profesionalna usluga za restorane i hotele",
        "horeca_text": "Mesnica i prerada mesa Kojundžić nudi posebne pogodnosti:\n* **Uslužna proizvodnja:** Izrada po receptu.\n* **Veleprodajne cijene:** Za redovne isporuke.\n* **Dostava:** Vlastitim vozilima.",
        "horeca_mail": "Ostale informacije dostupne su putem e-mail adrese:",
        "haccp_title": "HACCP Standardi i Sigurnost",
        "haccp_text": "Naša proizvodnja u 2026. odvija se pod najstrožim sanitarnim uvjetima.",
        "info_title": "Obiteljska tradicija i kvaliteta",
        "info_text": "Smješteni u srcu Siska, ponosni smo na dugogodišnje iskustvo. Naša se stoka kupuje isključivo na farmama malih proizvođača iz okolice Siska (Park prirode Lonjsko polje, Banovina, Posavina). Meso se priprema na tradicionalan način u modernom pogonu te se dimi isključivo izabranim drvetom kako bismo osigurali vrhunsku aromu i kvalitetu.",
        "shipping_data": "Podaci za dostavu:",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", 
        "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti", 
        "p7": "Dimljene nogice mix", "p8": "Panceta", "p9": "Dimljeni vrat (BK)", 
        "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Čvarci"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 B2B SERVICE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING | 2026.", "cart_title": "🛍️ Your Cart",
        "cart_empty": "Your cart is empty.", 
        "note_vaga": "⚖️ **Note:** Final price confirmed after weighing.",
        "total": "Approx.", "form_name": "Full Name*", "form_tel": "Phone*",
        "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "form_country": "Country*", "btn_order": "🚀 CONFIRM ORDER", "success": "Thank you!",
        "unit_kg": "kg", "unit_pc": "pcs",
        "horeca_title": "B2B Service", "horeca_text": "Custom production and wholesale prices.",
        "horeca_mail": "Info via email:", "haccp_title": "HACCP", "haccp_text": "Strict safety standards 2026.",
        "info_title": "Tradition", "info_text": "Located in Sisak, traditional meat processing in modern facility.",
        "shipping_data": "Shipping info:",
        "p1": "Smoked bacon", "p2": "Smoked pork hock", "p3": "Smoked brisket tips",
        "p4": "Slavonian sausage", "p5": "Homemade salami", "p6": "Smoked bones",
        "p7": "Smoked pork feet", "p8": "Pancetta", "p9": "Smoked neck",
        "p10": "Smoked loin", "p11": "Smoked tenderloin", "p12": "Pork rinds"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 GASTRONOMIE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI & FLEISCHVERARBEITUNG | 2026.", "cart_title": "🛍️ Warenkorb",
        "cart_empty": "Ihr Warenkorb ist leer.", 
        "note_vaga": "⚖️ **Hinweis:** Endpreis nakon dem Wiegen.",
        "total": "Gesamt ca.", "form_name": "Name*", "form_tel": "Telefon*",
        "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "form_country": "Land*", "btn_order": "🚀 BESTELLUNG BESTÄTIGEN", "success": "Vielen Dank!",
        "unit_kg": "kg", "unit_pc": "Stk",
        "horeca_title": "Gastronomie", "horeca_text": "Lohnfertigung und Großhandelspreise.",
        "horeca_mail": "Infos per E-Mail:", "haccp_title": "HACCP", "haccp_text": "Produktion 2026.",
        "info_title": "Tradition", "info_text": "In Sisak ansässig, traditionelle Zubereitung.",
        "shipping_data": "Versanddetails:",
        "p1": "Geräucherter Hamburger", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen",
        "p4": "Slawonische Wurst", "p5": "Hausgemachte Salami", "p6": "Geräucherte Knochen",
        "p7": "Geräucherte Füße", "p8": "Pancetta", "p9": "Geräucherter Nacken",
        "p10": "Geräuchertes Karree", "p11": "Geräucherte Lende", "p12": "Grieben"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 3. FUNKCIJA ZA EMAIL (TRAJNO ZAKLJUČANO) ---
def posalji_email(ime, telefon, grad, adr, detalji, ukupno, jezik, country, ptt):
    predmet = f"🔴 NOVA NARUDŽBA 2026: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nZemlja: {country}\nLokacija: {ptt} {grad}\nAdresa: {adr}\nJezik: {jezik}\n\nArtikli:\n{detalji}\n\nUkupno: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 4. DIZAJN (SMANJENO ZA 30% - TRAJNO ZAKLJUČANO) ---
st.markdown("""<style>
    .brand-name { color: #8B0000; font-size: 35px; font-weight: 900; text-align: center; margin:0; }
    .brand-sub { color: #333; font-size: 14px; text-align: center; margin-bottom: 15px; }
    .product-card { background: white; border-radius: 8px; padding: 8px; border: 1px solid #eee; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 5px; }
    .product-card h4 { font-size: 13px; margin: 3px 0; }
    .product-card p { font-size: 12px; color: #8B0000; font-weight: bold; }
    .qty-display { font-size: 14px; font-weight: bold; color: #8B0000; text-align: center; }
    .stButton>button { height: 24px; line-height: 24px; padding: 0 6px; font-size: 10px; }
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 5. NAVIGACIJA (TRAJNO ZAKLJUČANO) ---
izabrani_jezik = st.sidebar.selectbox("Jezik / Language / Sprache", list(LANG_MAP.keys()), index=0)
T = LANG_MAP[izabrani_jezik]
choice = st.sidebar.radio("Meni", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

# --- 6. TRGOVINA ---
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)

    col_proizvodi, col_desno = st.columns([0.65, 0.35])

    with col_proizvodi:
        proizvodi = [
            {"id": 1, "name": T["p1"], "price": 12.0, "type": "kg"},
            {"id": 2, "name": T["p2"], "price": 8.0, "type": "pc"},
            {"id": 3, "name": T["p3"], "price": 9.0, "type": "pc"},
            {"id": 4, "name": T["p4"], "price": 16.0, "type": "kg"},
            {"id": 5, "name": T["p5"], "price": 25.0, "type": "kg"},
            {"id": 6, "name": T["p6"], "price": 2.5, "type": "kg"},
            {"id": 7, "name": T["p7"], "price": 2.5, "type": "kg"},
            {"id": 8, "name": T["p8"], "price": 17.0, "type": "kg"},
            {"id": 9, "name": T["p9"], "price": 15.0, "type": "kg"},
            {"id": 10, "name": T["p10"], "price": 15.0, "type": "kg"},
            {"id": 11, "name": T["p11"], "price": 20.0, "type": "kg"},
            {"id": 12, "name": T["p12"], "price": 10.0, "type": "pc"}
        ]
        
        cols = st.columns(3)
        for i, p in enumerate(proizvodi):
            sa_kolonom = cols[i % 3]
            with sa_kolonom:
                st.markdown(f'<div class="product-card"><h4>{p["name"]}</h4><p>{p["price"]:.2f} €</p></div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1,1,1])
                if c1.button("➖", key=f"m_{p['id']}"):
                    if st.session_state.cart.get(p['id'], 0) > 0:
                        st.session_state.cart[p['id']] -= 1
                        st.rerun()
                c2.markdown(f'<p class="qty-display">{st.session_state.cart.get(p["id"], 0)}</p>', unsafe_allow_html=True)
                if c3.button("➕", key=f"p_{p['id']}"):
                    st.session_state.cart[p['id']] = st.session_state.cart.get(p['id'], 0) + 1
                    st.rerun()

    with col_desno:
        st.subheader(T["cart_title"])
        ukupno_eur = 0.0
        detalji_narudzbe = ""
        for p in proizvodi:
            kol = st.session_state.cart.get(p['id'], 0)
            if kol > 0:
                iznos = kol * p['price']
                ukupno_eur += iznos
                st.write(f"🥩 {p['name']}: {kol} x {p['price']}€ = {iznos:.2f} €")
                detalji_narudzbe += f"- {p['name']}: {kol} ({iznos:.2f} €)\n"
        
        if ukupno_eur > 0:
            st.divider()
            st.markdown(f"### {T['total']}: **{ukupno_eur:.2f} €**")
            st.caption(T["note_vaga"])
            with st.form("narudzba"):
                ime = st.text_input(T["form_name"])
                tel = st.text_input(T["form_tel"])
                grad = st.text_input(T["form_city"])
                adr = st.text_input(T["form_addr"])
                ptt = st.text_input(T["form_zip"])
                drv = st.text_input(T["form_country"])
                if st.form_submit_button(T["btn_order"]):
                    if ime and tel and grad:
                        if posalji_email(ime, tel, grad, adr, detalji_narudzbe, ukupno_eur, izabrani_jezik, drv, ptt):
                            st.success(T["success"])
                            st.session_state.cart = {}
                            time.sleep(2)
                            st.rerun()
        else:
            st.info(T["cart_empty"])

elif choice == T["nav_horeca"]:
    st.header(T["horeca_title"])
    st.write(T["horeca_text"])
    st.info(f"{T['horeca_mail']} **{MOJ_EMAIL}**")
elif choice == T["nav_haccp"]:
    st.header(T["haccp_title"])
    st.write(T["haccp_text"])
elif choice == T["nav_info"]:
    st.header(T["info_title"])
    st.write(T["info_text"])
