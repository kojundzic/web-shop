import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (TRAJNO ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. MASTER PRIJEVODI ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Vaša Košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "note_vaga": """⚖️ **Napomena o vaganju:** Cijene proizvoda su fiksne, no točan iznos Vašeg računa znat ćemo nakon vaganja. 
        Konačan iznos znati ćete kada Vam paket stigne i kada ga budete plaćali pouzećem. 
        Mi ćemo se truditi da se pridržavamo naručenih količina i da informativni iznos i konačni iznos imaju što manju razliku.""",
        "total": "Informativni iznos", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom", "curr": "€", "tax": "PDV uključen", "shipping_info": "PODACI ZA DOSTAVU",
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "footer": "© 2026 Mesnica Kojundžić Sisak", "status_msg": "Slanje...", "err_msg": "Greška!"
    }
}

# --- 3. PODACI O PROIZVODIMA ---
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

# --- 4. FUNKCIJA ZA EMAIL ---
def send_email(info, cart_items, lang):
    summary = "\n".join([f"- {i['name']}: {i['qty']} {i['unit']}" for i in cart_items])
    body = f"NARUDŽBA 2026\nKupac: {info['name']}\nTel: {info['tel']}\nAdresa: {info['addr']}, {info['city']}\n\nStavke:\n{summary}\n\nInformativni iznos: {info['total']:.2f} €"
    msg = MIMEText(body); msg['Subject'] = f"Narudžba: {info['name']}"; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls(); s.login(MOJ_EMAIL, MOJA_LOZINKA); s.send_message(msg)
        return True
    except: return False

# --- 5. APP UI ---
st.set_page_config(page_title="Mesnica Kojundžić 2026", layout="wide")

if 'cart' not in st.session_state: st.session_state.cart = {}

with st.sidebar:
    lang_choice = st.selectbox("Jezik / Language", list(LANG_MAP.keys()))
    T = LANG_MAP[lang_choice]
    menu = st.radio("Meni", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if menu == T["nav_shop"]:
    st.title("🥩 " + T["title_sub"])
    col1, col2 = st.columns([2, 1]) # Lijeva kolona šira za artikle
    
    with col1:
        st.subheader(T["nav_shop"])
        p_cols = st.columns(2)
        for idx, p in enumerate(PRODUCTS):
            with p_cols[idx % 2]:
                with st.container(border=True):
                    st.write(f"**{T.get(p['id'], p['id'])}**")
                    st.write(f"{p['price']:.2f} € / {T['unit_'+p['unit']]}")
                    
                    if p['unit'] == "pc":
                        q = st.number_input(f"{T['unit_pc']}", min_value=0.0, step=1.0, key=f"q_{p['id']}")
                    else:
                        if f"state_{p['id']}" not in st.session_state: st.session_state[f"state_{p['id']}"] = 0.0
                        q = st.number_input(f"{T['unit_kg']}", min_value=0.0, step=0.5, key=f"q_{p['id']}")
                        
                        if q == 0.5 and st.session_state[f"state_{p['id']}"] == 0.0:
                            q = 1.0
                            st.session_state[f"state_{p['id']}"] = 1.0
                            st.rerun()
                        else:
                            st.session_state[f"state_{p['id']}"] = q

                    if q > 0: st.session_state.cart[p['id']] = q
                    elif p['id'] in st.session_state.cart: del st.session_state.cart[p['id']]

    with col2:
        st.subheader(T["cart_title"])
        total_price = 0
        items_for_mail = []
        
        # Prikaz sadržaja košarice
        if not st.session_state.cart:
            st.info(T["cart_empty"])
        else:
            for pid, q in st.session_state.cart.items():
                p_data = next(x for x in PRODUCTS if x['id'] == pid)
                sub = q * p_data['price']
                total_price += sub
                st.write(f"✅ **{T.get(pid, pid)}**: {q} {T['unit_'+p_data['unit']]} = {sub:.2f} €")
                items_for_mail.append({'name': T.get(pid, pid), 'qty': q, 'unit': T['unit_'+p_data['unit']]})
        
        st.divider()
        
        # INFORMATIVNI IZNOS (Uvijek vidljiv)
        st.markdown(f"### {T['total']}: <span style='color:#d32f2f'>{total_price:.2f} €</span>", unsafe_allow_html=True)
        
        # UOKVIRENA I OBOJANA NAPOMENA
        st.markdown(f"""
            <div style="border: 2px solid #e0e0e0; border-left: 5px solid #d32f2f; padding: 15px; background-color: #fff5f5; border-radius: 5px;">
                <p style="color: #b71c1c; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    {T['note_vaga']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Razmak
        
        # STALNO VIDLJIVA FORMA ZA DOSTAVU
        with st.form("order_form"):
            st.write(f"✍️ **{T['shipping_info']}**")
            n = st.text_input(T["form_name"])
            t = st.text_input(T["form_tel"])
            a = st.text_input(T["form_addr"])
            c = st.text_input(T["form_city"])
            z = st.text_input(T["form_zip"])
            co = st.text_input(T["form_country"])
            
            submit = st.form_submit_button(T["btn_order"])
            if submit:
                if not st.session_state.cart:
                    st.error(T["cart_empty"])
                elif n and t and a:
                    if send_email({'name':n,'tel':t,'addr':a,'city':c,'total':total_price}, items_for_mail, lang_choice):
                        st.success(T["success"])
                        st.session_state.cart = {}
                        for p in PRODUCTS: 
                            if f"state_{p['id']}" in st.session_state: st.session_state[f"state_{p['id']}"] = 0.0
                        time.sleep(2); st.rerun()
                else:
                    st.warning("Molimo ispunite obavezna polja (*)")

elif menu == T["nav_horeca"]: st.header(T["horeca_title"])
elif menu == T["nav_haccp"]: st.header(T["haccp_title"])
elif menu == T["nav_info"]: st.header(T["info_title"])
