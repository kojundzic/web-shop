import streamlit as st
import smtplib
from email.mime.text import MIMEText

# --- 1. KONFIGURACIJA (FIKSNA) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI (SA STALNIM NAPOMENAMA I LOKACIJOM) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "je prazna",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo nakon vaganja. Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. Mi ćemo se truditi da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "note_delivery": """🚚 **Dostava i plaćanje:** Naručene artikle dostaviti će Vam dostavna služba na kućnu adresu. Alternativno, možete ih preusmjeriti u najbliži paketomat. Plaćanja se vrše **isključivo pouzećem** (prilikom preuzimanja paketa).""",
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "horeca_text": "Kao obiteljski posao, duboko cijenimo rad naših kolega u ugostiteljstvu...",
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "haccp_text": "U mesnici Kojundžić, higijena je temelj našeg obraza...",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. 
\n📍 **Glavno prodajno mjesto:** Tržnica Caprag, Sisak. \nRadno vrijeme: Pon-Sub: 07:00 - 13:00""",
        "form_name": "Ime i Prezime*", "form_tel": "Broj telefona za dostavu*", "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "Zaprimljeno! Javit ćemo Vam se uskoro.", "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "total": "Informativni iznos", "shipping_info": "PODACI ZA DOSTAVU"
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

def send_email(info, cart_items):
    summary = "\n".join([f"- {i['name']}: {i['qty']} {i['unit']}" for i in cart_items])
    body = f"NARUDŽBA 2026\n\nKupac: {info['name']}\nTel: {info['tel']}\nAdresa: {info['addr']}, {info['zip']} {info['city']}\n\nSTAVKE:\n{summary}\n\nUKUPNO: {info['total']:.2f} €"
    msg = MIMEText(body); msg['Subject'] = f"Narudžba: {info['name']}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls(); s.login(MOJ_EMAIL, MOJA_LOZINKA); s.send_message(msg)
        return True
    except: return False

# --- 4. UI ---
st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
if 'cart' not in st.session_state: st.session_state.cart = {}

with st.sidebar:
    lang_choice = st.selectbox("Jezik", list(LANG_MAP.keys()))
    T = LANG_MAP[lang_choice]
    menu = st.radio("Izbornik", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if menu == T["nav_shop"]:
    st.title(T["title_sub"])
    col1, col2 = st.columns([1.6, 1])
    
    with col1:
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.container(border=True):
                    name_p = T.get(f"p{idx+1}", f"Proizvod {idx+1}")
                    st.write(f"**{name_p}**")
                    st.write(f"{p['price']:.2f} € / {T['unit_'+p['unit']]}")
                    step = 0.5 if p['unit'] == "kg" else 1.0
                    q = st.number_input(f"{T['unit_'+p['unit']]}", min_value=0.0, step=step, key=f"z_{p['id']}")
                    if q > 0: st.session_state.cart[p['id']] = q
                    elif p['id'] in st.session_state.cart: del st.session_state.cart[p['id']]

    with col2:
        status = f" {T['cart_empty']}" if not st.session_state.cart else ""
        st.subheader(f"{T['cart_title']}{status}")
        
        tot = 0; items_mail = []
        for pid, q in st.session_state.cart.items():
            pd = next(x for x in PRODUCTS if x['id'] == pid)
            sub = q * pd['price']; tot += sub
            p_name = T.get(pid, pid)
            st.write(f"✅ {p_name}: {q} {T['unit_'+pd['unit']]} = {sub:.2f} €")
            items_mail.append({'name': p_name, 'qty': q, 'unit': T['unit_'+pd['unit']]})
        
        if st.session_state.cart:
            st.divider()
            st.write(f"### {T['total']}: {tot:.2f} €")
            
            # STALNO VIDLJIVE NAPOMENE ISPOD KOŠARICE
            st.info(T["note_vaga"])
            st.warning(T["note_delivery"])
            
            with st.form("checkout"):
                st.write(f"### {T['shipping_info']}")
                name = st.text_input(T["form_name"])
                tel = st.text_input(T["form_tel"])
                addr = st.text_input(T["form_addr"])
                city = st.text_input(T["form_city"])
                zip_c = st.text_input(T["form_zip"])
                
                if st.form_submit_button(T["btn_order"]):
                    if name and tel and addr:
                        info = {"name": name, "tel": tel, "addr": addr, "city": city, "zip": zip_c, "total": tot}
                        if send_email(info, items_mail):
                            st.success(T["success"])
                            st.session_state.cart = {}
                            st.rerun()
                    else: st.error("Ispunite obavezna polja (*)")

elif menu == T["nav_info"]:
    st.title(T["info_title"])
    st.markdown(T["info_text"])
    # KARTA I LOKACIJA
    st.subheader("📍 Naša lokacija (Tržnica Caprag)")
    import pandas as pd
    map_data = pd.DataFrame({'lat': [45.4622], 'lon': [16.3755]}) # Koordinate Tržnice Caprag
    st.map(map_data)

else:
    key_prefix = "horeca" if menu == T["nav_horeca"] else "haccp"
    st.title(T[f"{key_prefix}_title"])
    st.markdown(T[f"{key_prefix}_text"])
