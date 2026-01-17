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
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Košarica je prazna. Dodajte domaće proizvode.",
        "note_vaga": """⚖️ **NAPOMENA O VAGANJU:** U našoj mesnici poštujemo prirodni rez. Cijene su fiksne po jedinici, ali konačan iznos računa formira se nakon preciznog vaganja neposredno prije pakiranja. Naš cilj je da odstupanje od naručene težine bude minimalno.""",
        "note_delivery": """🚚 **DOSTAVA I PLAĆANJE:** Pakete šaljemo u termo-izoliranoj ambalaži. Plaćanje je isključivo **pouzećem (gotovinom)** prilikom preuzimanja, što garantira sigurnost Vama i nama.""",
        "horeca_title": "HoReCa Partnerstvo: Vrhunska sirovina za Vaš restoran",
        "horeca_text": """U 2026. godini podižemo ljestvicu kvalitete. Vašim gostima nudimo meso koje je prošlo tradicionalni proces sušenja i dimljenja na hladnom dimu bukve. Nudimo stabilne cijene, prioritetnu dostavu vlastitim hladnjačama i personalizirane rezove mesa prema specifikacijama Vašeg chefa kuhinje.""",
        "suppliers_title": "🚜 Izravno s pašnjaka: Banovina, Posavina i Lonjsko polje",
        "suppliers_text": """Snaga našeg okusa leži u podrijetlu. Surađujemo isključivo s lokalnim OPG-ovima s područja **Banovine, Posavine i Lonjskog polja**. Naše životinje veći dio godine provode na otvorenom, hraneći se prirodno, što rezultira mesom koje je nutritivno bogato i prepoznatljive teksture.""",
        "haccp_title": "🛡️ Sigurnost hrane i digitalna sljedivost",
        "haccp_text": """Primjenjujemo najstrože HACCP protokole. U 2026. svakom kupcu jamčimo potpunu sljedivost: od markice životinje na pašnjaku do gotovog proizvoda u Vašoj vrećici. Naš pogon u Sisku pod stalnim je veterinarskim i laboratorijskim nadzorom.""",
        "info_title": "ℹ️ O nama: Obitelj Kojundžić",
        "info_text": """Tradicija duga desetljećima nastavlja se na tržnici u Sisku. Mi nismo industrija, mi smo obiteljska manufaktura koja vjeruje u sol, dim i strpljenje. Bez aditiva, bez kompromisa – samo čisto domaće meso pripremljeno onako kako su to radili naši stari.""",
        "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA USPJEŠNO PRIMLJENA! Hvala Vam.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "📍 PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is empty.",
        "note_vaga": """⚖️ **WEIGHT NOTE:** Final prices are determined after weighing during packaging. We aim for minimal deviation from your ordered quantity.""",
        "note_delivery": """🚚 **DELIVERY & PAYMENT:** Shipped in thermo-boxes. Payment is **Cash on Delivery (COD)** only.""",
        "horeca_title": "HoReCa Partnership",
        "horeca_text": "We provide premium beech-smoked meats for restaurants in 2026. Custom cuts and reliable cold-chain delivery guaranteed.",
        "suppliers_title": "🚜 Local Origins",
        "suppliers_text": "Our meat comes from the **Banovina, Posavina, and Lonjsko Polje** regions. Pasture-raised animals ensure superior quality.",
        "haccp_title": "🛡️ Food Safety",
        "haccp_text": "Strict HACCP standards and full digital traceability from farm to table.",
        "info_title": "ℹ️ Our Story",
        "info_text": "A family legacy at Sisak Market. Traditional recipes, natural spices, and authentic wood smoke.",
        "form_name": "Full Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Address*",
        "btn_order": "🚀 PLACE ORDER", "success": "ORDER RECEIVED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "📍 SHIPPING DETAILS",
        "p1": "Smoked Bacon", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters", "p8": "Premium Pancetta", "p9": "Smoked Neck", "p10": "Smoked Loin", "p11": "Smoked Tenderloin", "p12": "Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Pork Head", "p18": "White Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Ihr Warenkorb ist leer.",
        "note_vaga": """⚖️ **WIEGEHINWEIS:** Der Endpreis wird nach dem Wiegen ermittelt. Wir streben minimale Abweichungen an.""",
        "note_delivery": """🚚 **LIEFERUNG & ZAHLUNG:** Versand in Thermoboxen. Zahlung nur per **Nachnahme (Bar)**.""",
        "horeca_title": "HoReCa-Partner",
        "horeca_text": "Premium-Fleisch für die Gastronomie 2026. Traditionelle Räucherung und zuverlässige Kühlkettenlogistik.",
        "suppliers_title": "🚜 Herkunft",
        "suppliers_text": "Fleisch aus den Regionen **Banovina, Posavina und Lonjsko Polje**. Weidehaltung für besten Geschmack.",
        "haccp_title": "🛡️ Sicherheit",
        "haccp_text": "Strenge HACCP-Kontrollen und lückenlose Rückverfolgbarkeit in Sisak.",
        "info_title": "ℹ️ Über uns",
        "info_text": "Familientradition auf dem Markt von Sisak. Ohne Zusatzstoffe, nur Salz und echter Buchenrauch.",
        "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "🚀 BESTELLEN", "success": "BESTELLUNG ERHALTEN!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "📍 LIEFERDATEN",
        "p1": "Geräucherter Speck", "p2": "Geräucherte Stelze", "p3": "Geräucherte Spitzen", "p4": "Slawonische Wurst", "p5": "Hausmacher Salami", "p6": "Räucherknochen",
        "p7": "Schweinefüße", "p8": "Pancetta Premium", "p9": "Geräucherter Nacken", "p10": "Karree", "p11": "Lendenstück", "p12": "Grieben",
        "p13": "Schweineschmalz", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Trockenrippen", "p17": "Schweinekopf", "p18": "Speck weiß"
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

# --- 4. UI STRUKTURA ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
lang_choice = st.sidebar.radio("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

# Layout: Glavni dio (65%) | Sidebar desno (35%)
col_left, col_right = st.columns([0.65, 0.35])

# --- LIJEVA STRANA (Sadržaj rubrika) ---
with col_left:
    st.title(T["title_sub"])
    tab_shop, tab_horeca, tab_suppliers, tab_haccp, tab_info = st.tabs([
        T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]
    ])
    
    with tab_shop:
        cols_shop = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_shop[idx % 2]:
                st.subheader(T[p["id"]])
                st.write(f"**{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                step_v = 0.5 if p["unit"] == "kg" else 1.0
                q = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=step_v, key=f"shop_{p['id']}")
                if q > 0: st.session_state.cart[p["id"]] = q
                elif p["id"] in st.session_state.cart: del st.session_state.cart[p["id"]]

    with tab_horeca:
        st.header(T["horeca_title"])
        st.write(T["horeca_text"])
    with tab_suppliers:
        st.header(T["suppliers_title"])
        st.write(T["suppliers_text"])
    with tab_haccp:
        st.header(T["haccp_title"])
        st.write(T["haccp_text"])
    with tab_info:
        st.header(T["info_title"])
        st.write(T["info_text"])

# --- DESNA STRANA (Košarica, Dostava, Napomene - Stalno vidljivo) ---
with col_right:
    st.markdown(f"### {T['cart_title']}")
    
    if not st.session_state.cart:
        st.info(T["cart_empty"])
        total_price = 0.0
    else:
        total_price = 0.0
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_price += sub
            st.write(f"🔸 **{T[pid]}**: {qty} {T['unit_'+p_inf['unit']]} = {sub:.2f} €")
        
        st.divider()
        st.metric(label=T["total"], value=f"{total_price:.2f} €")

    # Podaci za dostavu (uvijek vidljivi)
    with st.expander(T["shipping_info"], expanded=True):
        with st.form("delivery_form"):
            f_name = st.text_input(T["form_name"])
            f_tel = st.text_input(T["form_tel"])
            f_city = st.text_input(T["form_city"])
            f_zip = st.text_input(T["form_zip"])
            f_addr = st.text_input(T["form_addr"])
            
            submit = st.form_submit_button(T["btn_order"])
            
            if submit:
                if f_name and f_tel and f_addr and st.session_state.cart:
                    # EMAIL LOGIKA
                    body = f"NARUDŽBA 2026:\nKupac: {f_name}\nTel: {f_tel}\nAdresa: {f_addr}, {f_zip} {f_city}\n\nArtikli:\n"
                    for pid, qty in st.session_state.cart.items():
                        body += f"- {T[pid]}: {qty}\n"
                    body += f"\nUkupno: {total_price:.2f} EUR"

                    try:
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                        server.login(MOJ_EMAIL, MOJA_LOZINKA)
                        msg = MIMEText(body); msg['Subject'] = f"Narudžba {f_name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                        st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
                elif not st.session_state.cart:
                    st.error("Košarica je prazna!")
                else:
                    st.error("Ispunite sva polja označena zvjezdicom (*).")

    # Napomene (uvijek vidljive na dnu desne strane)
    st.info(T["note_vaga"])
    st.warning(T["note_delivery"])
