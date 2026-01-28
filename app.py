import streamlit as st
import streamlit.components.v1 as components
import time

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - FIXED PRESTIGE EDITION
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica i prerada mesa", 
    page_icon="🥩", 
    layout="wide"
)

# --- CUSTOM CSS ZA LUKSUZAN IZGLED I MODAL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');

    .main-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(to bottom, #ffffff, #fcfcfc);
        border-bottom: 2px solid #d32f2f;
        margin-bottom: 30px;
    }

    .luxury-title {
        font-family: 'Playfair Display', serif;
        font-size: 58px;
        font-weight: 900;
        color: #1a1a1a;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .luxury-subtitle {
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 300;
        color: #d32f2f;
        letter-spacing: 5px;
        text-transform: uppercase;
    }

    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.92); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 15cm; height: 10cm; background-color: white; 
        border: 10px solid #28a745; border-radius: 40px; 
        display: flex; flex-direction: column; justify-content: center; 
        align-items: center; text-align: center; padding: 30px;
    }
    .success-text { color: #28a745; font-size: 42px; font-weight: bold; font-family: 'Playfair Display', serif; }
    
    .qty-display { 
        text-align: center; font-size: 1.4rem; font-weight: bold; 
        color: #d32f2f; font-family: 'Lato', sans-serif; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- PODACI ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"}
}

EU_DATA = {
    "Hrvatska": ["Sisak", "Zagreb", "Split", "Rijeka", "Osijek", "Zadar", "Varaždin", "Petrinja", "Kutina", "Popovača"],
    "Austrija": ["Beč (Wien)", "Salzburg", "Graz", "Linz", "Innsbruck", "Klagenfurt"],
    "Njemačka": ["Berlin", "München", "Hamburg", "Frankfurt", "Stuttgart", "Köln", "Düsseldorf"],
    "Slovenija": ["Ljubljana", "Maribor", "Celje", "Kranj", "Velenje", "Koper"],
    "Italija": ["Rim", "Milano", "Venecija", "Napulj", "Torino", "Firenca"]
}
DRZAVE_LISTA = sorted(["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Bugarska", "Cipar", "Danska", "Estonija", "Finska", "Grčka", "Irska", "Latvija", "Litva", "Luksemburg", "Malta", "Nizozemska", "Portugal", "Rumunjska", "Slovačka", "Španjolska", "Švedska"])

LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_ug": "🏨 ZA UGOSTITELJE", "nav_dob": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA", "nav_lang": "🌍 JEZIK",
        "title": "KOJUNDŽIĆ", "subtitle": "MESNICA I PRERADA MESA SISAK",
        "cart_title": "🛒 KOŠARICA", "cart_empty_msg": "Vaša košarica je trenutno prazna.", "total_label": "Informativni iznos narudžbe",
        "weight_note": "### ⚖️ Važna napomena o obračunu\nIstaknute cijene su točne i fiksne. Konačan iznos računa saznat ćete pri dostavi.",
        "form_title": "🚚 PODACI ZA DOSTAVU", "f_name": "Ime*", "f_lname": "Prezime*", "f_country": "Država EU*", "f_city": "Grad*", "f_zip": "Poštanski broj*", "f_addr": "Adresa*", "f_phone": "Mobitel*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success_msg": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!",
        "err_cart": "Košarica je prazna!", "err_form": "Popunite podatke!",
        "about_txt": "### Obiteljska tradicija...\nNaša priča počinje u Sisku...",
        "dob_txt": "### Partnerstvo s OPG-ovima...",
        "haccp_txt": "### Sigurnost hrane...",
        "ugostitelji_txt": "### Za ugostitelje..."
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_ug": "🏨 FOR CHEFS", "nav_dob": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US", "nav_lang": "🌍 LANGUAGE",
        "title": "KOJUNDŽIĆ", "subtitle": "BUTCHERY & MEAT PROCESSING SISAK",
        "cart_title": "🛒 SHOPPING CART", "cart_empty_msg": "Your cart is currently empty.", "total_label": "Total Amount",
        "weight_note": "### ⚖️ Billing Note\nFinal amount determined at delivery.",
        "form_title": "🚚 DELIVERY DETAILS", "f_name": "First Name*", "f_lname": "Last Name*", "f_country": "Country*", "f_city": "City*", "f_zip": "ZIP*", "f_addr": "Address*", "f_phone": "Phone*",
        "btn_order": "🚀 PLACE ORDER", "success_msg": "ORDER PLACED!<br><br>THANK YOU!",
        "err_cart": "Cart empty!", "err_form": "Fill details!",
        "about_txt": "### Family Tradition...",
        "dob_txt": "### Suppliers...",
        "haccp_txt": "### Safety...",
        "ugostitelji_txt": "### For Chefs..."
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_ug": "🏨 GASTRONOMIE", "nav_dob": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS", "nav_lang": "🌍 SPRACHE",
        "title": "KOJUNDŽIĆ", "subtitle": "METZGEREI UND FLEISCHVERARBEITUNG SISAK",
        "cart_title": "🛒 WARENKORB", "cart_empty_msg": "Ihr Warenkorb ist derzeit leer.", "total_label": "Gesamtbetrag",
        "weight_note": "### ⚖️ Abrechnungshinweis\nEndgültiger Betrag bei Lieferung.",
        "form_title": "🚚 LIEFERDATEN", "f_name": "Vorname*", "f_lname": "Nachname*", "f_country": "Land*", "f_city": "Stadt*", "f_zip": "PLZ*", "f_addr": "Adresse*", "f_phone": "Telefon*",
        "btn_order": "🚀 BESTELLEN", "success_msg": "BESTELLUNG ERFOLGREICH!<br><br>DANKE!",
        "err_cart": "Korb leer!", "err_form": "Daten ausfüllen!",
        "about_txt": "### Tradition...",
        "dob_txt": "### Lieferanten...",
        "haccp_txt": "### Sicherheit...",
        "ugostitelji_txt": "### Gastronomie..."
    }
}

# --- INITIALIZATION ---
if 'lang' not in st.session_state: st.session_state.lang = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG[st.session_state.lang]

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f"""<div class="success-overlay"><div class="success-modal"><div class="success-text">{L['success_msg']}</div></div></div>""", unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.order_done = False
    st.session_state.cart = {}
    st.rerun()

# --- PRESTIGE HEADER ---
st.markdown(f"""<div class="main-header"><div class="luxury-title">{L['title']}</div><div class="luxury-subtitle">{L['subtitle']}</div></div>""", unsafe_allow_html=True)

# --- MAIN TABS ---
tabs = st.tabs([L["nav_shop"], L["nav_ug"], L["nav_dob"], L["nav_haccp"], L["nav_info"], L["nav_lang"]])

# --- SHOP ---
with tabs[0]:
    col_trgovina, col_kosarica = st.columns([1.4, 1], gap="large")
    with col_trgovina:
        st.header(L["nav_shop"])
        items = list(PROIZVODI.items())
        for i in range(0, len(items), 2):
            row_cols = st.columns(2)
            for j in range(2):
                if i + j < len(items):
                    naziv, info = items[i+j]
                    jed = info["jedinica"]
                    with row_cols[j]:
                        with st.container(border=True):
                            st.subheader(naziv)
                            st.write(f"Cijena: **{info['cijena']:.2f} € / {jed}**")
                            # POPRAVLJENO: Dodan broj 3 u st.columns(3)
                            c_min, c_qty, c_plus = st.columns(3)
                            with c_min:
                                if st.button("➖", key=f"min_{naziv}", use_container_width=True):
                                    if naziv in st.session_state.cart:
                                        curr = st.session_state.cart[naziv]
                                        step = 0.5 if jed == "kg" else 1.0
                                        if curr <= step: del st.session_state.cart[naziv]
                                        else: st.session_state.cart[naziv] -= step
                                        st.rerun()
                            with c_qty:
                                val = st.session_state.cart.get(naziv, 0.0)
                                q_txt = f"{int(val) if val.is_integer() else val} {jed}" if val > 0 else "0"
                                st.markdown(f'<div class="qty-display">{q_txt}</div>', unsafe_allow_html=True)
                            with c_plus:
                                if st.button("➕", key=f"plus_{naziv}", use_container_width=True):
                                    curr = st.session_state.cart.get(naziv, 0.0)
                                    st.session_state.cart[naziv] = 1.0 if curr == 0 and jed == "kg" else curr + (0.5 if jed == "kg" else 1.0)
                                    st.rerun()

    with col_kosarica:
        st.header(L["cart_title"])
        inf_total = 0
        if not st.session_state.cart:
            st.warning(L["cart_empty_msg"])
        else:
            for it, q in st.session_state.cart.items():
                sub = q * PROIZVODI[it]["cijena"]
                inf_total += sub
                st.write(f"🥩 **{it}** ({int(q) if q.is_integer() else q}{PROIZVODI[it]['jedinica']}) = {sub:.2f} €")
            st.markdown(f"### {L['total_label']}: {inf_total:.2f} €")
        
        st.info(L["weight_note"])
        st.divider()
        st.header(L["form_title"])
        f_i = st.text_input(L["f_name"])
        f_p = st.text_input(L["f_lname"])
        idx_hr = DRZAVE_LISTA.index("Hrvatska")
        f_d = st.selectbox(L["f_country"], DRZAVE_LISTA, index=idx_hr)
        
        gradovi = EU_DATA.get(f_d, [])
        f_g_sel = st.selectbox(L["f_city"], [""] + gradovi + ["Ostalo (Upiši ručno)"], index=0)
        f_g = st.text_input(f"{L['f_city']}*") if f_g_sel == "Ostalo (Upiši ručno)" else f_g_sel
        
        f_z = st.text_input(L["f_zip"])
        f_a = st.text_input(L["f_addr"])
        f_m = st.text_input(L["f_phone"])

        valid = all([f_i, f_p, f_g, f_z, f_a, f_m]) and f_g != "" and len(st.session_state.cart) > 0
        if st.button(L["btn_order"], type="primary", use_container_width=True, disabled=not valid):
            st.session_state.order_done = True
            st.rerun()

with tabs[1]: st.markdown(L["ugostitelji_txt"])
with tabs[2]: st.markdown(L["dob_txt"])
with tabs[3]: st.markdown(L["haccp_txt"])
with tabs[4]: 
    st.markdown(L["about_txt"])
    components.html('<iframe src="https://www.google.com" width="100%" height="350" style="border:0; border-radius:15px;"></iframe>', height=380)

with tabs[5]:
    st.header(L["nav_lang"])
    nova = st.radio("Select:", list(LANG.keys()), index=list(LANG.keys()).index(st.session_state.lang))
    if nova != st.session_state.lang:
        st.session_state.lang = nova
        st.rerun()
