import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (HRVATSKI, ENGLESKI, NJEMAČKI) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Vaša Košarica", "cart_empty": "Vaša košarica je trenutno prazna. Odaberite domaće delicije iz ponude!",
        "note_vaga": "⚖️ **Napomena o vaganju:** Naši su proizvodi ručno obrađeni i prirodni. Navedene cijene su fiksne po jedinici mjere, ali točan iznos Vašeg računa znat ćemo nakon preciznog vaganja svakog komada prije same isporuke.",
        "total": "Informativni iznos", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POTVRDI NARUDŽBU", "success": "Hvala Vam! Narudžba je zaprimljena, javit ćemo Vam se ubrzo!",
        "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "tax": "PDV uključen", "shipping_info": "PODACI ZA DOSTAVU",
        
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "horeca_text": """Kao obiteljski posao, duboko cijenimo rad naših kolega u ugostiteljstvu. Razumijemo da vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom sirovinom. 
        \n**Što nudimo našim HoReCa partnerima u 2026. godini:**
        \n* **Autentični miris dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba, što Vašim jelima daje onaj prepoznatljiv, domaći potpis.
        \n* **Sigurna dostava:** Raspolažemo vlastitim vozilima s kontroliranim temperaturnim režimom (hladnjače), jamčeći svježinu u svakoj isporuci.
        \n* **Veleprodajna podrška:** Redovnim partnerima osiguravamo prioritetnu obradu narudžbi i stabilne uvjete poslovanja.""",
        "horeca_mail": "Za kreiranje individualnog cjenika i dogovor o suradnji, pišite nam na:",
        
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "haccp_text": """U mesnici Kojundžić, higijena nije samo zakonska obveza, već temelj našeg obraza. U 2026. godini primjenjujemo najstrože standarde kontrole kvalitete.
        \n* **Potpuna sljedivost:** Svaki komad mesa u našoj ponudi ima svoj 'rodni list'. Točno znamo s koje farme dolazi i tko ga je uzgojio.
        \n* **Strogi HACCP protokoli:** Naš moderni pogon u Sisku pod stalnim je nadzorom. Svaki korak – od prijema stoke, preko zrenja i dimljenja, do finalnog pakiranja – odvija se u sterilnim i temperaturno kontroliranim uvjetima.
        \n* **EU Certifikacija:** Naša proizvodnja u potpunosti zadovoljava visoke kriterije Europske unije o sigurnosti hrane, uz redovite laboratorijske analize.""",
        
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu pretvaranja najboljeg domaćeg mesa u vrhunske delicije. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima.
        \n**Zašto odabrati nas?**
        \nVjerujemo da se prava kvaliteta ne može postići industrijskom brzinom. Naša stoka dolazi isključivo od malih, provjerenih uzgajivača s pašnjaka Lonjskog polja, Banovine i Posavine. Meso pripremamo polako, uz prirodne začine i bez nepotrebnih aditiva.
        \nKada kupujete kod nas, podržavate lokalne farmere i tradiciju koja izumire. Naša misija je donijeti miris domaće kuhinje u Vaš dom, baš onako kako su to radili naši stari. Hvala Vam na povjerenju!""",
        
        "footer": "© 2026 Mesnica Kojundžić Sisak | Tradicija kojoj vjerujete", "status_msg": "Slanje narudžbe...", "err_msg": "Greška! Molimo pokušajte ponovo.",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 FOR CATERERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Your Cart", "cart_empty": "Your cart is currently empty. Choose some homemade delicacies!",
        "note_vaga": "⚖️ **Note on weighing:** Our products are hand-processed and natural. Prices are fixed per unit, but the exact amount will be known after precise weighing before delivery.",
        "total": "Informative total", "form_name": "Full Name*", "form_tel": "Phone number*",
        "form_city": "City*", "form_zip": "Postal code*", "form_addr": "Street and number*",
        "form_country": "Country*", "btn_order": "🚀 CONFIRM ORDER", "success": "Thank you! Order received, we will contact you soon!",
        "unit_kg": "kg", "unit_pc": "pcs", "curr": "€", "tax": "VAT included", "shipping_info": "SHIPPING DETAILS",
        
        "horeca_title": "Partnership based on trust and tradition",
        "horeca_text": """As a family business, we deeply value the work of our colleagues in the catering industry. We understand that a top-tier dish in a restaurant or hotel starts with uncompromising raw materials.
        \n**What we offer our HoReCa partners in 2026:**
        \n* **Authentic smoke aroma:** We have our own chambers for traditional cold smoking using beech and hornbeam wood, giving your dishes that recognizable, homemade signature.
        \n* **Safe delivery:** We use our own refrigerated vehicles with controlled temperature regimes, guaranteeing freshness in every delivery.
        \n* **Wholesale support:** For regular partners, we ensure priority order processing and stable business conditions.""",
        "horeca_mail": "For a personalized price list and cooperation agreement, contact us at:",
        
        "haccp_title": "Food Safety: From Field to Your Table",
        "haccp_text": """At Kojundžić Butcher Shop, hygiene is not just a legal obligation, but the foundation of our reputation. In 2026, we apply the strictest quality control standards.
        \n* **Full Traceability:** Every piece of meat in our offer has its own 'birth certificate'. We know exactly which farm it comes from and who raised it.
        \n* **Strict HACCP Protocols:** Our modern facility in Sisak is under constant supervision. Every step – from livestock reception to aging, smoking, and final packaging – takes place in sterile and temperature-controlled conditions.
        \n* **EU Certification:** Our production fully meets the high criteria of the European Union on food safety, with regular laboratory analyses.""",
        
        "info_title": "Our Story: Family, Sisak, and Genuine Quality",
        "info_text": """Located in the heart of Sisak, the Kojundžić family has for generations preserved the skill of turning the best domestic meat into premium delicacies. Our philosophy is simple: Respect nature, and it will reward you with the best flavors.
        \n**Why choose us?**
        \nWe believe that true quality cannot be achieved at industrial speed. Our livestock comes exclusively from small, verified breeders from the pastures of Lonjsko Polje, Banovina, and Posavina. We prepare meat slowly, with natural spices and without unnecessary additives.
        \nWhen you buy from us, you support local farmers and dying traditions. Our mission is to bring the aroma of home cooking to your home, just as our ancestors did. Thank you for your trust!""",
        
        "footer": "© 2026 Butcher Kojundžić Sisak | Quality you can trust", "status_msg": "Sending order...", "err_msg": "Error! Please try again.",
        "p1": "Smoked bacon", "p2": "Smoked pork hock", "p3": "Smoked brisket tips", "p4": "Slavonian sausage", "p5": "Homemade salami", "p6": "Smoked bones",
        "p7": "Smoked pork feet mix", "p8": "Pancetta (Premium)", "p9": "Smoked neck (Boneless)", "p10": "Smoked loin (Boneless)", "p11": "Smoked tenderloin", "p12": "Homemade pork rinds",
        "p13": "Pork lard (bucket)", "p14": "Blood sausage (home)", "p15": "Grill sausages", "p16": "Dry ribs", "p17": "Smoked head", "p18": "Soap bacon"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 FÜR GASTRONOMEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI & FLEISCHVERARBEITUNG KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Warenkorb", "cart_empty": "Ihr Warenkorb ist leer. Wählen Sie hausgemachte Spezialitäten aus!",
        "note_vaga": "⚖️ **Hinweis zum Wiegen:** Unsere Produkte sind handverarbeitet und naturbelassen. Die Preise sind pro Einheit fest, der genaue Betrag wird jedoch nach dem Wiegen vor der Lieferung ermittelt.",
        "total": "Informativer Betrag", "form_name": "Vor- und Nachname*", "form_tel": "Telefonnummer*",
        "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße und Hausnummer*",
        "form_country": "Land*", "btn_order": "🚀 BESTELLUNG BESTÄTIGEN", "success": "Vielen Dank! Bestellung erhalten, wir kontaktieren Sie bald!",
        "unit_kg": "kg", "unit_pc": "Stk", "curr": "€", "tax": "Inkl. MwSt.", "shipping_info": "LIEFERDATEN",
        
        "horeca_title": "Partnerschaft auf Basis von Vertrauen und Tradition",
        "horeca_text": """Als Familienunternehmen schätzen wir die Arbeit unserer Kollegen in der Gastronomie zutiefst. Wir wissen, dass ein erstklassiges Gericht im Restaurant oder Hotel mit kompromisslosen Rohstoffen beginnt.
        \n**Was wir unseren HoReCa-Partnern im Jahr 2026 bieten:**
        \n* **Authentisches Raucharoma:** Wir verfügen über eigene Kammern für die traditionelle Kaltrauchräucherung mit Buchen- und Hainbuchenholz, die Ihren Gerichten eine hausgemachte Note verleiht.
        \n* **Sichere Lieferung:** Wir nutzen eigene Kühlfahrzeuge mit kontrollierter Temperatur, um Frische bei jeder Lieferung zu garantieren.
        \n* **Großhandels-Support:** Für Stammpartner garantieren wir eine vorrangige Auftragsbearbeitung und stabile Geschäftsbedingungen.""",
        "horeca_mail": "Für eine personalisierte Preisliste und Kooperationsvereinbarung kontaktieren Sie uns unter:",
        
        "haccp_title": "Lebensmittelsicherheit: Vom Feld bis zu Ihrem Tisch",
        "haccp_text": """In der Metzgerei Kojundžić ist Hygiene nicht nur eine gesetzliche Pflicht, sondern das Fundament unseres Rufes. Im Jahr 2026 wenden wir strengste Qualitätskontrollstandards an.
        \n* **Vollständige Rückverfolgbarkeit:** Jedes Stück Fleisch in unserem Angebot hat seine eigene 'Geburtsurkunde'. Wir wissen genau, von welchem Bauernhof es kommt.
        \n* **Strenge HACCP-Protokolle:** Unsere moderne Anlage in Sisak steht unter ständiger Aufsicht. Jeder Schritt – von der Viehannahme bis zur Reifung und Verpackung – erfolgt unter sterilen Bedingungen.
        \n* **EU-Zertifizierung:** Unsere Produktion erfüllt die hohen Kriterien der Europäischen Union zur Lebensmittelsicherheit mit regelmäßigen Laboranalysen.""",
        
        "info_title": "Unsere Geschichte: Familie, Sisak und echte Qualität",
        "info_text": """Im Herzen von Sisak gelegen, bewahrt die Familie Kojundžić seit Generationen die Kunst, bestes heimisches Fleisch in Premium-Delikatessen zu verwandeln. Unsere Philosophie: Respektiere die Natur, und sie belohnt dich mit bestem Geschmack.
        \n**Warum uns wählen?**
        \nWir glauben, dass wahre Qualität nicht mit industrieller Geschwindigkeit erreicht werden kann. Unser Vieh stammt ausschließlich von kleinen, geprüften Züchtern aus der Region Lonjsko Polje, Banovina und Posavina. Wir bereiten das Fleisch langsam zu, mit natürlichen Gewürzen und ohne unnötige Zusatzstoffe.
        \nMit Ihrem Kauf unterstützen Sie lokale Bauern und Traditionen. Unsere Mission ist es, den Duft der Heimatküche in Ihr Zuhause zu bringen. Vielen Dank für Ihr Vertrauen!""",
        
        "footer": "© 2026 Metzgerei Kojundžić Sisak | Qualität, der Sie vertrauen", "status_msg": "Bestellung wird gesendet...", "err_msg": "Fehler! Bitte versuchen Sie es erneut.",
        "p1": "Geräucherter Speck", "p2": "Geräucherte Stelze", "p3": "Geräucherte Brustspitzen", "p4": "Slawonische Wurst", "p5": "Hausgemachte Salami", "p6": "Geräucherte Knochen",
        "p7": "Schweinefüße Mix", "p8": "Pancetta (Premium)", "p9": "Schweinenacken (o.K.)", "p10": "Karree geräuchert", "p11": "Lende geräuchert", "p12": "Hausgemachte Grieben",
        "p13": "Schweineschmalz (Eimer)", "p14": "Blutwurst (hausgemacht)", "p15": "Grillwürste", "p16": "Trockene Rippchen", "p17": "Geräucherter Kopf", "p18": "Seifenspeck"
    }
}

# --- 3. PODACI O PROIZVODIMA ---
PRODUCTS = [
    {"id": "p1", "price": 9.50, "unit": "kg"}, {"id": "p2", "price": 7.80, "unit": "kg"},
    {"id": "p3", "price": 6.50, "unit": "kg"}, {"id": "p4", "price": 14.20, "unit": "kg"},
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
    T = LANG_MAP[lang_code]
    summary = "\n".join([f"- {item['name']}: {item['qty']} {item['unit']} ({item['sub']:.2f}€)" for item in cart_items])
    
    email_body = f"""
    NOVA NARUDŽBA - WEB TRGOVINA 2026
    ---------------------------------
    KLIJENT: {client_info['name']}
    TEL: {client_info['tel']}
    ADRESA: {client_info['addr']}, {client_info['zip']} {client_info['city']}
    DRŽAVA: {client_info['country']}
    
    STAVKE NARUDŽBE:
    {summary}
    
    UKUPNO (INFORMATIVNO): {client_info['total']:.2f} EUR
    ---------------------------------
    Sustav Mesnice Kojundžić Sisak
    """
    
    msg = MIMEText(email_body)
    msg['Subject'] = f"Narudžba: {client_info['name']}"
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
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide", page_icon="🥩")

if 'cart' not in st.session_state:
    st.session_state.cart = {}

with st.sidebar:
    st.title("⚙️ Postavke / Settings")
    current_lang = st.selectbox("Jezik / Language", list(LANG_MAP.keys()))
    T = LANG_MAP[current_lang]
    st.divider()
    menu = st.radio("Navigacija", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])
    st.divider()
    st.markdown(f"*{T['footer']}*")

if menu == T["nav_shop"]:
    st.title("🥩 " + T["title_sub"])
    shop_col, cart_col = st.columns([2, 1])
    
    with shop_col:
        st.subheader(T["nav_shop"])
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.expander(f"**{T[p['id']]}**", expanded=True):
                    st.write(f"{p['price']:.2f} {T['curr']} / {T['unit_'+p['unit']]}")
                    qty = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=0.5, key=f"input_{p['id']}")
                    if qty > 0:
                        st.session_state.cart[p['id']] = qty
                    elif p['id'] in st.session_state.cart:
                        del st.session_state.cart[p['id']]

    with cart_col:
        st.subheader(T["cart_title"])
        if not st.session_state.cart:
            st.info(T["cart_empty"])
        else:
            total_sum = 0
            summary_list = []
            for pid, q in st.session_state.cart.items():
                p_data = next(x for x in PRODUCTS if x['id'] == pid)
                sub = q * p_data['price']
                total_sum += sub
                st.write(f"**{T[pid]}**")
                st.write(f"{q} {T['unit_'+p_data['unit']]} = {sub:.2f} €")
                summary_list.append({'name': T[pid], 'qty': q, 'unit': T['unit_'+p_data['unit']], 'sub': sub})
            
            st.divider()
            st.markdown(f"### {T['total']}: {total_sum:.2f} €")
            st.caption(T["note_vaga"])
            
            with st.form("checkout_form"):
                st.write(f"✍️ **{T['shipping_info']}**")
                c_name = st.text_input(T["form_name"])
                c_tel = st.text_input(T["form_tel"])
                c_addr = st.text_input(T["form_addr"])
                c_city = st.text_input(T["form_city"])
                c_zip = st.text_input(T["form_zip"])
                c_country = st.text_input(T["form_country"])
                
                if st.form_submit_button(T["btn_order"]):
                    if c_name and c_tel and c_addr:
                        info = {"name": c_name, "tel": c_tel, "addr": c_addr, "city": c_city, "zip": c_zip, "country": c_country, "total": total_sum}
                        if send_order_email(info, summary_list, current_lang):
                            st.success(T["success"])
                            st.session_state.cart = {}
                            time.sleep(3)
                            st.rerun()
                        else:
                            st.error(T["err_msg"])
                    else:
                        st.warning("!!!")

elif menu == T["nav_horeca"]:
    st.header(T["horeca_title"])
    st.write(T["horeca_text"])
    st.info(f"📧 {T['horeca_mail']} **{MOJ_EMAIL}**")

elif menu == T["nav_haccp"]:
    st.header(T["haccp_title"])
    st.write(T["haccp_text"])
    st.success("✅ Certificirana proizvodnja 2026. / Certified production 2026.")

elif menu == T["nav_info"]:
    st.header(T["info_title"])
    st.write(T["info_text"])
    st.markdown("📍 **Sisak, Hrvatska**")
