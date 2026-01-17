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

# --- 2. MASTER PRIJEVODI (KORIGIRANI I PROŠIRENI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. Trudimo se da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "note_delivery": """🚚 **Dostava i plaćanje:** Naručene artikle šaljemo putem provjerene dostavne službe na kućnu adresu ili u najbliži paketomat, ovisno o Vašem izboru pri preusmjeravanju. Plaćanje se vrši **isključivo pouzećem** (gotovinom dostavljaču), čime jamčimo sigurnost transakcije.""",
        "suppliers_title": "Naši partneri: Snaga lokalnog uzgoja",
        "suppliers_text": """Kvaliteta mesa u Mesnici Kojundžić izravan je rezultat suradnje s malim obiteljskim gospodarstmima iz našeg neposrednog okruženja. Vjerujemo u kratke lance opskrbe i podršku lokalnoj zajednici.
\n**Područja s kojih nabavljamo sirovinu u 2026. godini:**
* **Banovina i Posavina:** Naši glavni izvori vrhunske svinjetine i junetine. Životinje se uzgajaju na tradicionalan način, uz prirodnu ishranu, što rezultira savršenom teksturom mesa.
* **Lonjsko polje:** Posebno smo ponosni na suradnju s uzgajivačima čija stoka boravi na slobodnoj ispaši u netaknutoj prirodi parka prirode.
* **Okolica Siska:** Svakodnevna suradnja s lokalnim farmerima osigurava da meso s polja do naše mesnice stigne u najkraćem mogućem roku, jamčeći maksimalnu svježinu.""",
        "horeca_title": "HoReCa Partnerstvo: Temelj vrhunskog ugostiteljstva",
        "horeca_text": """Kao obiteljski vođen posao, duboko poštujemo trud kolega u ugostiteljskom sektoru. Razumijemo da svaki vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom kvalitetom sirovine.
\n**Naša ponuda za partnere u 2026. godini uključuje:**
* **Tradicija dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba.
* **Logistička izvrsnost:** Vlastita flota vozila s kontroliranim temperaturnim režimom (hladnjače).
* **Veleprodajni standard:** Prioritetna obrada i personalizirani rezovi mesa.""",
        "haccp_title": "Sigurnost hrane i HACCP: Beskompromisni standardi",
        "haccp_text": """U Mesnici Kojundžić, higijena je temelj našeg obiteljskog ugleda. U 2026. godini primjenjujemo najnovije tehnologije nadzora kvalitete.
* **Potpuna sljedivost (Traceability):** Svaki komad mesa ima dokumentiran put – točno znamo s koje farme dolazi.
* **Moderni pogon:** Naš objekt u Sisku pod stalnim je veterinarskim nadzorom uz stroge HACCP protokole.""",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima. Meso pripremamo polako, uz korištenje isključivo domaćih začina, bez aditiva.\n📍 **Glavno prodajno mjesto:** Tržnica Sisak.\n🕒 **Radno vrijeme:** Pon-Sub: 07:00 - 13:00""",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljeni nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA! HVALA VAM NA POVJERENJU.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_suppliers": "🚜 SUPPLIERS", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "is empty",
        "note_vaga": """⚖️ **Weight Note:** Product prices are fixed, but the exact total of your invoice will be confirmed after precise weighing just before packaging. You will know the final amount when the package arrives and you pay Cash on Delivery. We strive to adhere to ordered quantities and ensure the difference between the estimated and final amount is as small as possible.""",
        "note_delivery": """🚚 **Delivery and Payment:** Ordered items are shipped via a verified delivery service to your home address or nearest parcel locker, depending on your choice during redirection. Payment is made **exclusively Cash on Delivery** (cash to the courier), guaranteeing transaction security.""",
        "suppliers_title": "Our Partners: The Strength of Local Farming",
        "suppliers_text": """The meat quality at Kojundžić Butchery is a direct result of cooperation with small family farms in our immediate surroundings. We believe in short supply chains and supporting the local community.
\n**Regions from which we source raw materials in 2026:**
* **Banovina and Posavina:** Our main sources of premium pork and beef. Animals are raised in a traditional way, with a natural diet, resulting in perfect meat texture.
* **Lonjsko Polje:** We are particularly proud of our cooperation with breeders whose livestock grazes freely in the untouched nature of the nature park.
* **Sisak Surroundings:** Daily cooperation with local farmers ensures that meat arrives from the field to our butchery in the shortest possible time, guaranteeing maximum freshness.""",
        "horeca_title": "HoReCa Partnership: The Foundation of Premium Hospitality",
        "horeca_text": """As a family-run business, we deeply respect the efforts of our colleagues in the hospitality sector. We understand that every premium dish in a restaurant or hotel begins with uncompromising quality of raw materials.
\n**Our offer for partners in 2026 includes:**
* **Smoke Tradition:** We own our own chambers for traditional smoking over cold beech and hornbeam smoke.
* **Logistical Excellence:** Our own fleet of vehicles with controlled temperature regimes (refrigerated trucks).
* **Wholesale Standard:** Priority processing and personalized meat cuts.""",
        "haccp_title": "Food Safety and HACCP: Uncompromising Standards",
        "haccp_text": """At Kojundžić Butchery, hygiene is the foundation of our family reputation. In 2026, we apply the latest quality monitoring technologies.
* **Full Traceability:** Every piece of meat has a documented path – we know exactly which farm it comes from.
* **Modern Facility:** Our facility in Sisak is under constant veterinary supervision with strict HACCP protocols.""",
        "info_title": "Our Story: Family, Sisak, and True Quality",
        "info_text": """Located in the heart of Sisak, the Kojundžić family has been preserving the skill of traditional meat preparation for generations. Our philosophy is simple: Respect nature and it will return the best flavors. We prepare meat slowly, using exclusively local spices, without additives.\n📍 **Main Sales Point:** Sisak Market.\n🕒 **Opening Hours:** Mon-Sat: 07:00 - 13:00""",
        "p1": "Smoked Hamburger", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters Mix", "p8": "Pancetta (Premium)", "p9": "Smoked Neck (Boneless)", "p10": "Smoked Pork Loin (Boneless)", "p11": "Smoked Tenderloin", "p12": "Homemade Cracklings",
        "p13": "Lard (Bucket)", "p14": "Blood Sausages (Homemade)", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Head", "p18": "White Bacon",
        "form_name": "Full Name*", "form_tel": "Phone Number for Delivery*", "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street and House Number*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED! THANK YOU FOR YOUR TRUST.", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Amount", "shipping_info": "SHIPPING DETAILS"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_suppliers": "🚜 LIEFERANTEN", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Ihr Warenkorb", "cart_empty": "ist leer",
        "note_vaga": """⚖️ **Hinweis zum Wiegen:** Die Produktpreise sind fest, aber den genauen Betrag Ihrer Rechnung erfahren wir erst nach dem präzisen Wiegen unmittelbar vor dem Verpacken. Den endgültigen Betrag erfahren Sie, wenn das Paket bei Ihnen ankommt und Sie es per Nachnahme bezahlen. Wir bemühen uns, die bestellten Mengen einzuhalten und die Differenz zwischen dem Informationsbetrag und dem Endbetrag so gering wie möglich zu halten.""",
        "note_delivery": """🚚 **Lieferung und Zahlung:** Die bestellten Artikel versenden wir über einen geprüften Lieferdienst an Ihre Heimatadresse oder an die nächstgelegene Abholstation, je nach Ihrer Wahl bei der Umleitung. Die Zahlung erfolgt **ausschließlich per Nachnahme** (bar an den Zusteller), wodurch wir die Sicherheit der Transaktion garantieren.""",
        "suppliers_title": "Unsere Partner: Die Kraft der lokalen Zucht",
        "suppliers_text": """Die Fleischqualität in der Metzgerei Kojundžić ist das direkte Ergebnis der Zusammenarbeit mit kleinen Familienbetrieben aus unserer unmittelbaren Umgebung. Wir glauben an kurze Lieferketten und die Unterstützung der lokalen Gemeinschaft.
\n**Gebiete, aus denen wir im Jahr 2026 Rohstoffe beziehen:**
* **Banovina und Posavina:** Unsere Hauptquellen für erstklassiges Schweine- und Rindfleisch. Die Tiere werden auf traditionelle Weise mit natürlicher Ernährung aufgezogen, was zu einer perfekten Fleischtextur führt.
* **Lonjsko Polje:** Wir sind besonders stolz auf die Zusammenarbeit mit Züchtern, deren Vieh auf freien Weiden in der unberührten Natur des Naturparks lebt.
* **Umgebung von Sisak:** Die tägliche Zusammenarbeit mit lokalen Landwirten stellt sicher, dass das Fleisch in kürzester Zeit vom Feld in unsere Metzgerei gelangt, was maximale Frische garantiert.""",
        "horeca_title": "HoReCa-Partnerschaft: Fundament erstklassiger Gastronomie",
        "horeca_text": """Als familiengeführtes Unternehmen respektieren wir zutiefst die Bemühungen unserer Kollegen im Gastrosektor. Wir verstehen, dass jedes erstklassige Gericht in einem Restaurant oder Hotel mit kompromissloser Rohstoffqualität beginnt.
\n**Unser Angebot für Partner im Jahr 2026 umfasst:**
* **Rauchtradition:** Wir verfügen über eigene Kammern für das traditionelle Räuchern über kaltem Buchen- und Hainbuchenrauch.
* **Logistische Exzellenz:** Eigene Fahrzeugflotte mit kontrolliertem Temperaturregime (Kühlwagen).
* **Großhandelsstandard:** Vorrangige Bearbeitung und personalisierte Fleischschnitte.""",
        "haccp_title": "Lebensmittelsicherheit und HACCP: Kompromisslose Standards",
        "haccp_text": """In der Metzgerei Kojundžić ist Hygiene das Fundament unseres Familienrufs. Im Jahr 2026 wenden wir die neuesten Technologien zur Qualitätsüberwachung an.
* **Vollständige Rückverfolgbarkeit (Traceability):** Jedes Stück Fleisch hat einen dokumentierten Weg – wir wissen genau, von welchem Bauernhof es stammt.
* **Moderner Betrieb:** Unser Objekt in Sisak steht unter ständiger veterinärmedizinischer Aufsicht mit strengen HACCP-Protokollen.""",
        "info_title": "Unsere Geschichte: Familie, Sisak und wahre Qualität",
        "info_text": """Im Herzen von Sisak ansässig, bewahrt die Familie Kojundžić seit Generationen die Kunst der traditionellen Fleischzubereitung. Unsere Philosophie ist einfach: Respektiere die Natur, und sie wird dir die besten Aromen zurückgeben. Wir bereiten das Fleisch langsam zu, unter ausschließlicher Verwendung einheimischer Gewürze, ohne Zusatzstoffe.\n📍 **Hauptverkaufsstelle:** Marktplatz Sisak (Tržnica).\n🕒 **Öffnungszeiten:** Mo-Sa: 07:00 - 13:00""",
        "p1": "Geräucherter Hamburger", "p2": "Geräuchertes Eisbein", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Hausgemachte Salami", "p6": "Geräucherte Knochen",
        "p7": "Geräucherte Pfoten Mix", "p8": "Pancetta (Premium)", "p9": "Geräucherter Nacken (o.K.)", "p10": "Geräuchertes Kotelett (o.K.)", "p11": "Geräuchertes Lendenstück", "p12": "Hausgemachte Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwürste (hausgemacht)", "p15": "Grillwürste", "p16": "Trockenrippchen", "p17": "Geräucherter Kopf", "p18": "Speck (weiß)",
        "form_name": "Vor- und Nachname*", "form_tel": "Telefonnummer für Lieferung*", "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße und Hausnummer*",
        "btn_order": "🚀 BESTELLUNG SENDEN", "success": "BESTELLUNG ERFOLGREICH ÜBERMITTELT! VIELEN DANK FÜR IHR VERTRAUEN.", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Informativer Betrag", "shipping_info": "LIEFERDATEN"
    }
}

# --- 3. PROIZVODI ---
PROIZVODI = [
    {"id": "p1", "cijena": 9.50, "jed": "kg"}, {"id": "p2", "cijena": 5.50, "jed": "kg"},
    {"id": "p3", "cijena": 5.50, "jed": "kg"}, {"id": "p4", "cijena": 13.00, "jed": "kg"},
    {"id": "p5", "cijena": 16.00, "jed": "kg"}, {"id": "p6", "cijena": 2.50, "jed": "kg"},
    {"id": "p7", "cijena": 2.50, "jed": "kg"}, {"id": "p8", "cijena": 16.00, "jed": "kg"},
    {"id": "p9", "cijena": 11.00, "jed": "kg"}, {"id": "p10", "cijena": 10.00, "jed": "kg"},
    {"id": "p11", "cijena": 12.00, "jed": "kg"}, {"id": "p12", "cijena": 18.00, "jed": "kg"},
    {"id": "p13", "cijena": 18.00, "jed": "pc"}, {"id": "p14", "cijena": 8.00, "jed": "kg"},
    {"id": "p15", "cijena": 8.00, "jed": "kg"}, {"id": "p16", "cijena": 9.00, "jed": "kg"},
    {"id": "p17", "cijena": 2.50, "jed": "kg"}, {"id": "p18", "cijena": 8.00, "jed": "kg"}
]

# --- 4. FUNKCIJA ZA EMAIL ---
def posalji_email(sadrzaj, kupac_info):
    poruka_tekst = f"NOVA NARUDŽBA (2026):\n\nKUPAC:\n{kupac_info}\n\nSTAVKE:\n{sadrzaj}"
    msg = MIMEText(poruka_tekst)
    msg['Subject'] = f"Narudžba - {kupac_info.split(',')[0]}"
    msg['From'] = MOJ_EMAIL
    msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(MOJ_EMAIL, MOJA_LOZINKA)
            server.send_message(msg)
        return True
    except:
        return False

# --- 5. STREAMLIT UI ---
st.set_page_config(page_title="Mesnica Kojundžić", layout="wide")

if 'kosarica' not in st.session_state:
    st.session_state.kosarica = {}

lang = st.sidebar.selectbox("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[lang]

tabs = st.tabs([T["nav_shop"], T["nav_suppliers"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

with tabs[0]: # SHOP
    st.title(T["title_sub"])
    st.info(T["note_vaga"])
    st.warning(T["note_delivery"])
    
    st.divider()
    col1, col2 = st.columns(2)
    for i, p in enumerate(PROIZVODI):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            if p["jed"] == "kg":
                # LOGIKA: 0 -> 1.0 -> +0.5
                val = st.number_input(f"{T[p['id']]} ({p['cijena']:.2f} {T['curr']})", min_value=0.0, step=0.5, format="%.1f", key=p["id"])
                if 0.0 < val < 1.0:
                    val = 1.0
                    st.session_state[p["id"]] = 1.0
                    st.rerun()
            else:
                val = st.number_input(f"{T[p['id']]} ({p['cijena']:.2f} {T['curr']})", min_value=0, step=1, key=p["id"])
            
            if val > 0:
                st.session_state.kosarica[p["id"]] = {"qty": val, "price": p["cijena"], "unit": p["jed"]}
            elif p["id"] in st.session_state.kosarica:
                del st.session_state.kosarica[p["id"]]

    if st.session_state.kosarica:
        st.divider()
        st.header(T["cart_title"])
        ukupno = 0
        prikaz_narudzbe = ""
        for pid, d in st.session_state.kosarica.items():
            sub = d['qty'] * d['price']
            ukupno += sub
            linija = f"{T[pid]}: {d['qty']} {T['unit_'+d['unit']]} x {d['price']} = {sub:.2f} {T['curr']}"
            st.write(linija)
            prikaz_narudzbe += linija + "\n"
        
        st.subheader(f"{T['total']}: {ukupno:.2f} {T['curr']}")
        
        with st.form("order_form"):
            st.write(T["shipping_info"])
            f_ime = st.text_input(T["form_name"])
            f_tel = st.text_input(T["form_tel"])
            f_grad = st.text_input(T["form_city"])
            f_zip = st.text_input(T["form_zip"])
            f_adr = st.text_input(T["form_addr"])
            
            if st.form_submit_button(T["btn_order"]):
                if f_ime and f_tel and f_adr:
                    info = f"{f_ime}, Tel: {f_tel}, Grad: {f_grad}, ZIP: {f_zip}, Adresa: {f_adr}"
                    if posalji_email(prikaz_narudzbe, info):
                        st.success(T["success"])
                        st.session_state.kosarica = {}
                        time.sleep(3)
                        st.rerun()
                else:
                    st.error("Molimo ispunite obavezna polja!")

with tabs[1]:
    st.header(T["suppliers_title"])
    st.write(T["suppliers_text"])

with tabs[2]:
    st.header(T["horeca_title"])
    st.write(T["horeca_text"])

with tabs[3]:
    st.header(T["haccp_title"])
    st.write(T["haccp_text"])

with tabs[4]:
    st.header(T["info_title"])
    st.write(T["info_text"])
