import streamlit as st
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import time

# --- 1. KONFIGURACIJA (FIKSNA I ZAKLJUČANA) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (POTPUNI, DETALJNI I PROŠIRENI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "OBITELJSKA MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna. Molimo odaberite proizvode iz naše ponude.",
        "note_vaga": """⚖️ **VAŽNA NAPOMENA O VAGANJU PROIZVODA:** Cijene svih naših proizvoda su fiksne i izražene po jedinici mjere (kilogramu ili komadu). Međutim, zbog prirode mesnih proizvoda, točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja same pošiljke. Naš tim se trudi maksimalno se pridržavati naručenih količina kako bi razlika između informativnog iznosa i konačnog računa bila što manja. Konačan iznos plaćate dostavljaču prilikom preuzimanja.""",
        "note_delivery": """🚚 **DOSTAVA I NAČIN PLAĆANJA:** Sve naručene proizvode pažljivo pakiramo u specijaliziranu termo-izoliranu ambalažu koja jamči očuvanje svježine i kontroliranu temperaturu tijekom transporta. Pakete šaljemo putem provjerene dostavne službe izravno na Vašu kućnu adresu. Plaćanje se vrši **isključivo pouzećem** (gotovinom dostavljaču), čime Vam jamčimo potpunu sigurnost transakcije.""",
        "horeca_title": "HoReCa Partnerstvo: Temelj vrhunske ugostiteljske ponude",
        "horeca_text": """Kao obiteljski vođen posao, duboko poštujemo trud i posvećenost naših kolega u ugostiteljskom sektoru. Razumijemo da svaki vrhunski tanjur u restoranu ili hotelu započinje s beskompromisnom kvalitetom sirovine. Naša ponuda za partnere u 2026. godini uključuje tradicionalno dimljenje na hladnom dimu bukve i graba, bez ikakvih tekućih pripravaka. Raspolažemo vlastitom flotom vozila s kontroliranim temperaturnim režimom. 
        \n📬 **Sve upite, dogovore i narudžbe za ugostitelje molimo šaljite izravno na našu službenu email adresu:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)""",
        "suppliers_title": "🚜 Naši dobavljači: Izvorna kvaliteta s domaćih pašnjaka",
        "suppliers_text": """Ponosni smo na dugogodišnju suradnju s lokalnim uzgajivačima. Svo meso koje prerađujemo u našem pogonu dolazi isključivo s domaćih pašnjaka i farmi s područja **Banovine, Posavine i Lonjskog polja**. Ovakva strategija kratkog lanca opskrbe jamči Vam vrhunsku svježinu, potpunu kontrolu podrijetla te podržava opstanak i razvoj našeg ruralnog kraja. Naše meso odlikuje se bogatim okusom koji se može postići samo prirodnim uzgojem.""",
        "haccp_title": "🛡️ Sigurnost hrane i HACCP: Standardi bez kompromisa",
        "haccp_text": """U Mesnici Kojundžić higijena nije samo zakonska obveza, već temelj našeg obiteljskog ugleda. U 2026. godini primjenjujemo najnovije tehnologije digitalnog nadzora kvalitete. Svaki komad mesa ima dokumentiran put – od markice životinje na farmi do finalnog pakiranja, što nazivamo potpunom sljedivost (Traceability). Naš objekt u Sisku nalazi se pod stalnim i strogim veterinarskim nadzorom kako bismo Vam osigurali zdravstveno ispravne proizvode najviše kategorije.""",
        "info_title": "ℹ️ O nama: Obiteljska tradicija i lokacija u Sisku",
        "info_text": """Smješteni u samom srcu Siska, obitelj Kojundžić već naraštajima čuva i usavršava vještinu tradicionalne pripreme mesa. Naše delicije pripremamo polako, koristeći isključivo domaću sol i prirodne začine, bez ikakvih kemijskih dodataka ili aditiva. Miris našeg dima je miris bukve i graba, onakav kakav pamtite iz djetinjstva.
        \n📍 **LOKACIJA PRODAJNOG MJESTA:** Grad Sisak, Gradska tržnica Kontroba. Posjetite nas na našem glavnom štandu svakim radnim danom i subotom.
        \n🕒 **RADNO VRIJEME:** Ponedjeljak - Subota: 07:00 - 13:00 sati.""",
        "form_name": "Ime i Prezime primatelja*", "form_tel": "Kontakt telefon za dostavu*", "form_country": "Država*", "form_city": "Grad ili mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI KONAČNU NARUDŽBU", "success": "VAŠA NARUDŽBA JE USPJEŠNO PREDANA! HVALA VAM NA POVJERENJU.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos narudžbe", "shipping_info": "📍 PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek (svinjska koljenica)", "p3": "Dimljeni svinjski prsni vršci", "p4": "Domaća slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti za juhu",
        "p7": "Dimljene svinjske nogice (mix)", "p8": "Domaća panceta (vrhunska)", "p9": "Dimljeni svinjski vrat (bez kosti)", "p10": "Dimljeni svinjski kare (bez kosti)", "p11": "Dimljena svinjska pečenica", "p12": "Domaći čvarci (tradicionalni)",
        "p13": "Domaća svinjska mast (kanta)", "p14": "Domaće krvavice", "p15": "Pečenice za roštilj", "p16": "Suha svinjska rebra (dimljena)", "p17": "Dimljena svinjska glava", "p18": "Slanina sapunara (bijela slanina)"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ FAMILY BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Shopping Cart", "cart_empty": "Your cart is currently empty. Please select products from our offer.",
        "note_vaga": """⚖️ **IMPORTANT WEIGHT NOTE:** Prices are fixed per unit. Due to the nature of meat products, the exact total will be determined after precise weighing just before packaging.""",
        "note_delivery": """🚚 **SHIPPING AND PAYMENT:** Products are packed in thermo-insulated packaging. Payment is **Cash on Delivery (COD)** only.""",
        "horeca_title": "HoReCa Partnership",
        "horeca_text": "We offer traditionally smoked meats for the hospitality sector. \n📬 **Inquiries:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Our Origin: Banovina, Posavina and Lonjsko Polje",
        "suppliers_text": "Our meat comes exclusively from domestic pastures and family farms in the ecologically preserved regions.",
        "haccp_title": "🛡️ Food Safety and HACCP Standards",
        "haccp_text": "Strict hygiene protocols and full digital traceability from the farm to your table.",
        "info_title": "ℹ️ About Us: Tradition and Location",
        "info_text": "📍 **LOCATION:** Sisak City Market (Kontroba). We use only natural salt, spices, and beech wood smoke.",
        "form_name": "Full Name*", "form_tel": "Phone Number*", "form_country": "Country*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street and Number*",
        "btn_order": "🚀 SUBMIT FINAL ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Order Total", "shipping_info": "📍 PODACI ZA DOSTAVU",
        "p1": "Smoked Hamburger Bacon", "p2": "Smoked Pork Hock", "p3": "Smoked Pork Brisket Tips", "p4": "Homemade Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Soup Bones",
        "p7": "Smoked Pork Trotters", "p8": "Premium Smoked Pancetta", "p9": "Smoked Pork Neck (Boneless)", "p10": "Smoked Pork Loin (Boneless)", "p11": "Smoked Pork Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Pork Lard (Bucket)", "p14": "Traditional Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Smoked Pork Ribs", "p17": "Smoked Pork Head", "p18": "White Fat Bacon (Sapunara)"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Ihr Warenkorb ist zurzeit leer.",
        "note_vaga": """⚖️ **WIEGEHINWEIS:** Die Preise sind pro Einheit fest. Der genaue Betrag wird erst nach dem Wiegen kurz vor dem Verpacken ermittelt.""",
        "note_delivery": """🚚 **LIEFERUNG UND ZAHLUNG:** Versand in Thermo-Verpackung. Die Zahlung erfolgt ausschließlich per **Nachnahme**.""",
        "horeca_title": "HoReCa-Partnerschaft",
        "horeca_text": "Premium-Rohstoffe für die Gastronomie. \n📬 **Anfragen per E-Mail:** [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
        "suppliers_title": "🚜 Herkunft: Banovina, Posavina und Lonjsko Polje",
        "suppliers_text": "Unser Fleisch stammt ausschließlich von heimischen Weiden lokaler Bauernhöfe.",
        "haccp_title": "🛡️ Lebensmittelsicherheit (HACCP)",
        "haccp_text": "Höchste Hygienestandards und vollständige Rückverfolgbarkeit vom Bauernhof bis zum Tisch.",
        "info_title": "ℹ️ Über uns: Tradition und Standort",
        "info_text": "📍 **STANDORT:** Stadtmarkt Sisak (Kontroba). Traditionelle Rezepte ohne künstliche Zusatzstoffe.",
        "form_name": "Vor- und Nachname*", "form_tel": "Telefonnummer*", "form_country": "Staat*", "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße und Hausnummer*",
        "btn_order": "🚀 BESTELLUNG ABSCHICKEN", "success": "BESTELLUNG ERFOLGREICH ÜBERMITTELT!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Informativ Rechnungsbetrag", "shipping_info": "📍 PODACI ZA DOSTAVU",
        "p1": "Geräucherter Hamburger-Speck", "p2": "Geräucherte Schweinshaxe", "p3": "Geräucherte Schweinebrustspitzen", "p4": "Slawonische Hauswurst", "p5": "Hausmacher Salami", "p6": "Geräucherte Suppenknochen",
        "p7": "Geräucherte Schweinefüße", "p8": "Premium Pancetta", "p9": "Geräucherter Schweinenacken (o.K.)", "p10": "Geräuchertes Karree (o.K.)", "p11": "Geräuchertes Lendenstück", "p12": "Hausmacher Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Hausmacher Blutwürste", "p15": "Grillwürste", "p16": "Geräucherte Schweinerippchen", "p17": "Geräucherter Schweinekopf", "p18": "Weißer Speck (Sapunara)"
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
st.set_page_config(page_title="Mesnica Kojundžić Sisak 2026", layout="wide")
lang_choice = st.sidebar.radio("Odaberite jezik / Select Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang_choice]

col_main, col_side = st.columns([0.65, 0.35])

# --- SREDINA: ARTIKLI I RUBRIKE ---
with col_main:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs: # TRGOVINA
        cols_shop = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with cols_shop[idx % 2]:
                st.subheader(T[p["id"]])
                st.write(f"Cijena: **{p['price']:.2f} {T['curr']}** / {T['unit_'+p['unit']]}")
                
                # LOGIKA ZA KILOGRAME (0.0 -> 1.0 -> 1.5)
                if p["unit"] == "kg":
                    val = st.number_input(f"Količina ({T['unit_kg']})", min_value=0.0, step=0.5, value=0.0, key=f"shop_{p['id']}")
                    if 0.1 <= val <= 0.5: val = 1.0
                else:
                    val = st.number_input(f"Količina ({T['unit_pc']})", min_value=0.0, step=1.0, value=0.0, key=f"shop_{p['id']}")
                
                if val > 0: st.session_state.cart[p["id"]] = val
                elif p["id"] in st.session_state.cart: del st.session_state.cart[p["id"]]

    with tabs: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs: st.header(T["info_title"]); st.write(T["info_text"])

# --- DESNA STRANA: KOŠARICA, IZNOS, NAPOMENE I DOSTAVA ---
with col_side:
    st.markdown(f"### {T['cart_title']}")
    total_val = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, qty in st.session_state.cart.items():
            p_inf = next(i for i in PRODUCTS if i["id"] == pid)
            sub = qty * p_inf["price"]
            total_val += sub
            st.write(f"✅ **{T[pid]}**")
            st.write(f"&nbsp;&nbsp;&nbsp;&nbsp; {qty} {T['unit_'+p_inf['unit']]} × {p_inf['price']:.2f} € = **{sub:.2f} €**")
        
        st.divider()

    # Informativni iznos i Napomene (Stalno vidljivo)
    st.metric(label=T["total"], value=f"{total_val:.2f} €")
    st.warning(T["note_vaga"])
    st.info(T["note_delivery"])
    
    # PODACI ZA DOSTAVU
    st.markdown(f"#### {T['shipping_info']}")
    with st.form("sidebar_delivery_form"):
        f_name = st.text_input(T["form_name"])
        f_tel = st.text_input(T["form_tel"])
        f_country = st.text_input(T["form_country"], value="Hrvatska")
        f_city = st.text_input(T["form_city"])
        f_zip = st.text_input(T["form_zip"])
        f_addr = st.text_input(T["form_addr"])
        
        if st.form_submit_button(T["btn_order"]):
            if f_name and f_tel and f_addr and st.session_state.cart:
                # E-mail tijelo
                mail_body = f"NOVA NARUDŽBA - MESNICA KOJUNDŽIĆ 2026\n\nKUPAC: {f_name}\nTEL: {f_tel}\nDRŽAVA: {f_country}\nADRESA: {f_addr}, {f_zip} {f_city}\n\nNARUČENO:\n"
                for pid, q in st.session_state.cart.items():
                    unit_type = next(i["unit"] for i in PRODUCTS if i["id"] == pid)
                    mail_body += f"- {T[pid]}: {q} {T['unit_'+unit_type]}\n"
                mail_body += f"\nUKUPNO: {total_val:.2f} EUR"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(mail_body); msg['Subject'] = f"Narudžba 2026 - {f_name}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.success(T["success"]); st.session_state.cart = {}; time.sleep(2); st.rerun()
                except: st.error("Slanje narudžbe trenutno nije moguće. Provjerite internet vezu.")
            elif not st.session_state.cart: st.error("Košarica je prazna!")
            else: st.error("Molimo ispunite sva obavezna polja označena zvjezdicom (*).")
