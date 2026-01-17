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

# --- VIŠEJEZIČNI RJEČNIK S PROŠIRENIM STRUČNIM TEKSTOVIMA ---
LANG = {
    "HR 🇭🇷": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA", "nav_lang": "🌍 JEZIK",
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
        "about_txt": "### Obiteljska tradicija i vizija\nObitelj Kojundžić generacijama predstavlja sinonim za vrhunsku mesnu struku u Sisačko-moslavačkoj županiji. Naš pristup temelji se na spoju povijesnih receptura sisačkog kraja i suvremenih tehnoloških procesa. Svaki komad mesa ručno obrađuju naši majstori mesari, osiguravajući da tekstura i kvaliteta zadovoljavaju najstrože gurmanske standarde. Naša pušnica koristi isključivo suho drvo bukve, čime postižemo onaj prepoznatljivi, blagi miris dima koji je postao naš zaštitni znak.",
        "horeca_txt": "### Partnerstvo za vrhunsku gastronomiju\nRazumijemo dinamiku modernog ugostiteljstva i potrebu za besprijekornom sirovinom. Za naše HORECA partnere (hotele, restorane i catering službe) nudimo sustav 'preciznog rezanja' i kalibracije proizvoda prema specifičnim normativima vaših jelovnika. Jamčimo kontinuitet kvalitete kroz cijelu godinu te stabilne lance opskrbe. Naša logistička mreža osigurava dostavu u kontroliranim temperaturnim uvjetima, poštujući vaše rokove i specifične zahtjeve skladištenja.",
        "suppliers_txt": "### Kratki lanci opskrbe i lokalni uzgoj\nSnaga naših proizvoda leži u porijeklu sirovine. Surađujemo isključivo s provjerenim OPG-ovima s područja Banovine i Posavine, promičući održivi razvoj lokalne zajednice. Naša goveda i svinje uzgajani su na tradicionalan način, uz prirodnu prehranu bez GMO dodataka. Ovakav pristup rezultira mesom bogatim intramuskularnom masnoćom, što je ključno za sočnost i bogatstvo okusa koje naši kupci cijene.",
        "haccp_txt": "### Beskompromisna sigurnost hrane\nU pogonima Kojundžić sigurnost potrošača je imperativ. Implementirani HACCP sustav (Hazard Analysis and Critical Control Points) nije samo zakonska obveza, već temelj našeg poslovanja. Provodimo rigorozne kontrole u svakoj fazi – od ulaza sirovine, preko termičke obrade i dimljenja, do finalnog pakiranja. Redovito uzorkovanje i suradnja s ovlaštenim laboratorijima osiguravaju da je svaki proizvod koji stigne do vašeg stola mikrobiološki čist i zdravstveno ispravan.",
        "products": ["Dimljeni hamburger", "Dimljeni buncek", "Dimljeni prsni vršci", "Slavonska kobasica", "Domaća salama", "Dimljene kosti", "Dimljene nogice mix", "Panceta", "Dimljeni vrat (BK)", "Dimljeni kare (BK)", "Dimljena pečenica", "Domaći čvarci", "Svinjska mast (kanta)", "Krvavice", "Pečenice za roštilj", "Suha rebra", "Dimljena glava", "Slanina sapunara"]
    },
    "EN 🇬🇧": {
        "title": "KOJUNDŽIĆ Butcher Shop & Processing | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US", "nav_lang": "🌍 LANGUAGE",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is currently empty.",
        "total": "Total informative amount", "unit_kg": "kg", "unit_pc": "pcs",
        "note_vaga": "⚖️ **IMPORTANT:** Prices are exact, but weight may vary slightly due to manual cutting.",
        "note_cod": "🚚 Cash on Delivery",
        "form_title": "📍 DELIVERY INFORMATION",
        "fname": "First Name*", "lname": "Last Name*", "tel": "Phone*", "city": "City*", "addr": "Street & Number*",
        "btn_order": "🚀 PLACE ORDER",
        "err_fields": "🛑 ORDER REJECTED: Please fill in all required fields (*).",
        "err_cart": "🛑 ORDER REJECTED: Your cart is empty!",
        "success_msg": "Your order has been received, thank you!",
        "about_txt": "### Family Tradition and Vision\nThe Kojundžić family has been synonymous with top-tier butchery in the Sisak region for generations. Our approach combines historical local recipes with modern technological processes. Each piece of meat is handcrafted by our master butchers, ensuring that texture and quality meet the highest gourmet standards. We use exclusively dry beech wood for smoking, achieving the distinctive, mild smoky aroma that is our signature.",
        "horeca_txt": "### Partnership for Superior Gastronomy\nWe understand the dynamics of modern hospitality and the need for flawless raw materials. For our HORECA partners, we offer 'precision cutting' and product calibration according to the specific standards of your menus. We guarantee quality consistency throughout the year and stable supply chains. Our logistics network ensures delivery under controlled temperature conditions.",
        "suppliers_txt": "### Short Supply Chains and Local Breeding\nThe strength of our products lies in the origin of the raw materials. We cooperate exclusively with verified local family farms from the Banovina and Posavina regions. Our livestock is raised in a traditional way, with a natural diet free of GMO additives. This results in meat rich in intramuscular fat, which is key to the juiciness our customers value.",
        "haccp_txt": "### Uncompromising Food Safety\nAt Kojundžić facilities, consumer safety is an imperative. Our implemented HACCP system is the foundation of our business. We conduct rigorous checks at every stage – from raw material entry to final packaging. Regular sampling and cooperation with certified laboratories ensure that every product reaching your table is microbiologically clean and healthy.",
        "products": ["Smoked Hamburger", "Smoked Pork Hock", "Smoked Brisket Tips", "Slavonian Sausage", "Homemade Salami", "Smoked Bones", "Smoked Trotters Mix", "Pancetta", "Smoked Neck (Boneless)", "Smoked Loin (Boneless)", "Smoked Pork Tenderloin", "Homemade Pork Rinds", "Lard (Bucket)", "Blood Sausages", "Grilling Sausages", "Dry Ribs", "Smoked Pig Head", "Soap Bacon"]
    },
    "DE 🇩🇪": {
        "title": "KOJUNDŽIĆ Metzgerei & Verarbeitung | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS", "nav_lang": "🌍 SPRACHE",
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
        "about_txt": "### Familientradition und Vision\nDie Familie Kojundžić steht seit Generationen für erstklassiges Fleischerhandwerk in der Region Sisak. Unser Ansatz verbindet historische lokale Rezepte mit modernen technologischen Prozessen. Jedes Stück Fleisch wird von unseren Metzgermeistern handgefertigt, um sicherzustellen, dass Textur und Qualität den höchsten Gourmet-Standards entsprechen.",
        "horeca_txt": "### Partnerschaft für erstklassige Gastronomie\nWir verstehen die Dynamik der modernen Hotellerie und den Bedarf an makellosen Rohstoffen. Für unsere HORECA-Partner bieten wir 'Präzisionsschnitt' und Produktkalibrierung nach den spezifischen Standards Ihrer Menüs an. Wir garantieren Qualitätskonstanz über das ganze Jahr und stabile Lieferketten.",
        "suppliers_txt": "### Kurze Lieferketten und lokale Zucht\nDie Stärke unserer Produkte liegt in der Herkunft der Rohstoffe. Wir arbeiten ausschließlich mit geprüften lokalen Familienbetrieben zusammen. Unser Vieh wird auf traditionelle Weise mit natürlicher Ernährung ohne GVO-Zusätze aufgezogen. Dies führt zu Fleisch, das reich an intramuskulärem Fett ist – der Schlüssel zur Saftigkeit.",
        "haccp_txt": "### Kompromisslose Lebensmittelsicherheit\nIn den Kojundžić-Betrieben hat die Verbrauchersicherheit oberste Priorität. Unser implementiertes HACCP-System ist das Fundament unseres Geschäfts. Wir führen in jeder Phase strenge Kontrollen durch. Regelmäßige Probenahmen und die Zusammenarbeit mit zertifizierten Labors stellen sicher, dass jedes Produkt mikrobiologisch einwandfrei ist.",
        "products": ["Geräucherter Hamburger", "Geräuchertes Eisbein", "Geräucherte Brustspitzen", "Slawonische Wurst", "Hausgemachte Salami", "Geräucherte Knochen", "Geräucherte Pfoten Mix", "Pancetta", "Geräucherter Nacken", "Geräuchertes Karree", "Geräuchertes Lendenstück", "Hausgemachte Grammeln", "Schweineschmalz", "Blutwurst", "Grillwürste", "Trockenrippen", "Geräucherter Schweinekopf", "Speck"]
    }
}

# --- INICIJALIZACIJA STANJA ---
if 'sel_lang_key' not in st.session_state: st.session_state.sel_lang_key = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
T = LANG[st.session_state.sel_lang_key]

# --- GLAVNI ELEMENTI ---
pop_placeholder = st.empty()
col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title"])
    # Navigacija
    t1, t2, t3, t4, t5, t6 = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"], T["nav_lang"]])
    
    with t1: # TRGOVINA
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        BASE_PRICES = [9.5, 7.8, 6.5, 14.2, 17.5, 3.8, 4.5, 16.9, 12.5, 13.5, 15.0, 18.0, 10.0, 9.0, 10.5, 8.5, 5.0, 9.0]
        UNITS = ["kg", "pc", "pc", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "pc", "kg", "kg", "kg", "pc", "kg"]
        for i in range(18):
            pid = f"p{i+1}"
            with (c1 if i % 2 == 0 else c2):
                st.subheader(T["products"][i])
                st.write(f"**{BASE_PRICES[i]:.2f} €** / {T['unit_'+UNITS[i]]}")
                cq = st.session_state.cart.get(pid, 0.0)
                nq = st.number_input(f"{T['products'][i]} ({T['unit_'+UNITS[i]]})", 0.0, step=(0.5 if UNITS[i]=="kg" else 1.0), value=float(cq), key=f"inp_{pid}")
                if nq != cq:
                    if nq > 0: st.session_state.cart[pid] = nq
                    else: st.session_state.cart.pop(pid, None)
                    st.rerun()

    with t2: st.markdown(T["horeca_txt"])
    with t3: st.markdown(T["suppliers_txt"])
    with t4: st.markdown(T["haccp_txt"])
    with t5: st.markdown(T["about_txt"])
    with t6: # JEZIK
        st.write("### Choose your language / Odaberite jezik / Sprache wählen")
        new_lang = st.radio("Selection:", list(LANG.keys()), index=list(LANG.keys()).index(st.session_state.sel_lang_key), label_visibility="collapsed")
        if new_lang != st.session_state.sel_lang_key:
            st.session_state.sel_lang_key = new_lang
            st.rerun()

with col_right:
    st.markdown(f"### {T['cart_title']}")
    suma = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, q in list(st.session_state.cart.items()):
            idx = int(pid[1:]) - 1
            sub = q * BASE_PRICES[idx]
            suma += sub
            st.write(f"✅ **{T['products'][idx]}**: {q} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{suma:.2f} €")
    st.warning(T["note_cod"])
    
    with st.form("main_form"):
        st.markdown(f"#### {T['form_title']}")
        fi = st.text_input(T["fname"]); fp = st.text_input(T["lname"]); ft = st.text_input(T["tel"])
        fg = st.text_input(T["city"]); fa = st.text_input(T["addr"])
        
        if st.form_submit_button(T["btn_order"], use_container_width=True):
            if not st.session_state.cart: st.error(T["err_cart"])
            elif not (fi and fp and ft and fg and fa): st.error(T["err_fields"])
            else:
                try:
                    detalji = "".join([f"- {T['products'][int(p[1:])-1]}: {q}\n" for p, q in st.session_state.cart.items()])
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(f"Kupac: {fi} {fp}\nTel: {ft}\nAdresa: {fa}, {fg}\n\nNarudžba:\n{detalji}\nUKUPNO: {suma:.2f} €")
                    msg['Subject'] = f"ORDER 2026: {fi} {fp}"; server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    
                    st.session_state.cart = {}
                    with pop_placeholder.container():
                        st.markdown(f"""<style>.ov {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20cm; height: 10cm; background: white; border: 8px solid #ff4b4b; border-radius: 25px; display: flex; justify-content: center; align-items: center; z-index: 999999; box-shadow: 0px 0px 60px rgba(0,0,0,0.6); }} .tx {{ color: #ff4b4b; font-size: 38px; font-weight: bold; text-align: center; padding: 30px; font-family: Arial; }}</style><div class="ov"><div class="tx">{T['success_msg']}</div></div>""", unsafe_allow_html=True)
                    time.sleep(4); pop_placeholder.empty(); st.rerun()
                except Exception as e: st.error(f"Error: {e}")
