import streamlit as st
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Final

# =================================================================
# 🌍 INTERNACIONALIZACIJA (I18N) - Svi jezici na jednom mjestu
# =================================================================
I18N: Final = {
    "HR 🇭🇷": {
        "nav": ["TRGOVINA", "O NAMA", "DOBAVLJAČI", "HACCP"],
        "hero_title": "MESNICA KOJUNDŽIĆ",
        "hero_sub": "Sisak 2026 | Obiteljska tradicija od 1990.",
        "cart_title": "VAŠA KOŠARICA",
        "order_btn": "ZAKLJUČI NARUDŽBU",
        "details_btn": "ℹ️ Detalji proizvoda",
        "note_placeholder": "Napomena za ovaj proizvod (npr. narezati tanje)",
        "comp_details": "MESNICA KOJUNDŽIĆ d.o.o. | OIB: 12345678901 | Sisak, Hrvatska",
        "haccp_info": "Certificirano prema HRN EN ISO 22000:2018. Sigurnost hrane je zajamčena.",
        "fields": ["Ime i Prezime*", "Kontakt Mobitel*", "Adresa Dostave*", "Opća napomena uz narudžbu"],
        "success": "Narudžba uspješno poslana! 🚀",
        "error": "Greška u sustavu. Pokušajte ponovno."
    },
    "EN 🇬🇧": {
        "nav": ["SHOP", "ABOUT US", "SUPPLIERS", "HACCP"],
        "hero_title": "KOJUNDŽIĆ BUTCHERY",
        "hero_sub": "Sisak 2026 | Family tradition since 1990.",
        "cart_title": "YOUR CART",
        "order_btn": "PLACE ORDER",
        "details_btn": "ℹ️ Product Details",
        "note_placeholder": "Item specific note (e.g., slice thin)",
        "comp_details": "KOJUNDŽIĆ BUTCHERY Ltd. | VAT: HR12345678901 | Sisak, Croatia",
        "haccp_info": "Certified according to HRN EN ISO 22000:2018. Food safety guaranteed.",
        "fields": ["Full Name*", "Mobile Number*", "Delivery Address*", "General order note"],
        "success": "Order successfully sent! 🚀",
        "error": "System error. Please try again."
    }
}

# =================================================================
# 🥩 DATA LAYER - Proizvodi, Dobavljači i Poduzeće
# =================================================================
PRODUCTS: Final = {
    "Dimljeni hamburger": {
        "icon": "🥓", "origin": "OPG Horvat", 
        "desc_hr": "Vrhunski svinjski hamburger, dimljen na suhoj bukovini 14 dana.",
        "desc_en": "Premium pork hamburger, smoked on dry beechwood for 14 days."
    },
    "Slavonska kobasica": {
        "icon": "🌭", "origin": "OPG Marić", 
        "desc_hr": "Tradicionalna kobasica s domaćom ljutom paprikom, bez konzervansa.",
        "desc_en": "Traditional sausage with homemade hot peppers, no preservatives."
    },
    "Domaći čvarci": {
        "icon": "🍿", "origin": "Vlastita proizvodnja", 
        "desc_hr": "Ručno topljeni u bakrenim kotlovima, hrskavi i zlatni.",
        "desc_en": "Hand-melted in copper kettles, crispy and golden."
    }
}

# =================================================================
# ⚙️ BUSINESS ENGINE - Logika narudžbi i slanja
# =================================================================
class OrderProcessor:
    @staticmethod
    def send_order(user_info: Dict[str, str], cart_data: Dict[str, Any]) -> bool:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            items_str = "\n".join([f"- {k}: {v['qty']}kg (Napomena: {v['note']})" for k, v in cart_data.items()])
            
            body = (f"NOVA NARUDŽBA - {timestamp}\n\n"
                    f"KLIJENT: {user_info['name']}\nTEL: {user_info['tel']}\nADRESA: {user_info['addr']}\n"
                    f"OPĆA NAPOMENA: {user_info['gen_note']}\n\n"
                    f"STAVKE:\n{items_str}")

            msg = MIMEText(body)
            msg['Subject'] = f"Narudžba 2026: {user_info['name']}"
            msg['From'] = msg['To'] = "tomislavtomi90@gmail.com"

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                server.starttls()
                server.login("tomislavtomi90@gmail.com", "czdx ndpg owzy wgqu")
                server.send_message(msg)
            return True
        except Exception:
            return False

# =================================================================
# 🖥️ UI LAYER - Streamlit profesionalno sučelje
# =================================================================
def main():
    st.set_page_config(page_title="Kojundžić Premium 2026", layout="wide", page_icon="🥩")

    # Jezik i Globalno stanje
    lang_choice = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", list(I18N.keys()))
    L = I18N[lang_choice]
    if "cart" not in st.session_state: st.session_state.cart = {}

    # Navigacija
    menu = st.sidebar.radio("NAV", L["nav"])

    if menu == L["nav"][0]: # SHOP
        st.title(f"🥩 {L['hero_title']}")
        st.markdown(f"*{L['hero_sub']}*")
        
        cols = st.columns(3)
        for i, (name, info) in enumerate(PRODUCTS.items()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(f"{info['icon']} {name}")
                    
                    # Skočni prozor (Popover) za detalje proizvoda
                    with st.popover(L["details_btn"]):
                        desc = info['desc_hr'] if "HR" in lang_choice else info['desc_en']
                        st.write(f"**Opis:** {desc}")
                        st.write(f"**Podrijetlo:** {info['origin']}")
                    
                    qty = st.number_input("Količina (kg)", 0.0, 50.0, step=0.5, key=f"q_{name}")
                    note = st.text_input(L["note_placeholder"], key=f"n_{name}")
                    
                    if st.button(f"Dodaj u košaricu", key=f"b_{name}", use_container_width=True):
                        if qty > 0:
                            st.session_state.cart[name] = {"qty": qty, "note": note}
                            st.toast(f"✅ {name} dodan!")

    elif menu == L["nav"][1]: # ABOUT US
        st.header(L["nav"][1])
        st.info(L["comp_details"])
        st.write("Generacijama smo posvećeni vrhunskoj obradi mesa. Naša vizija 2026. ostaje ista: domaće, čisto i dimljeno po starinski.")

    elif menu == L["nav"][2]: # SUPPLIERS
        st.header(L["nav"][2])
        for p, info in PRODUCTS.items():
            st.write(f"🛡️ **{p}** – Dobavljač: {info['origin']}")

    elif menu == L["nav"][3]: # HACCP
        st.header(L["nav"][3])
        st.success(L["haccp_info"])

    # --- SIDEBAR KOŠARICA & CHECKOUT ---
    with st.sidebar:
        st.divider()
        st.header(f"🛒 {L['cart_title']}")
        if not st.session_state.cart:
            st.write("Prazno.")
        else:
            for item, data in list(st.session_state.cart.items()):
                st.write(f"**{item}**: {data['qty']}kg")
                if data['note']: st.caption(f"Napomena: {data['note']}")
            
            if st.button("🗑️ Isprazni košaricu"):
                st.session_state.cart = {}; st.rerun()

            st.divider()
            with st.form("checkout"):
                u_name = st.text_input(L["fields"][0])
                u_tel = st.text_input(L["fields"][1])
                u_addr = st.text_area(L["fields"][2])
                u_note = st.text_area(L["fields"][3])
                
                if st.form_submit_button(L["order_btn"], use_container_width=True):
                    if all([u_name, u_tel, u_addr]) and st.session_state.cart:
                        user = {"name": u_name, "tel": u_tel, "addr": u_addr, "gen_note": u_note}
                        if OrderProcessor.send_order(user, st.session_state.cart):
                            st.success(L["success"])
                            st.session_state.cart = {}; st.balloons()
                        else: st.error(L["error"])
                    else: st.warning("Popunite obavezna polja!")

if __name__ == "__main__":
    main()
