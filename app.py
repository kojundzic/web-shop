import streamlit as st
import smtplib
from email.mime.text import MIMEText

# --- 1. KONFIGURACIJA (Provjeriti Gmail App Password) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "horeca_text": """Kao obiteljski posao, duboko cijenimo rad naših kolega u ugostiteljstvu. Razumijemo da vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom sirovinom. 

**Što nudimo našim HoReCa partnerima u 2026. godini:**
* **Autentični miris dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba.
* **Sigurna dostava:** Raspolažemo vlastitim vozilima s kontroliranim temperaturnim režimom (hladnjače).
* **Veleprodajna podrška:** Redovnim partnerima osiguravamo prioritetnu obradu narudžbi i prilagođene rezove mesa.""",
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "haccp_text": """U mesnici Kojundžić, higijena je temelj našeg obraza. U 2026. godini primjenjujemo najstrože standarde kontrole kvalitete.
* **Potpuna sljedivost:** Svaki komad mesa u našoj ponudi ima svoj 'rodni list' – točno znamo s koje farme dolazi.
* **Strogi HACCP protokoli:** Naš moderni pogon u Sisku pod stalnim je nadzorom, uz redovite laboratorijske kontrole i sanitarne standarde koji nadilaze zakonske okvire.""",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima. 
Meso pripremamo polako, uz korištenje isključivo prirodnih začina, bez nepotrebnih aditiva i kemijskih dodataka. Mi ne proizvodimo samo hranu – mi čuvamo baštinu sisačkog kraja.""",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": "⚖️ **Napomena:** Konačan iznos računa znat ćemo nakon preciznog vaganja.",
        "note_delivery": "🚚 **Dostava:** Plaćanje se vrši isključivo **pouzećem**.",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "Narudžba zaprimljena!", "unit_kg": "kg", "unit_pc": "kom", "total": "Informativni iznos",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "KOJUNDŽIĆ BUTCHERY | SISAK 2026.",
        "horeca_title": "Partnership Based on Trust",
        "horeca_text": "We provide authentic beech-smoked meats and reliable refrigerated delivery for 2026 hospitality partners.",
        "haccp_title": "Food Safety",
        "haccp_text": "Strict HACCP protocols and full traceability from farm to table.",
        "info_title": "Our Story",
        "info_text": "Generations of tradition in Sisak, using natural spices and slow-smoking techniques.",
        "cart_title": "🛒 Your Cart", "cart_empty": "is empty", "btn_order": "🚀 SEND ORDER", "unit_kg": "kg", "unit_pc": "pcs", "total": "Total (Est.)", "success": "Sent!"
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | SISAK 2026.",
        "horeca_title": "Vertrauensvolle Partnerschaft",
        "horeca_text": "Authentisches Raucharoma und gekühlte Lieferung für die Gastronomie im Jahr 2026.",
        "haccp_title": "Lebensmittelsicherheit",
        "haccp_text": "Höchste HACCP-Standards und lückenlose Rückverfolgbarkeit.",
        "info_title": "Unsere Geschichte",
        "info_text": "Traditionelle Fleischzubereitung aus Sisak – ohne Chemie, nur Natur.",
        "cart_title": "🛒 Warenkorb", "cart_empty": "ist leer", "btn_order": "🚀 ABSCHICKEN", "unit_kg": "kg", "unit_pc": "Stk", "total": "Summe", "success": "Eingegangen!"
    }
}

# --- 3. PROIZVODI ---
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

# --- 4. FUNKCIJA ZA SLANJE EMAILA ---
def send_email(info, cart_items):
    summary = "\n".join([f"- {i['name']}: {i['qty']} {i['unit']}" for i in cart_items])
    body = f"NOVA NARUDŽBA - 2026\n\nKupac: {info['name']}\nTel: {info['tel']}\nAdresa: {info['addr']}, {info['zip']} {info['city']}\n\nSTAVKE:\n{summary}\n\nUKUPNO (Informativno): {info['total']:.2f} €"
    msg = MIMEText(body)
    msg['Subject'] = f"Narudžba: {info['name']}"
    msg['From'] = MOJ_EMAIL
    msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls()
            s.login(MOJ_EMAIL, MOJA_LOZINKA)
            s.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Greška pri slanju: {e}")
        return False

# --- 5. UI ---
st.set_page_config(page_title="Mesnica Kojundžić 2026", layout="wide")

if 'cart' not in st.session_state:
    st.session_state.cart = {}

with st.sidebar:
    lang_choice = st.selectbox("Jezik / Language", list(LANG_MAP.keys()))
    T = LANG_MAP[lang_choice]
    menu = st.radio("Navigacija", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if menu == T["nav_shop"]:
    st.title(T["title_sub"])
    col1, col2 = st.columns([1.6, 1])
    
    with col1:
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.container(border=True):
                    st.write(f"**{T.get(p['id'], p['id'])}**")
                    st.write(f"{p['price']:.2f} € / {T['unit_'+p['unit']]}")
                    step_val = 0.5 if p['unit'] == "kg" else 1.0
                    q = st.number_input(f"Količina ({T['unit_'+p['unit']]})", min_value=0.0, step=step_val, key=f"inp_{p['id']}")
                    if q > 0: st.session_state.cart[p['id']] = q
                    elif p['id'] in st.session_state.cart: del st.session_state.cart[p['id']]

    with col2:
        status = f" {T['cart_empty']}" if not st.session_state.cart else ""
        st.subheader(f"{T['cart_title']}{status}")
        
        tot = 0; items_mail = []
        for pid, q in st.session_state.cart.items():
            pd = next(x for x in PRODUCTS if x['id'] == pid)
            sub = q * pd['price']; tot += sub
            st.write(f"✅ {T.get(pid, pid)}: {q} {T['unit_'+pd['unit']]} = {sub:.2f} €")
            items_mail.append({'name': T.get(pid, pid), 'qty': q, 'unit': T['unit_'+pd['unit']]})
        
        if st.session_state.cart:
            st.divider()
            st.write(f"### {T['total']}: {tot:.2f} €")
            st.info(T["note_vaga"])
            
            with st.form("order_form"):
                name = st.text_input(T.get("form_name", "Ime*"))
                tel = st.text_input(T.get("form_tel", "Tel*"))
                addr = st.text_input(T.get("form_addr", "Adresa*"))
                city = st.text_input(T.get("form_city", "Grad*"))
                zip_c = st.text_input(T.get("form_zip", "Zip*"))
                
                if st.form_submit_button(T["btn_order"]):
                    if name and tel and addr:
                        info = {"name": name, "tel": tel, "addr": addr, "city": city, "zip": zip_c, "total": tot}
                        if send_email(info, items_mail):
                            st.success(T["success"])
                            st.session_state.cart = {}
                            st.rerun()
                    else: st.warning("Molimo ispunite polja sa zvjezdicom (*)")

elif menu == T["nav_horeca"]:
    st.title(T["horeca_title"])
    st.markdown(T["horeca_text"])
elif menu == T["nav_haccp"]:
    st.title(T["haccp_title"])
    st.markdown(T["haccp_text"])
elif menu == T["nav_info"]:
    st.title(T["info_title"])
    st.markdown(T["info_text"])
