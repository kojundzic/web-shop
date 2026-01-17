import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (TRAJNO ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (185 STAVKI - TRAJNO ZAKLJUČANO) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Vaša Košarica", "cart_empty": "Vaša košarica je prazna.",
        "note_vaga": "⚖️ **Napomena:** Cijene su točne, ali konačan iznos ovisi o vaganju proizvoda.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "tax": "PDV uključen", "shipping_info": "PODACI ZA DOSTAVU",
        "horeca_title": "B2B i Ugostiteljstvo", 
        "horeca_text": "Nudimo uslužnu proizvodnju po vašem receptu, veleprodajne cijene i vlastitu dostavu hladnjačom.",
        "haccp_title": "Sigurnost hrane (HACCP)", 
        "haccp_text": "Naša proizvodnja u 2026. udovoljava svim EU standardima i sanitarnim normama.",
        "info_title": "Obiteljska Tradicija Kojundžić",
        "info_text": "Meso nabavljamo isključivo od malih proizvođača iz Parka prirode Lonjsko polje i Banovina.",
        "footer": "© 2026 Mesnica Kojundžić Sisak | Sva prava pridržana",
        "status_msg": "Slanje narudžbe...", "err_msg": "Sustav trenutno nedostupan!",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci",
        "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)",
        "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj",
        "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 B2B SERVICE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Your Cart", "cart_empty": "Your cart is empty.",
        "note_vaga": "⚖️ **Note:** Final price confirmed after weighing products.",
        "total": "Approximate", "form_name": "Full Name*", "form_tel": "Phone Number*",
        "form_city": "City*", "form_zip": "Postal Code*", "form_addr": "Street and Number*",
        "form_country": "Country*", "btn_order": "🚀 CONFIRM ORDER", "success": "Received! Thank you.",
        "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "tax": "VAT included", "shipping_info": "SHIPPING DETAILS",
        "horeca_title": "B2B & Gastronomy", 
        "horeca_text": "We offer custom production, wholesale prices, and refrigerated delivery.",
        "haccp_title": "Food Safety (HACCP)", 
        "haccp_text": "Our production meets all EU standards and sanitary norms in 2026.",
        "info_title": "Kojundžić Tradition",
        "info_text": "Meat from small producers in Lonjsko Polje and Banovina region.",
        "footer": "© 2026 Butcher Kojundžić Sisak | All rights reserved",
        "status_msg": "Sending order...", "err_msg": "System error!",
        "p1": "Smoked bacon", "p2": "Smoked pork hock", "p3": "Smoked brisket tips",
        "p4": "Slavonian sausage", "p5": "Homemade salami", "p6": "Smoked bones",
        "p7": "Smoked pork feet", "p8": "Pancetta (Premium)", "p9": "Smoked neck (Boneless)",
        "p10": "Smoked loin (Boneless)", "p11": "Smoked tenderloin", "p12": "Homemade pork rinds",
        "p13": "Pork lard (bucket)", "p14": "Blood sausage", "p15": "Grill sausages",
        "p16": "Dry ribs", "p17": "Smoked head", "p18": "Soap bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 B2B SERVICE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Warenkorb", "cart_empty": "Ihr Warenkorb ist leer.",
        "note_vaga": "⚖️ **Hinweis:** Endpreis nach dem Wiegen der Produkte.",
        "total": "Gesamt ca.", "form_name": "Name und Nachname*", "form_tel": "Telefonnummer*",
        "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße und Hausnummer*",
        "form_country": "Land*", "btn_order": "🚀 BESTELLUNG BESTÄTIGEN", "success": "Vielen Dank!",
        "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "tax": "MwSt. inkl.", "shipping_info": "LIEFERDATEN",
        "horeca_title": "B2B & Gastronomie", 
        "horeca_text": "Wir bieten Lohnfertigung, Großhandelspreise und eigene Kühllieferung.",
        "haccp_title": "Lebensmittelsicherheit", 
        "haccp_text": "Unsere Produktion entspricht allen EU-Standards und Sanitärnormen 2026.",
        "info_title": "Kojundžić Tradition",
        "info_text": "Fleisch von Erzeugern aus Lonjsko Polje und Banovina Gebiet.",
        "footer": "© 2026 Metzgerei Kojundžić Sisak | Alle Rechte vorbehalten",
        "status_msg": "Bestellung wird gesendet...", "err_msg": "Systemfehler!",
        "p1": "Geräucherter Hamburger", "p2": "Geräucherte Stelze", "p3": "Brustspitzen geräuchert",
        "p4": "Slawonische Wurst", "p5": "Hausgemachte Salami", "p6": "Geräucherte Knochen",
        "p7": "Schweinefüße Mix", "p8": "Pancetta (Premium)", "p9": "Schweinenacken (o.K.)",
        "p10": "Karree geräuchert (o.K.)", "p11": "Lende geräuchert", "p12": "Hausgemachte Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwurst", "p15": "Grillwürste",
        "p16": "Trockene Rippchen", "p17": "Geräucherter Kopf", "p18": "Seifenspeck"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 3. LOGIKA ZA EMAIL ---
def posalji_email(ime, telefon, grad, adr, detalji, ukupno, jezik, country, ptt):
    predmet = f"🔴 NOVA NARUDŽBA 2026: {ime}"
    tijelo = f"KUPAC: {ime}\nTEL: {telefon}\nADRESA: {adr}, {ptt} {grad}, {country}\nJEZIK: {jezik}\n\nSTAVKE:\n{detalji}\nUKUPNO: {ukupno:.2f} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 4. DIZAJN ---
st.markdown("""<style>
    .brand-name { color: #8B0000; font-size: 38px; font-weight: 900; text-align: center; margin:0; }
    .product-card { background: white; border-radius: 10px; padding: 12px; border: 1px solid #eee; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .footer { text-align: center; color: #888; font-size: 12px; margin-top: 50px; }
    .qty-display { font-size: 18px; font-weight: bold; color: #8B0000; text-align: center; }
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state: st.session_state.cart = {}

izabrani_jezik = st.sidebar.selectbox("Language / Jezik", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
choice = st.sidebar.radio("Meni", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ 2026</p>', unsafe_allow_html=True)
    c_p, c_k = st.columns([0.65, 0.35])
    
    proizvodi = [{"id": i, "name": T[f"p{i}"], "price": 10.0 + i} for i in range(1, 19)]

    with c_p:
        for i in range(0, len(proizvodi), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(proizvodi):
                    p = proizvodi[i + j]
                    with cols[j]:
                        st.markdown(f'<div class="product-card"><b>{p["name"]}</b><br>{p["price"]:.2f} {T["curr"]}</div>', unsafe_allow_html=True)
                        c1, c2, c3 = st.columns()
                        if c1.button("➖", key=f"m{p['id']}"):
                            if st.session_state.cart.get(p['id'], 0) > 0:
                                st.session_state.cart[p['id']] -= 1
                                st.rerun()
                        c2.markdown(f'<p class="qty-display">{st.session_state.cart.get(p["id"], 0)}</p>', unsafe_allow_html=True)
                        if c3.button("➕", key=f"p{p['id']}"):
                            st.session_state.cart[p['id']] = st.session_state.cart.get(p['id'], 0) + 1
                            st.rerun()

    with c_k:
        st.subheader(T["cart_title"])
        ukupno, detalji = 0.0, ""
        for p in proizvodi:
            k = st.session_state.cart.get(p["id"], 0)
            if k > 0:
                ukupno += k * p['price']; detalji += f"- {p['name']} x {k}\n"
                st.write(f"🥩 {p['name']} x {k} = {k*p['price']:.2f} {T['curr']}")
        if ukupno > 0:
            st.divider()
            st.markdown(f"### {T['total']}: {ukupno:.2f} {T['curr']}"); st.info(T["note_vaga"])
            st.markdown(f"**{T['shipping_info']}**")
            with st.form("nar_form"):
                i = st.text_input(T["form_name"]); t = st.text_input(T["form_tel"])
                g = st.text_input(T["form_city"]); a = st.text_input(T["form_addr"])
                pc = st.text_input(T["form_zip"]); dr = st.text_input(T["form_country"])
                if st.form_submit_button(T["btn_order"]):
                    if i and t and g and a:
                        st.write(T["status_msg"])
                        if posalji_email(i, t, g, a, detalji, ukupno, izabrani_jezik, dr, pc):
                            st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                        else: st.error(T["err_msg"])
                    else: st.warning("Popunite polja!")
        else: st.info(T["cart_empty"])

elif choice == T["nav_info"]:
    st.header(T["info_title"]); st.write(T["info_text"])
elif choice == T["nav_horeca"]:
    st.header(T["horeca_title"]); st.write(T["horeca_text"])
elif choice == T["nav_haccp"]:
    st.header(T["haccp_title"]); st.write(T["haccp_text"])

st.markdown(f'<p class="footer">{T["footer"]}</p>', unsafe_allow_html=True)
