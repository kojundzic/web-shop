import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# =================================================================
# 🛡️ TRAJNO ZAKLJUČANA KONFIGURACIJA - KOJUNDŽIĆ SISAK 2026.
# =================================================================

MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- VIŠEJEZIČNI RJEČNIK (USIDRENO: HR, EN, DE) ---
LANG = {
    "HR": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "total": "Ukupni informativni iznos", "unit_kg": "kg", "unit_pc": "kom",
        "note_vaga": "⚖️ **VAŽNO:** Cijene su točne, ali zbog ručne obrade težina može minimalno odstupati.",
        "note_cod": "🚚 Plaćanje pouzećem",
        "form_title": "📍 PODACI ZA DOSTAVU",
        "fname": "Ime*", "lname": "Prezime*", "tel": "Kontakt telefon*", "city": "Grad/Mjesto*", "addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU",
        "err_fields": "🛑 NARUDŽBA ODBIJENA: Molimo ispunite sva polja označena zvjezdicom (*).",
        "err_cart": "🛑 NARUDŽBA ODBIJENA: Vaša košarica ne smije biti prazna!",
        "success_msg": "Vaša narudžba je zaprimljena, hvala!",
        "about_txt": "Obitelj Kojundžić već generacijama njeguje tradiciju vrhunske prerade mesa u srcu Siska. Naša misija je jednostavna: očuvati izvorne recepte naših starih uz primjenu najmodernijih standarda higijene. Ponosni smo na naš suhi program koji se dimi isključivo na drvetu bukve i graba.",
        "horeca_txt": "Za hotele, restorane i kafiće nudimo posebne uvjete suradnje. Naš asortiman prilagođavamo potrebama vašeg jelovnika, uz zajamčenu svježinu i redovitu dostavu. Kontaktirajte nas za personalizirani cjenik za partnere.",
        "suppliers_txt": "Naša sirovina dolazi isključivo s pašnjaka Banovine i Posavine. Surađujemo s malim lokalnim OPG-ovima koji dijele našu strast prema prirodnom uzgoju. Vjerujemo u održivi razvoj i podršku domaćem selu.",
        "haccp_txt": "Sigurnost hrane nam je na prvom mjestu. Naši pogoni su u potpunosti usklađeni s HACCP sustavom upravljanja sigurnošću hrane. Redovite analize osiguravaju zdravstveno ispravan proizvod.",
        "products": [
            "Dimljeni hamburger", "Dimljeni buncek", "Dimljeni prsni vršci", "Slavonska kobasica",
            "Domaća salama", "Dimljene kosti", "Dimljene nogice mix", "Panceta",
            "Dimljeni vrat (BK)", "Dimljeni kare (BK)", "Dimljena pečenica", "Domaći čvarci",
            "Svinjska mast (kanta)", "Krvavice", "Pečenice za roštilj", "Suha rebra",
            "Dimljena glava", "Slanina sapunara"
        ]
    },
    "EN": {
        "title": "KOJUNDŽIĆ Butcher Shop & Processing | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is currently empty.",
        "total": "Total informative amount", "unit_kg": "kg", "unit_pc": "pcs",
        "note_vaga": "⚖️ **IMPORTANT:** Prices are exact, but weight may vary slightly due to manual cutting.",
        "note_cod": "🚚 Cash on Delivery",
        "form_title": "📍 DELIVERY INFORMATION",
        "fname": "First Name*", "lname": "Last Name*", "tel": "Phone*", "city": "City*", "addr": "Street & Number*",
        "btn_order": "🚀 PLACE ORDER",
        "err_fields": "🛑 ORDER REJECTED: Please fill in all fields marked with (*).",
        "err_cart": "🛑 ORDER REJECTED: Your cart cannot be empty!",
        "success_msg": "Your order has been received, thank you!",
        "about_txt": "The Kojundžić family has been nurturing the tradition of quality meat processing in Sisak for generations. Our mission is to preserve original recipes while applying the latest hygiene standards.",
        "horeca_txt": "We offer special terms for hotels, restaurants, and cafes. We adapt our assortment to your menu with guaranteed freshness. Contact us for a partner price list.",
        "suppliers_txt": "Our raw materials come exclusively from local pastures. We cooperate with small family farms that share our passion for natural breeding.",
        "haccp_txt": "Food safety is our priority. Our facilities are fully compliant with the HACCP system, ensuring safe and healthy products for our customers.",
        "products": [
            "Smoked Hamburger", "Smoked Pork Hock", "Smoked Brisket Tips", "Slavonian Sausage",
            "Homemade Salami", "Smoked Bones", "Smoked Trotters Mix", "Pancetta",
            "Smoked Neck (Boneless)", "Smoked Loin (Boneless)", "Smoked Pork Tenderloin", "Homemade Pork Rinds",
            "Lard (Bucket)", "Blood Sausages", "Grilling Sausages", "Dry Ribs",
            "Smoked Pig Head", "Soap Bacon"
        ]
    },
    "DE": {
        "title": "KOJUNDŽIĆ Metzgerei & Verarbeitung | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Ihr Warenkorb ist leer.",
        "total": "Gesamtbetrag", "unit_kg": "kg", "unit_pc": "stk",
        "note_vaga": "⚖️ **WICHTIG:** Preise sind korrekt, Gewicht kann variieren.",
        "note_cod": "🚚 Nachnahme",
        "form_title": "📍 LIEFERINFORMATIONEN",
        "fname": "Vorname*", "lname": "Nachname*", "tel": "Telefon*", "city": "Stadt*", "addr": "Straße & Hausnummer*",
        "btn_order": "🚀 BESTELLUNG ABSCHICKEN",
        "err_fields": "🛑 ABGELEHNT: Bitte alle Pflichtfelder (*) ausfüllen.",
        "err_cart": "🛑 ABGELEHNT: Ihr Warenkorb ist leer!",
        "success_msg": "Ihre Bestellung ist eingegangen, danke!",
        "about_txt": "Familie Kojundžić pflegt seit Generationen die Tradition der Fleischverarbeitung in Sisak. Wir bewahren Originalrezepte unter modernsten Hygienestandards.",
        "horeca_txt": "Besondere Konditionen für Hotels und Gastronomie. Wir liefern Frische direkt in Ihre Küche. Kontaktieren Sie uns für Partnerpreise.",
        "suppliers_txt": "Unsere Rohstoffe stammen von lokalen Weiden. Wir unterstützen die heimische Landwirtschaft und nachhaltige Zucht.",
        "haccp_txt": "Lebensmittelsicherheit nach HACCP-Standard. Regelmäßige Kontrollen garantieren gesunde und sichere Produkte.",
        "products": [
            "Geräucherter Hamburger", "Geräuchertes Eisbein", "Geräucherte Brustspitzen", "Slawonische Wurst",
            "Hausgemachte Salami", "Geräucherte Knochen", "Geräucherte Pfoten Mix", "Pancetta",
            "Geräucherter Nacken", "Geräuchertes Karree", "Geräuchertes Lendenstück", "Hausgemachte Grammeln",
            "Schweineschmalz", "Blutwurst", "Grillwürste", "Trockenrippen",
            "Geräucherter Schweinekopf", "Speck"
        ]
    }
}

# --- PRIPREMA ARTIKALA ---
BASE_PRODUCTS = [{"id": f"p{i+1}", "price": p, "unit": u} for i, (p, u) in enumerate([
    (9.50, "kg"), (7.80, "pc"), (6.50, "pc"), (14.20, "kg"), (17.50, "kg"), (3.80, "kg"),
    (4.50, "kg"), (16.90, "kg"), (12.50, "kg"), (13.50, "kg"), (15.00, "kg"), (18.00, "kg"),
    (10.00, "pc"), (9.00, "kg"), (10.50, "kg"), (8.50, "kg"), (5.00, "pc"), (9.00, "kg")
])]

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")

# Selektor jezika
sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE / SPRACHE", ["HR", "EN", "DE"])
T = LANG[sel_lang]

if 'cart' not in st.session_state: st.session_state.cart = {}
pop_placeholder = st.empty()
col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title"])
    t1, t2, t3, t4, t5 = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with t1: # SHOP
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        for i, bp in enumerate(BASE_PRODUCTS):
            p_name = T["products"][i]
            with (c1 if i % 2 == 0 else c2):
                st.subheader(p_name)
                st.write(f"**{bp['price']:.2f} €** / {T['unit_'+bp['unit']]}")
                cur_qty = st.session_state.cart.get(bp["id"], 0.0)
                step = 0.5 if bp["unit"] == "kg" else 1.0
                new_qty = st.number_input(f"{p_name}", 0.0, step=step, value=float(cur_qty), key=f"f_{bp['id']}")
                if new_qty != cur_qty:
                    if new_qty > 0: st.session_state.cart[bp["id"]] = new_qty
                    else: st.session_state.cart.pop(bp["id"], None)
                    st.rerun()

    with t2: st.write(T["horeca_txt"])
    with t3: st.write(T["suppliers_txt"])
    with t4: st.write(T["haccp_txt"])
    with t5: st.write(T["about_txt"])

with col_right:
    st.markdown(f"### {T['cart_title']}")
    ukupan_iznos = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, q in list(st.session_state.cart.items()):
            idx = int(pid[1:]) - 1
            sub = q * BASE_PRODUCTS[idx]["price"]
            ukupan_iznos += sub
            st.write(f"✅ **{T['products'][idx]}**: {q} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{ukupan_iznos:.2f} €")
    st.warning(T["note_cod"])
    
    with st.form("main_order_form"):
        st.markdown(f"#### {T['form_title']}")
        f_ime = st.text_input(T["fname"])
        f_prezime = st.text_input(T["lname"])
        f_tel = st.text_input(T["tel"])
        f_grad = st.text_input(T["city"])
        f_adresa = st.text_input(T["addr"])
        
        if st.form_submit_button(T["btn_order"], use_container_width=True):
            if not st.session_state.cart:
                st.error(T["err_cart"])
            elif not (f_ime and f_prezime and f_tel and f_grad and f_adresa):
                st.error(T["err_fields"])
            else:
                detalji = "".join([f"- {T['products'][int(pid[1:])-1]}: {q}\n" for pid, q in st.session_state.cart.items()])
                poruka = f"Kupac: {f_ime} {f_prezime}\nTel: {f_tel}\nAdresa: {f_adresa}, {f_grad}\nJezik: {sel_lang}\n\nNarudžba:\n{detalji}\nUKUPNO: {ukupan_iznos:.2f} €"
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(poruka)
                    msg['Subject'] = f"NARUDŽBA {sel_lang} 2026: {f_ime} {f_prezime}"
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    
                    st.session_state.cart = {}
                    with pop_placeholder.container():
                        st.markdown(f"""
                            <style>
                            .overlay {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20cm; height: 10cm; background: white; border: 8px solid #ff4b4b; border-radius: 25px; display: flex; justify-content: center; align-items: center; z-index: 999999; box-shadow: 0px 0px 60px rgba(0,0,0,0.6); }}
                            .tekst {{ color: #ff4b4b; font-size: 38px; font-weight: bold; text-align: center; padding: 30px; font-family: 'Arial Black', sans-serif; }}
                            </style>
                            <div class="overlay"><div class="tekst">{T['success_msg']}</div></div>
                        """, unsafe_allow_html=True)
                    time.sleep(4)
                    pop_placeholder.empty()
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")
