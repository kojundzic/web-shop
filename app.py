import streamlit as st
import streamlit.components.v1 as components

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - FINALNA PRO VERZIJA
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica", 
    page_icon="🥩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEFINICIJA PROIZVODA I LOGIKE MJERNIH JEDINICA ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Domaća mast": {"cijena": 10.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"},
    "Domaći kulen": {"cijena": 25.00, "jedinica": "kom"}
}

# --- VIŠEJEZIČNI RJEČNIK ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ SIGURNOST", "nav_info": "📍 O NAMA",
        "title": "KOJUNDŽIĆ | Tradicija koja se okusi",
        "subtitle": "Vrhunska prerada mesa iz Siska • Od 2026.",
        "price": "Cijena", "unit_kg": "kg", "unit_kom": "kom", "in_cart": "U košarici",
        "cart_title": "🛒 Vaša košarica", "info_total": "Informativni iznos", "btn_order": "🚀 POŠALJI NARUDŽBU",
        "weight_note": "### ⚖️ Važna napomena o iznosu\nIstaknute cijene po jedinici mjere su **točne i fiksne**. Međutim, s obzirom na to da su naši proizvodi plod prirodnog uzgoja i ručne obrade, **konačan iznos računa** bit će utvrđen u trenutku pakiranja i dostave. Naš tim će se maksimalno potruditi da isporučena količina bude što bliža Vašoj traženoj količini i informativnom iznosu koji vidite u košarici.",
        "form_title": "📍 PODACI ZA DOSTAVU", "f_name": "Ime", "f_lname": "Prezime", "f_country": "Država", "f_city": "Grad", "f_addr": "Adresa", "f_zip": "Poštanski broj", "f_phone": "Broj mobitela",
        "success": "### ✅ Narudžba zaprimljena!", "thanks": "Hvala Vam na povjerenju! Naš tim će Vas kontaktirati za potvrdu točnog iznosa i termina dostave.",
        "countries": ["Hrvatska 🇭🇷", "Austrija 🇦🇹", "Njemačka 🇩🇪", "Slovenija 🇸🇮"],
        "cities": ["Sisak", "Petrinja", "Zagreb", "Velika Gorica", "Kutina", "Popovača", "Ostalo..."]
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ SAFETY", "nav_info": "📍 ABOUT US",
        "title": "KOJUNDŽIĆ | Taste the Tradition",
        "subtitle": "Premium meat processing from Sisak • Since 2026.",
        "price": "Price", "unit_kg": "kg", "unit_kom": "pc", "in_cart": "In cart",
        "cart_title": "🛒 Your Cart", "info_total": "Informative Total", "btn_order": "🚀 PLACE ORDER",
        "weight_note": "### ⚖️ Important Weight Notice\nThe unit prices shown are **accurate and fixed**. However, as our products are naturally raised and manually processed, the **final invoice amount** will be determined at the time of packaging and delivery. We will do our absolute best to ensure the delivered quantity is as close as possible to your requested amount and the informative total shown in your cart.",
        "form_title": "📍 DELIVERY DETAILS", "f_name": "First Name", "f_lname": "Last Name", "f_country": "Country", "f_city": "City", "f_addr": "Address", "f_zip": "ZIP Code", "f_phone": "Phone Number",
        "success": "### ✅ Order received!", "thanks": "Thank you! Our team will contact you to confirm the exact amount and delivery time.",
        "countries": ["Croatia 🇭🇷", "Austria 🇦🇹", "Germany 🇩🇪", "Slovenia 🇸🇮"],
        "cities": ["Sisak", "Petrinja", "Zagreb", "Velika Gorica", "Kutina", "Popovača", "Other..."]
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ SCHUTZ", "nav_info": "📍 ÜBER UNS",
        "title": "KOJUNDŽIĆ | Tradition, die man schmeckt",
        "subtitle": "Premium-Fleischverarbeitung aus Sisak • Seit 2026.",
        "price": "Preis", "unit_kg": "kg", "unit_kom": "stk", "in_cart": "Im Korb",
        "cart_title": "🛒 Ihr Warenkorb", "info_total": "Informativer Gesamtbetrag", "btn_order": "🚀 BESTELLEN",
        "weight_note": "### ⚖️ Wichtiger Hinweis zum Gewicht\nDie angegebenen Einzelpreise sind **fest und korrekt**. Da unsere Produkte jedoch naturbelassen und handverarbeitet sind, wird der **endgültige Rechnungsbetrag** erst bei Verpackung und Lieferung feststehen. Wir bemühen uns, die gelieferte Menge so nah wie möglich an Ihre Bestellung und den informativen Betrag im Warenkorb anzupassen.",
        "form_title": "📍 LIEFERDATEN", "f_name": "Vorname", "f_lname": "Nachname", "f_country": "Land", "f_city": "Stadt", "f_addr": "Adresse", "f_zip": "Postleitzahl", "f_phone": "Telefonnummer",
        "success": "### ✅ Bestellung erhalten!", "thanks": "Vielen Dank! Unser Team wird Sie kontaktieren, um den genauen Betrag und Liefertermin zu bestätigen.",
        "countries": ["Kroatien 🇭🇷", "Österreich 🇦🇹", "Deutschland 🇩🇪", "Slowenien 🇸🇮"],
        "cities": ["Sisak", "Petrinja", "Zagreb", "Velika Gorica", "Kutina", "Popovača", "Andere..."]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com", width=80)
    sel_lang = st.selectbox("🌍 JEZIK / LANGUAGE", list(LANG.keys()))
    L = LANG[sel_lang]
    st.divider()
    st.write(f"📞 **Tel:** +385 44 123 456")
    st.write(f"📧 **Mail:** info@kojundzic-sisak.hr")

# --- INITIALIZE SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- TABS ---
t1, t2, t3, t4 = st.tabs([L["nav_shop"], L["nav_horeca"], L["nav_haccp"], L["nav_info"]])

# --- TAB 1: SHOP ---
with t1:
    st.title(L["title"])
    st.caption(L["subtitle"])
    
    # Grid prikaz proizvoda
    items = list(PROIZVODI.items())
    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(items):
                naziv, info = items[i+j]
                jedinica = info["jedinica"]
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"#### {naziv}")
                        st.write(f"{L['price']}: **{info['cijena']:.2f} €/{jedinica}**")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("➕", key=f"add_{naziv}", use_container_width=True):
                                trenutno = st.session_state.cart.get(naziv, 0.0)
                                if jedinica == "kg":
                                    st.session_state.cart[naziv] = 1.0 if trenutno == 0 else trenutno + 0.5
                                else:
                                    st.session_state.cart[naziv] = trenutno + 1.0
                                st.rerun()
                        with c2:
                            if st.button("➖", key=f"rem_{naziv}", use_container_width=True):
                                if naziv in st.session_state.cart:
                                    trenutno = st.session_state.cart[naziv]
                                    korak = 0.5 if jedinica == "kg" else 1.0
                                    if trenutno <= korak: del st.session_state.cart[naziv]
                                    else: st.session_state.cart[naziv] -= korak
                                    st.rerun()
                        
                        if naziv in st.session_state.cart:
                            val = st.session_state.cart[naziv]
                            oznaka = L["unit_kg"] if jedinica == "kg" else L["unit_kom"]
                            st.success(f"{L['in_cart']}: {int(val) if val.is_integer() else val} {oznaka}")

    st.divider()

    # --- KOŠARICA I OBRAČUN ---
    if st.session_state.cart:
        st.header(L["cart_title"])
        inf_total = 0
        for it, q in st.session_state.cart.items():
            sub = q * PROIZVODI[it]["cijena"]
            inf_total += sub
            u = L["unit_kg"] if PROIZVODI[it]["jedinica"] == "kg" else L["unit_kom"]
            st.write(f"🥩 **{it}** ({int(q) if q.is_integer() else q} {u}) = {sub:.2f} €")
        
        st.markdown(f"## {L['info_total']}: {inf_total:.2f} €")
        st.info(L["weight_note"])
        
        st.divider()

        # --- FORMA ZA DOSTAVU ---
        with st.form("detailed_order_form"):
            st.markdown(f"### {L['form_title']}")
            
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                ime = st.text_input(L["f_name"])
                drzava = st.selectbox(L["f_country"], L["countries"])
                adresa = st.text_input(L["f_addr"])
            with row1_col2:
                prezime = st.text_input(L["f_lname"])
                grad = st.selectbox(L["f_city"], L["cities"])
                p_broj = st.text_input(L["f_zip"])
            
            mobitel = st.text_input(L["f_phone"])
            
            submit = st.form_submit_button(L["btn_order"], type="primary", use_container_width=True)
            
            if submit:
                if ime and prezime and adresa and mobitel and p_broj:
                    st.balloons()
                    st.success(L["success"])
                    st.info(L["thanks"])
                    st.session_state.cart = {}
                else:
                    st.error("❌ Molimo popunite sva polja kako bismo mogli izvršiti dostavu.")

# --- OSTALE RUBRIKE ---
with t2:
    st.markdown("### HORECA & Wholesale")
    st.write("Specijalne ponude za restorane i hotele.")
with t3:
    st.markdown("### HACCP Sigurnost")
    st.write("Najviši standardi higijene i sljedivosti.")
with t4:
    col_text, col_map = st.columns(2)
    with col_text:
        st.markdown("### Kojundžić Sisak 2026")
        st.write("Generacije kvalitete i domaće obrade.")
    with col_map:
        st.markdown("📍 **Lokacija**")
        map_code = """
        <iframe src="https://www.google.com" width="100%" height="300" style="border:0; border-radius:15px;"></iframe>
        """
        components.html(map_code, height=350)
