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
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je trenutno prazna. Odaberite domaće delicije iz ponude.",
        "note_vaga": """⚖️ **Važna napomena o vaganju:** U našoj mesnici poštujemo prirodni oblik svakog komada mesa. Cijene po jedinici su fiksne, ali točnu težinu i finalni iznos računa odredit ćemo preciznim vaganjem tijekom pakiranja. Naš cilj je maksimalno se približiti naručenoj količini.""",
        "note_delivery": """🚚 **Dostava i sigurno plaćanje:** Vašu narudžbu pažljivo pakiramo u termo-izolacijske kutije i šaljemo provjerenom dostavnom službom. Plaćanje se vrši **pouzećem (gotovinom)**, što Vam pruža maksimalnu sigurnost.""",
        "horeca_title": "HoReCa: Partnerstvo s okusom tradicije",
        "horeca_text": """Kao obiteljska manufaktura, razumijemo da vrhunski restorani zahtijevaju meso besprijekorne kvalitete i postojanog okusa. U 2026. nudimo personaliziranu uslugu rezanja, odležavanja i tradicionalnog dimljenja isključivo na drvu bukve. Osiguravamo hladni lanac dostave vlastitim vozilima do Vaših vrata u najkraćem roku.""",
        "suppliers_title": "🚜 Izravno s pašnjaka Banovine i Posavine",
        "suppliers_text": """Vjerujemo u kratki put od polja do stola. Naše sirovine potječu od malih, provjerenih uzgajivača s ekološki očuvanih područja **Banovine, Posavine i Lonjskog polja**. Životinje borave na otvorenim pašnjacima, što rezultira mesom vrhunske teksture i bogatog, prirodnog okusa kakav se danas rijetko nalazi.""",
        "haccp_title": "🛡️ Sigurnost bez kompromisa",
        "haccp_text": """Zdravlje naših kupaca je prioritet. Naš pogon u Sisku u 2026. godini koristi najsuvremenije standarde higijene uz strogi HACCP nadzor. Svaki komad mesa ima digitalni zapis o sljedivosti – točno znamo s koje je farme stigao u Vašu kuhinju.""",
        "info_title": "ℹ️ Obiteljska ostavština Kojundžić",
        "info_text": """Nalazimo se u srcu Siska, na gradskoj tržnici, gdje generacijama spajamo stare recepture i moderne standarde. Naše meso ne sadrži nepotrebne aditive ni umjetne boje – koristimo samo sol, prirodne začine i dim domaćeg drveta. Posjetite nas i osjetite miris prave tradicije.""",
        "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*", "form_city": "Grad i mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 ZAKLJUČI NARUDŽBU", "success": "NARUDŽBA POSLANA! Javit ćemo Vam se uskoro.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos (cca)", "shipping_info": "PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "The cart is empty. Choose some authentic delicacies.",
        "note_vaga": """⚖️ **Weight Note:** We respect the natural cut of each piece. Unit prices are fixed, but the final amount is determined by precise weighing during packaging. We aim for the closest match to your requested amount.""",
        "note_delivery": """🚚 **Delivery & Secure Payment:** Orders are shipped in thermo-insulated boxes. Payment is **Cash on Delivery (COD)**, ensuring a safe transaction for you.""",
        "horeca_title": "HoReCa: A Partnership in Quality",
        "horeca_text": "In 2026, we provide professional chefs with custom cuts and beech-smoked meats. We guarantee a strict cold chain delivery directly to your venue.",
        "suppliers_title": "🚜 Local Heritage",
        "suppliers_text": "All our meat is sourced from family farms in the **Banovina, Posavina, and Lonjsko Polje** regions. Animals graze on natural pastures, ensuring premium texture and rich flavor.",
        "haccp_title": "🛡️ Food Safety First",
        "haccp_text": "Our Sisak facility operates under strict 2026 HACCP protocols with full digital traceability for every product.",
        "info_title": "ℹ️ The Kojundžić Legacy",
        "info_text": "Located at the Sisak City Market, we combine heritage recipes with modern standards. No artificial additives—just salt, natural spices, and wood smoke.",
        "form_name": "Full Name*", "form_tel": "Phone Number*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & Number*",
        "btn_order": "🚀 SUBMIT ORDER", "success": "ORDER SUBMITTED! We will contact you soon.", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "SHIPPING DETAILS",
        "p1": "Smoked Bacon", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters Mix", "p8": "Premium Pancetta", "p9": "Smoked Neck (Boneless)", "p10": "Smoked Pork Loin", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Pork Head", "p18": "White Fat Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Der Warenkorb ist leer. Wählen Sie hausgemachte Köstlichkeiten.",
        "note_vaga": """⚖️ **Hinweis zum Wiegen:** Wir respektieren die natürliche Form jedes Stücks. Die Preise sind fest, aber der endgültige Betrag wird durch genaues Wiegen beim Verpacken ermittelt.""",
        "note_delivery": """🚚 **Lieferung & Zahlung:** Wir versenden in Thermoboxen. Die Zahlung erfolgt per **Nachnahme**, was Ihnen maximale Sicherheit bietet.""",
        "horeca_title": "HoReCa: Qualitätspartnerschaft",
        "horeca_text": "Wir bieten der Gastronomie im Jahr 2026 maßgeschneiderte Schnitte und Buchenholz-Räucherwaren mit garantierter Kühlkettenlieferung.",
        "suppliers_title": "🚜 Regionale Herkunft",
        "suppliers_text": "Unser Fleisch stammt ausschließlich von Bauernhöfen aus den Regionen **Banovina, Posavina und Lonjsko Polje**. Weidehaltung garantiert besten Geschmack.",
        "haccp_title": "🛡️ Sicherheit & HACCP",
        "haccp_text": "Unser Betrieb in Sisak erfüllt modernste HACCP-Standards mit vollständiger Rückverfolgbarkeit für jedes Produkt.",
        "info_title": "ℹ️ Familie Kojundžić",
        "info_text": "Auf dem Stadtmarkt von Sisak pflegen wir traditionelle Rezepte ohne künstliche Zusatzstoffe—nur Salz, Gewürze und Rauch.",
        "form_name": "Name*", "form_tel": "Telefonnummer*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Straße & Hausnummer*",
        "btn_order": "🚀 BESTELLEN", "success": "BESTELLUNG ABSCHICKT! Wir melden uns in Kürze.", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme (ca.)", "shipping_info": "LIEFERDATEN",
        "p1": "Geräucherter Speck", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Geräucherte Füße Mix", "p8": "Premium Pancetta", "p9": "Geräucherter Nacken", "p10": "Geräuchertes Karree", "p11": "Geräuchertes Lendenstück", "p12": "Hausmacher Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Geräucherter Kopf", "p18": "Speck (weiß)"
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

# --- 4. UI SETUP ---
st.set_page_config(page_title="Mesnica Kojundžić 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

# Glavna podjela: Sredina (70%) i Desna strana (30%)
col_main, col_sidebar = st.columns([0.7, 0.3])

# --- LIJEVA STRANA: ARTIKLI I RUBRIKE ---
with col_main:
    st.header(T["title_sub"])
    
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # SHOP
        st.markdown(f"### {T['nav_shop']}")
        cols_art = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_art[idx % 2]:
                st.subheader(T[p["id"]])
                st.write(f"Cijena: **{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                step_v = 0.5 if p["unit"] == "kg" else 1.0
                qty = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=step_v, key=f"q_{p['id']}")
                if qty > 0:
                    st.session_state.cart[p["id"]] = qty
                elif p["id"] in st.session_state.cart:
                    del st.session_state.cart[p["id"]]

    with tabs[1]: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs[2]: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs[3]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs[4]: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA: KOŠARICA, INFO I PODACI (STALNO VIDLJIVO) ---
with col_sidebar:
    st.markdown(f"## {T['cart_title']}")
    
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        total_v = 0.0
        for pid, q in st.session_state.cart.items():
            p_data = next(i for i in PRODUCTS if i["id"] == pid)
            sub = q * p_data["price"]
            total_v += sub
            st.write(f"**{T[pid]}**")
            st.write(f"{q} {T['unit_'+p_data['unit']]} x {p_data['price']} = {sub:.2f} €")
        
        st.divider()
        st.metric(label=T["total"], value=f"{total_v:.2f} €")
        
        # Formular s desne strane
        with st.form("sidebar_order_form"):
            st.write(T["shipping_info"])
            f_name = st.text_input(T["form_name"])
            f_tel = st.text_input(T["form_tel"])
            f_city = st.text_input(T["form_city"])
            f_zip = st.text_input(T["form_zip"])
            f_addr = st.text_input(T["form_addr"])
            
            if st.form_submit_button(T["btn_order"]):
                if f_name and f_tel and f_addr:
                    content = f"NARUDŽBA 2026\n\nKupac: {f_name}\nTel: {f_tel}\nAdresa: {f_addr}, {f_zip} {f_city}\n\nStavke:\n"
                    for pid, q in st.session_state.cart.items():
                        content += f"- {T[pid]}: {q}\n"
                    content += f"\nUkupno cca: {total_v:.2f} EUR"

                    try:
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                        server.login(MOJ_EMAIL, MOJA_LOZINKA)
                        msg = MIMEText(content); msg['Subject'] = f"Narudžba - {f_name}"
                        msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                        st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                    except Exception as e: st.error(f"Greška: {e}")
                else:
                    st.error("Ispunite obavezna polja!")

    st.divider()
    st.caption(T["note_vaga"])
    st.caption(T["note_delivery"])
