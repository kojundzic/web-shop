import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (STRIKTNO I PRIVATNO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu"  # Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. PROŠIRENI MASTER PRIJEVODI (OSOBNI PRISTUP 2026.) ---
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
        \n* **Krojenje po mjeri:** Naši mesari pripremaju rezove točno prema željama Vašeg chefa – od debljine odreska do specifičnog postotka masnoće.
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

# --- 4. FUNKCIJE ---
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

# Inicijalizacija košarice
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Sidebar - Odabir jezika i navigacija
with st.sidebar:
    st.title("⚙️ Postavke")
    current_lang = st.selectbox("Izaberite jezik / Choose language", list(LANG_MAP.keys()))
    T = LANG_MAP[current_lang]
    st.divider()
    menu = st.radio("Navigacija", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])
    st.divider()
    st.markdown(f"*{T['footer']}*")

# --- STRANICA: TRGOVINA ---
if menu == T["nav_shop"]:
    st.title("🥩 " + T["title_sub"])
    
    shop_col, cart_col = st.columns([2, 1])
    
    with shop_col:
        st.subheader(T["nav_shop"])
        # Prikaz proizvoda u gridu
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.expander(f"**{T[p['id']]}**", expanded=True):
                    st.write(f"Cijena: {p['price']:.2f} {T['curr']} / {T['unit_'+p['unit']]}")
                    qty = st.number_input(f"Količina ({T['unit_'+p['unit']]})", min_value=0.0, step=0.5, key=f"input_{p['id']}")
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
                st.write(f"{q} {T['unit_'+p_data['unit']]} x {p_data['price']:.2f} = {sub:.2f} €")
                summary_list.append({'name': T[pid], 'qty': q, 'unit': T['unit_'+p_data['unit']], 'sub': sub})
            
            st.divider()
            st.markdown(f"### {T['total']}: {total_sum:.2f} €")
            st.caption(T["note_vaga"])
            
            # Forma za narudžbu
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
                        st.warning("Molimo ispunite obavezna polja označena sa *")

# --- STRANICA: HORECA ---
elif menu == T["nav_horeca"]:
    st.header(T["horeca_title"])
    st.write(T["horeca_text"])
    st.info(f"📧 {T['horeca_mail']} **{MOJ_EMAIL}**")
    st.image("https://images.unsplash.com") # Slika restorana

# --- STRANICA: HACCP ---
elif menu == T["nav_haccp"]:
    st.header(T["haccp_title"])
    st.write(T["haccp_text"])
    st.success("✅ Certificirana proizvodnja 2026.")
    st.image("https://images.unsplash.com") # Slika laboratorija/kontrole

# --- STRANICA: O NAMA ---
elif menu == T["nav_info"]:
    st.header(T["info_title"])
    st.write(T["info_text"])
    st.markdown("📍 **Gdje nas pronaći?** Sisak, Hrvatska - posjetite našu matičnu mesnicu!")
    st.image("https://images.unsplash.com") # Slika tradicionalnog mesa
