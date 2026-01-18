import streamlit as st
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass
from datetime import datetime

# --- KONFIGURACIJA ---
CONFIG = {
    "EMAIL": "tomislavtomi90@gmail.com",
    "PASS": "czdx ndpg owzy wgqu",
    "SHOP_NAME": "KOJUNDŽIĆ",
    "LOCATION": "Sisak 2026",
    "THEME_COLOR": "#800000"  # Tamno crvena (boja mesa/tradicije)
}

# --- CUSTOM CSS (Za "Moćan" Izgled) ---
def apply_custom_style():
    st.markdown(f"""
    <style>
        /* Pozadina i fontovi */
        .stApp {{
            background-color: #f8f9fa;
        }}
        h1, h2, h3 {{
            color: {CONFIG['THEME_COLOR']};
            font-family: 'Playfair Display', serif;
            font-weight: 800;
        }}
        
        /* Premium Kartice Proizvoda */
        .product-card {{
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid {CONFIG['THEME_COLOR']};
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: transform 0.3s;
        }}
        .product-card:hover {{
            transform: translateY(-5px);
        }}
        
        /* Gumbi */
        .stButton>button {{
            background-color: {CONFIG['THEME_COLOR']};
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 2rem;
            font-weight: bold;
            width: 100%;
        }}
        .stButton>button:hover {{
            background-color: #a00000;
            border: none;
            color: white;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: #1a1a1a;
            color: white;
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{
            color: white;
        }}
    </style>
    """, unsafe_allow_status=True)

# --- POSLOVNA LOGIKA ---
@dataclass
class Order:
    user: dict
    items: dict
    
    def send_email(self):
        try:
            summary = "\n".join([f"🥩 {k}: {v}kg" for k, v in self.items.items()])
            body = f"NOVA PREMIUM NARUDŽBA\n\nKupac: {self.user['name']}\nTel: {self.user['tel']}\nAdresa: {self.user['addr']}\n\nStavke:\n{summary}"
            msg = MIMEText(body)
            msg['Subject'] = f"🔥 Narudžba: {self.user['name']}"
            msg['From'] = msg['To'] = CONFIG["EMAIL"]
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(CONFIG["EMAIL"], CONFIG["PASS"])
                server.send_message(msg)
            return True
        except: return False

# --- UI KOMPONENTE ---
def render_header():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("") # Ovdje bi išao logo
    with col2:
        st.title(f"👑 {CONFIG['SHOP_NAME']} | Premium Butchery")
        st.write(f"📍 {CONFIG['LOCATION']} | *Tradicija koja se osjeti u svakom zalogaju.*")
    st.divider()

def product_grid():
    products = {
        "Dimljeni hamburger": {"icon": "🥓", "desc": "Sušen na bukovom drvetu, savršen omjer mesa i masnoće."},
        "Dimljeni buncek": {"icon": "🍖", "desc": "Tradicionalna receptura, spreman za kuhanje."},
        "Slavonska kobasica": {"icon": "🌭", "desc": "Domaća paprika i birano meso iz domaćeg uzgoja."},
        "Domaći čvarci": {"icon": "🍿", "desc": "Hrskavi, topljeni na starinski način."},
        "Panceta": {"icon": "🥓", "desc": "Dugo zrenje, vrhunska aroma."},
        "Svinjska mast": {"icon": "🥣", "desc": "Čista, bijela, bez aditiva - kao kod bake."},
        "Dimljena glava": {"icon": "🐷", "desc": "Delikatesa za prave ljubitelje tradicije."}
    }

    st.subheader("🛒 Naša Ponuda")
    cols = st.columns(3)
    
    for i, (name, info) in enumerate(products.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <h3>{info['icon']} {name}</h3>
                <p style='color: #666; font-size: 0.9em;'>{info['desc']}</p>
            </div>
            """, unsafe_allow_status=True)
            
            qty = st.number_input("Količina (kg)", 0.0, 20.0, step=0.5, key=f"q_{name}")
            if st.button(f"Dodaj u košaricu", key=f"b_{name}"):
                if qty > 0:
                    st.session_state.cart[name] = qty
                    st.toast(f"✅ {name} dodan u košaricu!")

# --- GLAVNA APLIKACIJA ---
def main():
    st.set_page_config(page_title="Kojundžić Premium", page_icon="🥩", layout="wide")
    apply_custom_style()
    
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    render_header()
    
    # Hero sekcija
    st.markdown(f"""
    <div style="background-color: {CONFIG['THEME_COLOR']}; padding: 40px; border-radius: 20px; color: white; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; margin: 0;">DOMAĆE. DIMLJENO. VRHUNSKO.</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">Naručite direktno iz naše dimne komore do vašeg stola.</p>
    </div>
    """, unsafe_allow_status=True)

    product_grid()

    # Sidebar Checkout
    with st.sidebar:
        st.markdown("## 🛒 Vaša Seleksi")
        if not st.session_state.cart:
            st.info("Košarica je prazna. Odaberite najbolje od mesa.")
        else:
            for p, q in list(st.session_state.cart.items()):
                st.write(f"📍 **{p}**: {q} kg")
            
            if st.button("🗑️ Isprazni sve"):
                st.session_state.cart = {}
                st.rerun()
            
            st.divider()
            with st.form("checkout"):
                st.markdown("### 📋 Detalji Isporuke")
                u = {
                    "name": st.text_input("Ime i Prezime"),
                    "tel": st.text_input("Mobitel"),
                    "addr": st.text_area("Adresa dostave")
                }
                if st.form_submit_button("ZAVRŠI NARUDŽBU"):
                    if all(u.values()) and st.session_state.cart:
                        if Order(u, st.session_state.cart).send_email():
                            st.success("Narudžba primljena. Javit ćemo Vam se ubrzo! 🚀")
                            st.session_state.cart = {}
                            st.balloons()
                        else: st.error("Greška na serveru.")
                    else: st.warning("Molimo ispunite sva polja.")

if __name__ == "__main__":
    main()
