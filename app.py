import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (TRAJNO ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (TRAJNO ZAKLJUČANO) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Vaša Košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "note_vaga": "⚖️ **Napomena o vaganju:** Cijene su fiksne, no točan iznos Vašeg računa znat ćemo nakon preciznog vaganja prije same isporuke.",
        "total": "Informativni iznos", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POTVRDI NARUDŽBU", "success": "Hvala Vam! Narudžba je zaprimljena!",
        "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "tax": "PDV uključen", "shipping_info": "PODACI ZA DOSTAVU",
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "horeca_text": "Kao obiteljski posao, duboko cijenimo rad naših kolega u ugostiteljstvu. Nudimo autentični miris dima (bukva i grab), sigurnu dostavu vlastitim hladnjačama i punu veleprodajnu podršku za stabilno poslovanje u 2026. godini.",
        "horeca_mail": "Za personaliziranu ponudu, pišite nam na:",
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "haccp_text": "U mesnici Kojundžić primjenjujemo najstrože standarde u 2026. Svaki komad mesa ima potpunu sljedivost, uz stroge HACCP protokole i EU certifikaciju u svim fazama prerade i dimljenja.",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": "Smješteni u srcu Siska, generacijama čuvamo vještinu tradicionalne pripreme mesa. Naša stoka dolazi isključivo od malih uzgajivača s pašnjaka Lonjskog polja, Banovine i Posavine. Meso pripremamo polako, uz prirodne začine, onako kako su to radili naši stari.",
        "footer": "© 2026 Mesnica Kojundžić Sisak | Kvaliteta kojoj vjerujete", "status_msg": "Slanje...", "err_msg": "Greška!",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 FOR CATERERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Your Cart", "cart_empty": "Your cart is empty.",
        "note_vaga": "⚖️ **Weight Note:** Prices are fixed, but the exact total will be known after precise weighing before delivery.",
        "total": "Informative Total", "form_name": "Full Name*", "form_tel": "Phone*",
        "form_city": "City*", "form_zip": "Zip*", "form_addr": "Street*",
        "form_country": "Country*", "btn_order": "🚀 CONFIRM ORDER", "success": "Thank you! Order received.",
        "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "tax": "VAT included", "shipping_info": "SHIPPING DETAILS",
        "horeca_title": "Partnership based on trust and tradition",
        "horeca_text": "As a family business, we value our catering partners. We offer traditional beech smoke aroma, safe refrigerated delivery, and full wholesale support in 2026.",
        "haccp_title": "Food Safety: Field to Table",
        "haccp_text": "Strict 2026 HACCP protocols and EU certification ensure full traceability and safety for every product in our shop.",
        "info_title": "Our Story: Family, Sisak, and Quality",
        "info_text": "Based in Sisak, we preserve traditional skills. Our livestock comes from local farms in Lonjsko Polje and Banovina, prepared with natural spices and no additives.",
        "footer": "© 2026 Butcher Kojundžić Sisak", "status_msg": "Sending...", "err_msg": "Error!",
        "p1": "Smoked bacon", "p2": "Smoked pork hock", "p3": "Smoked brisket tips", "p4": "Slavonian sausage", "p5": "Homemade salami", "p6": "Smoked bones",
        "p7": "Smoked pork feet mix", "p8": "Pancetta", "p9": "Smoked neck", "p10": "Smoked loin", "p11": "Smoked tenderloin", "p12": "Pork rinds",
        "p13": "Pork lard", "p14": "Blood sausage", "p15": "Grill sausages", "p16": "Dry ribs", "p17": "Smoked head", "p18": "Soap bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 FÜR GASTRONOMEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Warenkorb", "cart_empty": "Warenkorb ist leer.",
        "note_vaga": "⚖️ **Hinweis:** Der genaue Betrag wird nach dem Wiegen vor der Lieferung ermittelt.",
        "total": "Gesamtbetrag", "form_name": "Name*", "form_tel": "Telefon*",
        "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Straße*",
        "form_country": "Land*", "btn_order": "🚀 BESTELLUNG BESTÄTIGEN", "success": "Vielen Dank!",
        "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "tax": "Inkl. MwSt.", "shipping_info": "LIEFERDATEN",
        "horeca_title": "Partnerschaft und Tradition",
        "horeca_text": "Wir bieten Kaltrauchräucherung, eigene Kühlfahrzeuge und Großhandelskonditionen für unsere Gastronomiepartner im Jahr 2026.",
        "haccp_title": "Lebensmittelsicherheit 2026",
        "haccp_text": "Vollständige Rückverfolgbarkeit und strenge HACCP-Kontrollen garantieren höchste Qualität unserer Produkte.",
        "info_title": "Unsere Geschichte: Familie & Qualität",
        "info_text": "Seit Generationen in Sisak, verarbeiten wir Fleisch von regionalen Bauern ohne unnötige Zusatzstoffe nach traditioneller Art.",
        "footer": "© 2026 Metzgerei Kojundžić Sisak", "status_msg": "Senden...", "err_msg": "Fehler!",
        "p1": "Geräucherter Speck", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Hausgemachte Salami", "p6": "Knochen",
        "p7": "Schweinefüße", "p8": "Pancetta", "p9": "Schweinenacken", "p10": "Karree geräuchert", "p11": "Lende geräuchert", "p12": "Grieben",
        "p13": "Schweineschmalz", "p14": "Blutwurst", "p15": "Grillwürste", "p16": "Trockene Rippchen", "p17": "Kopf", "p18": "Seifenspeck"
    }
}

# --- 3. PODACI O PROIZVODIMA ---
# p2 i p3 su na komad (pc), ostali na kg.
PRODUCTS = [
    {"id": "p1", "price": 9.50, "unit": "kg"}, {"id": "p2", "price": 7.80, "unit": "pc"},
    {"id": "p3", "price": 6.50, "unit": "pc"}, {"id": "p4", "price": 14.20, "unit": "kg"},
    {"id": "p5", "price": 17.50, "unit": "kg"}, {"id": "p6", "price": 3.80, "unit": "kg"},
    {"id": "p7", "price": 4.50, "unit": "kg"}, {"id": "p8", "price": 16.90, "unit": "kg"},
    {"id": "p9", "price": 11.20, "unit": "kg"}, {"id": "p10", "price": 12.50, "unit": "kg"},
    {"id": "p11", "price": 15.00, "unit": "kg"}, {"id": "p12", "price": 19.50, "unit": "kg"},
    {"id": "p13", "price": 24.00, "unit": "pc"}, {"id": "p14", "price": 7.90, "unit": "kg"},
    {"id": "p15", "price": 9.20, "unit": "kg"}, {"id": "p16", "price": 8.90, "unit": "kg"},
    {"id": "p17", "price": 4.20, "unit": "kg"}, {"id": "p18", "price": 7.50, "unit": "kg"}
]

# --- 4. FUNKCIJA ZA EMAIL ---
def send_order_email(client_info, cart_items, lang_code):
    summary = "\n".join([f"- {item['name']}: {item['qty']} {item['unit']} ({item['sub']:.2f}€)" for item in cart_items])
    email_body = f"NOVA NARUDŽBA 2026\nKupac: {client_info['name']}\nTel: {client_info['tel']}\nAdresa: {client_info['addr']}, {client_info['zip']} {client_info['city']}\n\nStavke:\n{summary}\n\nUkupno: {client_info['total']:.2f} EUR"
    msg = MIMEText(email_body); msg['Subject'] = f"Narudžba: {client_info['name']}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls(); s.login(MOJ_EMAIL, MOJA_LOZINKA); s.send_message(msg)
        return True
    except: return False

# --- 5. STREAMLIT UI ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
if 'cart' not in st.session_state: st.session_state.cart = {}

with st.sidebar:
    lang = st.selectbox("Jezik / Language", list(LANG_MAP.keys()))
    T = LANG_MAP[lang]
    menu = st.radio("Navigacija", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])
    st.divider(); st.write(T["footer"])

if menu == T["nav_shop"]:
    st.title("🥩 " + T["title_sub"])
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(T["nav_shop"])
        subcols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with subcols[idx % 2]:
                with st.expander(f"**{T[p['id']]}**", expanded=True):
                    st.write(f"Cijena: {p['price']:.2f} {T['curr']} / {T[f'unit_{p['unit']}']}")
                    
                    # LOGIKA ZA KOLIČINU:
                    if p['unit'] == "pc":
                        # Komadni artikli: 0, 1, 2, 3...
                        q = st.number_input(f"{T[f'unit_{p['unit']}']}", min_value=0.0, step=1.0, key=f"in_{p['id']}")
                    else:
                        # KG artikli: Počinju od 0, prvi klik je 1, ostali +0.5
                        curr_val = st.session_state.cart.get(p['id'], 0.0)
                        q = st.number_input(f"{T[f'unit_{p['unit']}']}", min_value=0.0, step=0.5, key=f"in_{p['id']}")
                        # Ako je korisnik kliknuo strelicu gore sa 0.0 na 0.5, automatski prebaci na 1.0
                        if curr_val == 0.0 and q == 0.5:
                            q = 1.0
                            st.rerun() # Osvježi da prikaže 1.0

                    if q > 0: st.session_state.cart[p['id']] = q
                    elif p['id'] in st.session_state.cart: del st.session_state.cart[p['id']]

    with col2:
        st.subheader(T["cart_title"])
        if not st.session_state.cart: st.info(T["cart_empty"])
        else:
            total = 0; s_list = []
            for pid, q in st.session_state.cart.items():
                pd = next(x for x in PRODUCTS if x['id'] == pid)
                sub = q * pd['price']; total += sub
                st.write(f"**{T[pid]}**: {q} {T[f'unit_{pd['unit']}']} = {sub:.2f} €")
                s_list.append({'name': T[pid], 'qty': q, 'unit': T[f'unit_{pd['unit']}'], 'sub': sub})
            st.divider(); st.write(f"### {T['total']}: {total:.2f} €"); st.caption(T["note_vaga"])
            with st.form("f"):
                n = st.text_input(T["form_name"]); t_ = st.text_input(T["form_tel"]); a = st.text_input(T["form_addr"])
                c = st.text_input(T["form_city"]); z = st.text_input(T["form_zip"]); co = st.text_input(T["form_country"])
                if st.form_submit_button(T["btn_order"]):
                    if n and t_ and a:
                        if send_order_email({'name':n,'tel':t_,'addr':a,'city':c,'zip':z,'country':co,'total':total}, s_list, lang):
                            st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                    else: st.error("!!!")

elif menu == T["nav_horeca"]: st.header(T["horeca_title"]); st.write(T["horeca_text"]); st.info(f"{T['horeca_mail']} {MOJ_EMAIL}")
elif menu == T["nav_haccp"]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
elif menu == T["nav_info"]: st.header(T["info_title"]); st.write(T["info_text"])
