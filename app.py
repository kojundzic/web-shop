import streamlit as st
import streamlit.components.v1 as components

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - ULTIMATE EDITION
# =================================================================

st.set_page_config(page_title="KOJUNDŽIĆ Mesnica", page_icon="🥩", layout="wide")

# --- DEFINICIJA PROIZVODA I LOGIKE ---
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
        "cart_title": "🛒 Vaša košarica", "total": "Ukupno za platiti", "btn_order": "🚀 POŠALJI NARUDŽBU",
        "form_title": "📍 PODACI ZA DOSTAVU", "name": "Ime i prezime", "address": "Adresa i grad", "phone": "Broj mobitela",
        "success": "### ✅ Narudžba zaprimljena!", "thanks": "Hvala Vam na povjerenju. Naš majstor mesar će Vas kontaktirati.",
        "note_vaga": "⚖️ Logika: Prvi klik na 'kg' dodaje 1kg, svaki sljedeći 0.5kg. 'Kom' ide po 1 komad.",
        "about_txt": "### Naša Priča\nObitelj Kojundžić generacijama čuva tajne tradicionalne prerade. Koristimo isključivo meso s lokalnih OPG-ova uz strogu kontrolu kvalitete.",
        "haccp_txt": "### Sigurnost Hrane\nNaš pogon u Sisku certificiran je po najnovijim HACCP standardima. Svaki komad mesa ima potpunu sljedivost od farme do Vašeg stola.",
        "horeca_txt": "### Za Restorane\nNudimo posebne rezove, zrenje mesa i stabilne cijene za naše partnere u ugostiteljstvu."
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ SAFETY", "nav_info": "📍 ABOUT US",
        "title": "KOJUNDŽIĆ | Taste the Tradition",
        "subtitle": "Premium meat processing from Sisak • Since 2026.",
        "price": "Price", "unit_kg": "kg", "unit_kom": "pc", "in_cart": "In cart",
        "cart_title": "🛒 Your Cart", "total": "Total Amount", "btn_order": "🚀 PLACE ORDER",
        "form_title": "📍 DELIVERY DETAILS", "name": "Full Name", "address": "Address & City", "phone": "Phone Number",
        "success": "### ✅ Order received!", "thanks": "Thank you! Our master butcher will contact you shortly.",
        "note_vaga": "⚖️ Logic: First click on 'kg' adds 1kg, then 0.5kg increments. Pieces go by 1 unit.",
        "about_txt": "### Our Story\nThe Kojundžić family has preserved traditional secrets for generations. We use local meat with strict quality control.",
        "haccp_txt": "### Food Safety\nOur facility in Sisak is HACCP certified. Full traceability from farm to your table.",
        "horeca_txt": "### For Restaurants\nWe offer special cuts, dry-aging, and wholesale pricing for our partners."
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_haccp": "🛡️ SCHUTZ", "nav_info": "📍 ÜBER UNS",
        "title": "KOJUNDŽIĆ | Tradition, die man schmeckt",
        "subtitle": "Premium-Fleischverarbeitung aus Sisak • Seit 2026.",
        "price": "Preis", "unit_kg": "kg", "unit_kom": "stk", "in_cart": "Im Korb",
        "cart_title": "🛒 Ihr Warenkorb", "total": "Gesamtbetrag", "btn_order": "🚀 BESTELLEN",
        "form_title": "📍 LIEFERDATEN", "name": "Name", "address": "Adresse", "phone": "Telefon",
        "success": "### ✅ Bestellung erhalten!", "thanks": "Vielen Dank! Unser Metzgermeister wird Sie kontaktieren.",
        "note_vaga": "⚖️ Logik: Erster Klick auf 'kg' fügt 1kg hinzu, dann 0,5kg Schritte.",
        "about_txt": "### Unsere Geschichte\nFamilie Kojundžić bewahrt seit Generationen die Geheimnisse der Fleischverarbeitung.",
        "haccp_txt": "### Sicherheit\nUnser Betrieb in Sisak ist HACCP-zertifiziert. Volle Rückverfolgbarkeit.",
        "horeca_txt": "### Gastronomie\nSpezialschnitte und Großhandelspreise für unsere Partner."
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com", width=80)
    sel_lang = st.selectbox("🌍 JEZIK / LANGUAGE", list(LANG.keys()))
    L = LANG[sel_lang]
    st.divider()
    st.write(f"📞 **Tel:** +385 44 123 456")
    st.write(f"📧 **Mail:** info@kojundzic.hr")

# --- HEADER ---
st.title(L["title"])
st.caption(L["subtitle"])

if 'cart' not in st.session_state:
    st.session_state.cart = {}

t1, t2, t3, t4 = st.tabs([L["nav_shop"], L["nav_horeca"], L["nav_haccp"], L["nav_info"]])

# --- TAB 1: SHOP (SMART LOGIC) ---
with t1:
    st.info(L["note_vaga"])
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
                            if st.button(f"➕", key=f"add_{naziv}", use_container_width=True):
                                trenutno = st.session_state.cart.get(naziv, 0.0)
                                if jedinica == "kg":
                                    st.session_state.cart[naziv] = 1.0 if trenutno == 0 else trenutno + 0.5
                                else:
                                    st.session_state.cart[naziv] = trenutno + 1.0
                                st.rerun()
                        with c2:
                            if st.button(f"➖", key=f"rem_{naziv}", use_container_width=True):
                                if naziv in st.session_state.cart:
                                    trenutno = st.session_state.cart[naziv]
                                    if jedinica == "kg":
                                        if trenutno <= 1.0: del st.session_state.cart[naziv]
                                        else: st.session_state.cart[naziv] = trenutno - 0.5
                                    else:
                                        if trenutno <= 1.0: del st.session_state.cart[naziv]
                                        else: st.session_state.cart[naziv] = trenutno - 1.0
                                    st.rerun()
                        
                        if naziv in st.session_state.cart:
                            val = st.session_state.cart[naziv]
                            oznaka = L["unit_kg"] if jedinica == "kg" else L["unit_kom"]
                            st.success(f"{L['in_cart']}: {int(val) if val.is_integer() else val} {oznaka}")

    st.divider()
    if st.session_state.cart:
        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader(L["cart_title"])
            ukupno = 0
            for k, v in st.session_state.cart.items():
                cijena = v * PROIZVODI[k]["cijena"]
                ukupno += cijena
                jed = L["unit_kg"] if PROIZVODI[k]["jedinica"] == "kg" else L["unit_kom"]
                st.write(f"🥩 {k} ({int(v) if v.is_integer() else v}{jed}) = **{cijena:.2f} €**")
            st.markdown(f"### {L['total']}: {ukupno:.2f} €")
        
        with c_right:
            with st.form("order_form"):
                st.markdown(f"### {L['form_title']}")
                ime = st.text_input(L["name"])
                adr = st.text_input(L["address"])
                mob = st.text_input(L["phone"])
                if st.form_submit_button(L["btn_order"], type="primary", use_container_width=True):
                    if ime and adr and mob:
                        st.balloons()
                        st.success(L["success"])
                        st.info(L["thanks"])
                        st.session_state.cart = {}
                    else: st.error("❌ Popunite polja!")

# --- TAB 2 & 3: TEKSTOVI ---
with t2: st.markdown(L["horeca_txt"])
with t3: st.markdown(L["haccp_txt"])

# --- TAB 4: O NAMA & MAPA ---
with t4:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(L["about_txt"])
    with col_b:
        st.markdown("### 📍 Lokacija Sisak")
        map_html = """
        <iframe src="https://www.google.com" 
        width="100%" height="350" style="border:0; border-radius:15px;" allowfullscreen="" loading="lazy"></iframe>
        """
        components.html(map_html, height=400)
