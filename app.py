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

# --- 2. MASTER PRIJEVODI (POTPUNI I PROŠIRENI - 2026.) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo tek nakon preciznog vaganja neposredno prije pakiranja. Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. Trudimo se da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "note_delivery": """🚚 **Dostava i plaćanje:** Naručene artikle šaljemo putem provjerene dostavne službe na kućnu adresu ili u najbliži paketomat, ovisno o Vašem izboru pri preusmjeravanju. Plaćanje se vrši **isključivo pouzećem** (gotovinom dostavljaču), čime jamčimo sigurnost transakcije.""",
        "suppliers_title": "Naši partneri: Snaga lokalnog uzgoja",
        "suppliers_text": """Kvaliteta mesa u Mesnici Kojundžić izravan je rezultat suradnje s malim obiteljskim gospodarstvima iz našeg neposrednog okruženja. Vjerujemo u kratke lance opskrbe i podršku lokalnoj zajednici.
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
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Meso pripremamo polako, uz korištenje isključivo domaćih začina, bez aditiva.\n📍 **Glavno prodajno mjesto:** Tržnica Sisak.\n🕒 **Radno vrijeme:** Pon-Sub: 07:00 - 13:00""",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*", "form_country": "Država*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA! HVALA VAM NA POVJERENJU.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljeni nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_suppliers": "🚜 SUPPLIERS", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "cart_title": "🛒 Your Cart", "cart_empty": "is empty",
        "note_vaga": """⚖️ **Weight Note:** Product prices are fixed, but the exact total of your invoice will be confirmed after precise weighing just before packaging. You will pay the final amount upon delivery. We strive for minimal differences between estimated and final amounts.""",
        "note_delivery": """🚚 **Delivery and Payment:** We ship via a verified service to your home address or parcel locker. Payment is **exclusively Cash on Delivery** (cash to courier), ensuring security.""",
        "suppliers_title": "Our Partners: The Strength of Local Farming",
        "suppliers_text": """Quality at Kojundžić Butchery comes from small family farms in Banovina, Posavina, and Lonjsko Polje. We believe in short supply chains and local support.""",
        "horeca_title": "HoReCa Partnership: Foundation of Hospitality",
        "horeca_text": """We offer smoke tradition, logistical excellence, and priority wholesale processing for our 2026 partners.""",
        "haccp_title": "Food Safety and HACCP",
        "haccp_text": """Hygiene is the foundation of our reputation. We apply the latest quality monitoring with full traceability and strict HACCP protocols.""",
        "info_title": "Our Story: Family, Sisak, and Quality",
        "info_text": """Generations of traditional meat preparation in Sisak using only local spices and no additives.\n📍 **Main Shop:** Sisak Market.\n🕒 **Hours:** Mon-Sat: 07:00 - 13:00""",
        "form_name": "Full Name*", "form_tel": "Phone*", "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*", "form_country": "Country*",
        "btn_order": "🚀 SEND ORDER", "success": "ORDER SUCCESSFULLY SUBMITTED!", "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "total": "Estimated Total", "shipping_info": "SHIPPING DETAILS",
        "p1": "Smoked Hamburger", "p2": "Smoked Pork Hock", "p3": "Smoked Brisket Tips", "p4": "Slavonian Sausage", "p5": "Homemade Salami", "p6": "Smoked Bones",
        "p7": "Smoked Trotters Mix", "p8": "Pancetta (Premium)", "p9": "Smoked Neck", "p10": "Smoked Loin", "p11": "Smoked Tenderloin", "p12": "Cracklings",
        "p13": "Lard", "p14": "Blood Sausages", "p15": "Grill Sausages", "p16": "Dry Ribs", "p17": "Smoked Head", "p18": "White Bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_suppliers": "🚜 LIEFERANTEN", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "ist leer",
        "note_vaga": """⚖️ **Hinweis zum Wiegen:** Die Preise sind fest, der genaue Betrag wird jedoch erst nach dem Wiegen ermittelt. Die Bezahlung erfolgt per Nachnahme.""",
        "note_delivery": """🚚 **Lieferung:** Zustellung an Ihre Adresse oder Packstation. Die Zahlung erfolgt **ausschließlich per Nachnahme** bar an den Zusteller.""",
        "suppliers_title": "Unsere Partner: Lokale Zucht",
        "suppliers_text": """Die Qualität kommt von kleinen Familienbetrieben aus Banovina, Posavina und Lonjsko Polje. Wir unterstützen die lokale Gemeinschaft.""",
        "horeca_title": "HoReCa-Partnerschaft",
        "horeca_text": """Rauchtradition, Logistik und Großhandelsstandard für Partner im Jahr 2026.""",
        "haccp_title": "Sicherheit und HACCP",
        "haccp_text": """Hygiene ist das Fundament unseres Rufs. Wir nutzen modernste Überwachung und ständige veterinärmedizinische Kontrolle.""",
        "info_title": "Unsere Geschichte",
        "info_text": """In Sisak bewahrt die Familie Kojundžić seit Generationen die Kunst der Fleischzubereitung bez Zusatzstoffe.\n📍 **Markt Sisak.**\n🕒 **Mo-Sa: 07:00 - 13:00**""",
        "form_name": "Name*", "form_tel": "Telefon*", "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*", "form_country": "Land*",
        "btn_order": "🚀 BESTELLEN", "success": "BESTELLUNG ERFOLGREICH!", "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "total": "Gesamtsumme", "shipping_info": "LIEFERDATEN",
        "p1": "Geräucherter Hamburger", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Salami", "p6": "Knochen",
        "p7": "Füße Mix", "p8": "Pancetta", "p9": "Nacken", "p10": "Kotelett", "p11": "Lende", "p12": "Grieben",
        "p13": "Schmalz", "p14": "Blutwürste", "p15": "Grillwürste", "p16": "Rippchen", "p17": "Kopf", "p18": "Speck"
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
    st.divider()
    col_proizvodi, col_kosarica = st.columns([1.5, 1])
    
    with col_proizvodi:
        p_col1, p_col2 = st.columns(2)
        for i, p in enumerate(PROIZVODI):
            target_col = p_col1 if i % 2 == 0 else p_col2
            with target_col:
                if p["jed"] == "kg":
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

    with col_kosarica:
        st.header(T["cart_title"])
        if st.session_state.kosarica:
            ukupno = 0
            prikaz_narudzbe = ""
            for pid, d in st.session_state.kosarica.items():
                sub = d['qty'] * d['price']
                ukupno += sub
                linija = f"{T[pid]}: {d['qty']} {T['unit_'+d['unit']]} x {d['price']} = {sub:.2f} {T['curr']}"
                st.write(linija)
                prikaz_narudzbe += linija + "\n"
            
            st.subheader(f"{T['total']}: {ukupno:.2f} {T['curr']}")
            st.info(T["note_vaga"])
            st.warning(T["note_delivery"])
            
            with st.form("order_form"):
                st.write(T["shipping_info"])
                f_ime = st.text_input(T["form_name"])
                f_tel = st.text_input(T["form_tel"])
                f_country = st.text_input(T["form_country"]) # DODANO POLJE DRŽAVA
                f_grad = st.text_input(T["form_city"])
                f_zip = st.text_input(T["form_zip"])
                f_adr = st.text_input(T["form_addr"])
                
                if st.form_submit_button(T["btn_order"]):
                    if f_ime and f_tel and f_adr and f_country:
                        info = f"{f_ime}, Tel: {f_tel}, Država: {f_country}, Grad: {f_grad}, ZIP: {f_zip}, Adresa: {f_adr}"
                        if posalji_email(prikaz_narudzbe, info):
                            st.success(T["success"])
                            st.session_state.kosarica = {}
                            time.sleep(3)
                            st.rerun()
                    else:
                        st.error("Molimo ispunite obavezna polja!")
        else:
            st.write(T["cart_empty"])

with tabs[1]: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
with tabs[2]: st.header(T["horeca_title"]); st.write(T["horeca_text"])
with tabs[3]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
with tabs[4]: st.header(T["info_title"]); st.write(T["info_text"])
