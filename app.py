import streamlit as st
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any

# =================================================================
# ⚙️ CONSTANTS & CONFIGURATION (React-like Config)
# =================================================================

CONFIG = {
    "EMAIL": "tomislavtomi90@gmail.com",
    "PASS": "czdx ndpg owzy wgqu",
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "YEAR": 2026
}

EU_COUNTRIES = ["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Mađarska", "Slovačka"]

# --- I18N DATA (Internationalization) ---
LANG_DATA = {
    "HR 🇭🇷": {
        "title": f"KOJUNDŽIĆ Mesnica | Sisak {CONFIG['YEAR']}.",
        "sections": ["🏬 TRGOVINA", "🏨 HORECA", "🛡️ HACCP", "ℹ️ O NAMA"],
        "cart": {"title": "🛒 Košarica", "empty": "Košarica je prazna.", "btn": "POŠALJI"},
        "fields": ["Ime*", "Prezime*", "Telefon*", "Adresa*"],
        "products": ["Dimljeni hamburger", "Dimljeni buncek", "Slavonska kobasica", "Domaći čvarci", "Panceta", "Svinjska mast", "Dimljena glava"]
    },
    "EN 🇬🇧": {
        "title": f"KOJUNDŽIĆ Butchery | Sisak {CONFIG['YEAR']}.",
        "sections": ["🏬 SHOP", "🏨 HORECA", "🛡️ HACCP", "ℹ️ ABOUT US"],
        "cart": {"title": "🛒 Cart", "empty": "Cart is empty.", "btn": "PLACE ORDER"},
        "fields": ["First Name*", "Last Name*", "Phone*", "Address*"],
        "products": ["Smoked Hamburger", "Smoked Pork Hock", "Slavonian Sausage", "Pork Rinds", "Pancetta", "Lard", "Smoked Pig Head"]
    }
}

# =================================================================
# 🛠️ BUSINESS LOGIC (Utility Functions / "Hooks")
# =================================================================

def send_order_email(user_data: Dict[str, str], cart_items: str) -> bool:
    """Side effect handler for sending emails."""
    try:
        msg_body = f"NARUDŽBA {CONFIG['YEAR']}\n\nKlijent: {user_data['name']}\nTel: {user_data['tel']}\nAdresa: {user_data['addr']}\n\nStavke:\n{cart_items}"
        msg = MIMEText(msg_body)
        msg['Subject'] = f"Nova narudžba: {user_data['name']}"
        msg['From'], msg['To'] = CONFIG['EMAIL'], CONFIG['EMAIL']

        with smtplib.SMTP(CONFIG['SMTP_SERVER'], CONFIG['SMTP_PORT']) as server:
            server.starttls()
            server.login(CONFIG['EMAIL'], CONFIG['PASS'])
            server.sendmail(CONFIG['EMAIL'], CONFIG['EMAIL'], msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send: {e}")
        return False

# =================================================================
# 🖥️ UI COMPONENTS (Streamlit Components)
# =================================================================

def render_store(lang: Dict[str, Any]):
    """Component for rendering the product grid."""
    st.title(lang["title"])
    cols = st.columns(3)
    for i, prod in enumerate(lang["products"]):
        with cols[i % 3]:
            st.subheader(prod)
            qty = st.number_input(f"kg", min_value=0.0, step=0.5, key=f"input_{prod}")
            if st.button(f"Add {prod}", key=f"btn_{prod}"):
                if qty > 0:
                    st.session_state.cart[prod] = qty
                    st.toast(f"✅ {prod} added!")

def render_sidebar_cart(lang: Dict[str, Any]):
    """Component for the sidebar cart and checkout."""
    st.sidebar.header(lang["cart"]["title"])
    
    if not st.session_state.cart:
        st.sidebar.info(lang["cart"]["empty"])
        return

    order_summary = ""
    for p, q in list(st.session_state.cart.items()):
        if q > 0:
            st.sidebar.write(f"🥩 **{p}**: {q} kg")
            order_summary += f"- {p}: {q} kg\n"
    
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state.cart = {}
        st.rerun()

    st.sidebar.divider()
    
    # --- Checkout Form (React-like Controlled Form) ---
    with st.sidebar.form("checkout_form"):
        fn = st.text_input(lang["fields"][0])
        ln = st.text_input(lang["fields"][1])
        tel = st.text_input(lang["fields"][2])
        adr = st.text_input(lang["fields"][3])
        
        if st.form_submit_button(lang["cart"]["btn"]):
            if all([fn, ln, tel, adr]):
                user_payload = {"name": f"{fn} {ln}", "tel": tel, "addr": adr}
                if send_order_email(user_payload, order_summary):
                    st.success("Order Shipped! 🚀")
                    st.session_state.cart = {}
                    st.balloons()
            else:
                st.sidebar.warning("Fill all required fields.")

# =================================================================
# 🚀 MAIN APP ENTRY POINT (Root Component)
# =================================================================

def main():
    st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")

    # Initial State initialization
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    # Language Selector (React Context-like behavior)
    selected_lang = st.sidebar.selectbox("🌍 Language", list(LANG_DATA.keys()))
    L = LANG_DATA[selected_lang]

    # Navigation Setup
    page = st.sidebar.radio("Navigation", L["sections"])

    # Component Routing
    if page == L["sections"][0]:
        render_store(L)
    elif page == L["sections"][1]:
        st.title(L["sections"][1])
        st.markdown("### HORECA Precision Cutting\nOptimized for hotels & restaurants.")
    elif page == L["sections"][2]:
        st.title(L["sections"][2])
        st.markdown("### HACCP Certified\nSafety first, quality always.")
    else:
        st.title(L["sections"][3])
        st.write("Family Kojundžić Tradition - Sisak 2026.")

    render_sidebar_cart(L)

if __name__ == "__main__":
    main()
