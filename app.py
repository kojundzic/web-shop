import streamlit as st
import smtplib
import time
from email.mime.text import MIMEText
from dataclasses import dataclass
from datetime import datetime

# --- INTERNA KONFIGURACIJA ---
@dataclass(frozen=True)
class AppConfig:
    EMAIL: str = "tomislavtomi90@gmail.com"
    PASS: str = "czdx ndpg owzy wgqu"  # Koristi Google App Password
    SERVER: str = "smtp.gmail.com"
    PORT: int = 587
    THEME_COLOR: str = "#800000"  # Deep Crimson
    SECONDARY_COLOR: str = "#1E1E1E" # Charcoal Dark

CONFIG = AppConfig()

PRODUCTS = {
    "Dimljeni hamburger": {"icon": "🥓", "desc": "Sušen na bukovom drvetu."},
    "Dimljeni buncek": {"icon": "🍖", "desc": "Tradicionalna receptura."},
    "Slavonska kobasica": {"icon": "🌭", "desc": "Domaća paprika i meso."},
    "Domaći čvarci": {"icon": "🍿", "desc": "Topljeni na starinski način."},
    "Panceta": {"icon": "🥓", "desc": "Dugo zrenje, vrhunska aroma."},
    "Svinjska mast": {"icon": "🥣", "desc": "Čista, bez aditiva."},
    "Dimljena glava": {"icon": "🐷", "desc": "Tradicionalna delikatesa."}
}

# --- STYLING (Premium Visuals) ---
def apply_styles():
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #fdfdfd; }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
        
        .hero-section {{
            background: linear-gradient(135deg, {CONFIG.THEME_COLOR} 0%, {CONFIG.SECONDARY_COLOR} 100%);
            padding: 4rem 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}
        
        .product-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid #eee;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: 0.3s;
            text-align: center;
            height: 220px;
        }}
        
        .product-card:hover {{
            border-color: {CONFIG.THEME_COLOR};
            transform: translateY(-5px);
        }}

        .stButton>button {{
            background-color: {CONFIG.THEME_COLOR};
            color: white;
            border-radius: 10px;
            border: none;
            width: 100%;
            height: 45px;
            font-weight: bold;
            transition: 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: {CONFIG.SECONDARY_COLOR};
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        [data-testid="stSidebar"] {{
            background-color: {CONFIG.SECONDARY_COLOR};
            color: white;
        }}
        .stMarkdown p {{ font-size: 1.05rem; }}
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
class OrderService:
    @staticmethod
    def send_notification(user, cart):
        try:
            items_str = "\n".join([f"🥩 {k}: {v}kg" for k, v in cart.items()])
            body = (f"NARUDŽBA - MESNICA KOJUNDŽIĆ 2026\n\n"
                    f"KUPAC: {user['name']}\n"
                    f"TEL: {user['tel']}\n"
                    f"ADRESA: {user['addr']}\n\n"
                    f"STAVKE:\n{items_str}\n\n"
                    f"Vrijeme: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            msg = MIMEText(body)
            msg['Subject'] = f"🔥 Nova narudžba: {user['name']}"
            msg['From'] = CONFIG.EMAIL
            msg['To'] = CONFIG.EMAIL

            with smtplib.SMTP(CONFIG.SERVER, CONFIG.PORT, timeout=12) as server:
                server.starttls()
                server.login(CONFIG.EMAIL, CONFIG.PASS)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False

# --- UI RENDERER ---
def main():
    st.set_page_config(page_title="Kojundžić Premium", page_icon="🥩", layout="wide")
    apply_styles()

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    # Hero
    st.markdown(f"""
    <div class="hero-section">
        <h1 style="color: white; font-size: 3.5rem; margin-bottom: 0;">KOJUNDŽIĆ</h1>
        <p style="font-size: 1.5rem; opacity: 0.9;">Premium Butchery • Sisak 2026</p>
        <hr style="width: 100px; margin: 20px auto; border-color: rgba(255,255,255,0.3);">
        <p>Vrhunsko domaće meso, dimljeno po tradiciji naših starih.</p>
    </div>
    """, unsafe_allow_html=True)

    # Katalog
    st.markdown("## 🛒 Naša ponuda")
    cols = st.columns(4)
    
    for i, (name, details) in enumerate(PRODUCTS.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="product-card">
                <span style="font-size: 3rem;">{details['icon']}</span>
                <h3 style="margin-top: 10px;">{name}</h3>
                <p style="color: #666; font-size: 0.9rem;">{details['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            qty = st.number_input("Odaberi kg", 0.0, 100.0, step=0.5, key=f"qty_{name}")
            if st.button(f"Dodaj u narudžbu", key=f"btn_{name}"):
                if qty > 0:
                    st.session_state.cart[name] = qty
                    st.toast(f"✅ Dodano: {name} ({qty} kg)")
                else:
                    st.error("Unesite količinu!")

    # Sidebar (Košarica)
    with st.sidebar:
        st.markdown("# 🧺 Vaša košarica")
        if not st.session_state.cart:
            st.info("Vaša košarica je trenutno prazna.")
        else:
            total_items = 0
            for item, weight in list(st.session_state.cart.items()):
                st.markdown(f"**{item}**")
                st.write(f"⚖️ {weight} kg")
                total_items += 1
            
            if st.button("🗑️ Isprazni sve", use_container_width=True):
                st.session_state.cart = {}
                st.rerun()

            st.divider()
            st.markdown("### 🚚 Podaci za dostavu")
            with st.form("checkout_form"):
                u_name = st.text_input("Ime i prezime*")
                u_tel = st.text_input("Kontakt mobitel*")
                u_addr = st.text_area("Adresa za dostavu*")
                
                submitted = st.form_submit_button("ZAKLJUČI NARUDŽBU", use_container_width=True)
                
                if submitted:
                    if all([u_name, u_tel, u_addr]) and st.session_state.cart:
                        with st.spinner("Šaljemo vašu narudžbu..."):
                            user_data = {"name": u_name, "tel": u_tel, "addr": u_addr}
                            if OrderService.send_notification(user_data, st.session_state.cart):
                                st.balloons()
                                st.success("Narudžba uspješno poslana! Javit ćemo Vam se ubrzo.")
                                st.session_state.cart = {}
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Došlo je do greške pri slanju maila. Provjerite internet vezu.")
                    else:
                        st.warning("Popunite sva polja i osigurajte da košarica nije prazna.")

if __name__ == "__main__":
    main()
