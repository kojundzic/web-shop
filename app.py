import streamlit as st
import streamlit.components.v1 as components

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - VERIFICIRANA FINALNA VERZIJA
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica i prerada mesa", 
    page_icon="🥩", 
    layout="wide"
)

# --- PROIZVODI I JEDINICE ---
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

# --- RJEČNIK S OPŠIRNIM TEKSTOVIMA ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title": "KOJUNDŽIĆ | Tradicija koja se okusi",
        "price": "Cijena", "unit_kg": "kg", "unit_kom": "kom", "in_cart": "U košarici",
        "cart_title": "🛒 Vaša košarica", "info_total": "Informativni iznos", "btn_order": "🚀 POŠALJI NARUDŽBU",
        "weight_note": "### ⚖️ Važna napomena o obračunu i količini\nIstaknute cijene po jedinici mjere su **točne i fiksne**. Budući da su naši proizvodi plod prirodnog uzgoja i tradicionalne ručne obrade, **konačan iznos računa** bit će utvrđen tek u trenutku pakiranja. Naš tim će se maksimalno potruditi da isporučena količina bude što bliža Vašoj traženoj količini i informativnom iznosu u košarici.",
        "form_title": "📍 PODACI ZA DOSTAVU", "f_name": "Ime", "f_lname": "Prezime", "f_country": "Država", "f_city": "Grad", "f_addr": "Adresa", "f_zip": "Poštanski broj", "f_phone": "Broj mobitela",
        "success": "### ✅ Narudžba zaprimljena!", "thanks": "Hvala Vam. Kontaktirat ćemo Vas za potvrdu točnog iznosa i termina dostave.",
        "about_txt": "### Obiteljska tradicija\nMesnica Kojundžić u Sisku simbol je kvalitete od 2026. godine. Naša vizija je očuvanje autentičnih okusa uz primjenu najviših standarda današnjice. Svaki komad mesa plod je lokalnog rada i ljubavi prema zanatu.",
        "suppliers_txt": "### Naši Dobavljači\nSurađujemo isključivo s lokalnim OPG-ovima. Naša stoka boravi na otvorenim ispašama, hranjena prirodnim žitaricama bez GMO dodataka, što jamči vrhunsku nutritivnu vrijednost.",
        "haccp_txt": "### Sigurnost hrane\nNaš pogon implementira HACCP sustav. Od ulaza sirovine do transporta, svaki korak je digitalno nadziran kako bismo osigurali zdravstveno ispravne proizvode po EU standardima.",
        "ugostitelji_txt": "### Za Ugostitelje\nNudimo specijalizirani asortiman za restorane i hotele. Personalizirani rezovi, dry-age usluga i prioritetna dostava temelj su naše suradnje s chefovima.",
        "countries": ["Hrvatska 🇭🇷", "Austrija 🇦🇹", "Njemačka 🇩🇪", "Slovenija 🇸🇮"],
        "cities": ["Sisak", "Zagreb", "Petrinja", "Velika Gorica", "Kutina", "Popovača", "Ostalo..."]
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR CHEFS", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title": "KOJUNDŽIĆ | Quality Tradition",
        "price": "Price", "unit_kg": "kg", "unit_kom": "pc", "in_cart": "In cart",
        "cart_title": "🛒 Your Cart", "info_total": "Informative Total", "btn_order": "🚀 PLACE ORDER",
        "weight_note": "### ⚖️ Important Billing Note\nUnit prices are **fixed**. Due to manual processing, the **final amount** will be determined during packaging. We strive to match your requested weight as closely as possible.",
        "form_title": "📍 DELIVERY INFO", "f_name": "First Name", "f_lname": "Last Name", "f_country": "Country", "f_city": "City", "f_addr": "Address", "f_zip": "ZIP", "f_phone": "Phone",
        "success": "### ✅ Order received!", "thanks": "Thank you. We will contact you shortly to confirm the total amount and delivery time.",
        "about_txt": "### Family Tradition\nKojundžić Butchers in Sisak stands for quality. We preserve authentic flavors using modern processing standards and local livestock.",
        "suppliers_txt": "### Local Suppliers\nWe work exclusively with local family farms (OPG), ensuring GMO-free, natural feeding for all animals.",
        "haccp_txt": "### Food Safety\nOur Sisak facility is fully HACCP compliant, with digital monitoring at every stage of production to meet EU health standards.",
        "ugostitelji_txt": "### For Restaurants\nCustom cuts, dry-aging, and priority delivery for hospitality professionals. We guarantee stable prices and premium quality.",
        "countries": ["Croatia 🇭🇷", "Austria 🇦🇹", "Germany 🇩🇪", "Slovenia 🇸🇮"],
        "cities": ["Sisak", "Zagreb", "Petrinja", "Other..."]
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 GASTRONOMIE", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title": "KOJUNDŽIĆ | Echte Tradition",
        "price": "Preis", "unit_kg": "kg", "unit_kom": "stk", "in_cart": "Im Korb",
        "cart_title": "🛒 Warenkorb", "info_total": "Informativ Gesamt", "btn_order": "🚀 BESTELLEN",
        "weight_note": "### ⚖️ Wichtiger Hinweis\nDie Einzelpreise sind **fest**. Da unsere Produkte handverarbeitet sind, steht der **endgültige Betrag** erst bei Verpackung fest.",
        "form_title": "📍 LIEFERDATEN", "f_name": "Vorname", "f_lname": "Nachname", "f_country": "Land", "f_city": "Stadt", "f_addr": "Adresse", "f_zip": "PLZ", "f_phone": "Telefon",
        "success": "### ✅ Bestellung erhalten!", "thanks": "Vielen Dank. Wir kontaktieren Sie zur Bestätigung.",
        "about_txt": "### Unsere Tradition\nMetzgerei Kojundžić in Sisak steht für Qualität. Wir bewahren authentische Aromen durch moderne Verarbeitungsstandards.",
        "suppliers_txt": "### Lieferanten\nWir arbeiten nur mit lokalen Bauernhöfen zusammen, um GMO-freie und natürliche Fütterung zu garantieren.",
        "haccp_txt": "### Sicherheit\nUnser Betrieb arbeitet nach HACCP-Richtlinien, um höchste Hygiene und EU-Gesundheitsstandards zu gewährleisten.",
        "ugostitelji_txt": "### Gastronomie\nSpezialschnitte und prioritäre Lieferung für Restaurants. Wir garantieren stabile Preise und Qualität.",
        "countries": ["Kroatien 🇭🇷", "Österreich 🇦🇹", "Deutschland 🇩🇪", "Slowenien 🇸🇮"],
        "cities": ["Sisak", "Zagreb", "Petrinja", "Andere..."]
    }
}

# --- LOGIKA SESSION STATE-A ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- SIDEBAR ---
sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", list(LANG.keys()))
L = LANG[sel_lang]
st.sidebar.divider()
st.sidebar.write("📞 +385 44 123 456")
st.sidebar.write("📧 info@kojundzic-sisak.hr")

# --- INTERFEJS ---
st.title(L["title"])
tabs = st.tabs([L["nav_shop"], L["nav_horeca"], L["nav_suppliers"], L["nav_haccp"], L["nav_info"]])

# --- TRGOVINA ---
with tabs[0]:
    items = list(PROIZVODI.items())
    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(items):
                naziv, info = items[i+j]
                jed = info["jedinica"]
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"#### {naziv}")
                        st.write(f"{L['price']}: **{info['cijena']:.2f} €/{jed}**")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("➕", key=f"add_{naziv}", use_container_width=True):
                                curr = st.session_state.cart.get(naziv, 0.0)
                                if jed == "kg":
                                    st.session_state.cart[naziv] = 1.0 if curr == 0 else curr + 0.5
                                else:
                                    st.session_state.cart[naziv] = curr + 1.0
                                st.rerun()
                        with c2:
                            if st.button("➖", key=f"rem_{naziv}", use_container_width=True):
                                if naziv in st.session_state.cart:
                                    curr = st.session_state.cart[naziv]
                                    step = 0.5 if jed == "kg" else 1.0
                                    if curr <= step: del st.session_state.cart[naziv]
                                    else: st.session_state.cart[naziv] -= step
                                    st.rerun()
                        if naziv in st.session_state.cart:
                            val = st.session_state.cart[naziv]
                            st.success(f"{L['in_cart']}: {int(val) if val.is_integer() else val} {L['unit_kg'] if jed == 'kg' else L['unit_kom']}")

    st.divider()
    if st.session_state.cart:
        st.header(L["cart_title"])
        inf_total = sum(q * PROIZVODI[it]["cijena"] for it, q in st.session_state.cart.items())
        for it, q in st.session_state.cart.items():
            u = L["unit_kg"] if PROIZVODI[it]["jedinica"] == "kg" else L["unit_kom"]
            st.write(f"🥩 **{it}** ({int(q) if q.is_integer() else q}{u}) = **{q * PROIZVODI[it]['cijena']:.2f} €**")
        
        st.subheader(f"{L['info_total']}: {inf_total:.2f} €")
        st.info(L["weight_note"])
        
        st.divider()
        with st.form("detailed_order"):
            st.markdown(f"### {L['form_title']}")
            f1, f2 = st.columns(2)
            with f1:
                fn = st.text_input(L["f_name"])
                cty = st.selectbox(L["f_country"], L["countries"])
                city = st.selectbox(L["f_city"], L["cities"])
                adr = st.text_input(L["f_addr"])
            with f2:
                ln = st.text_input(L["f_lname"])
                zp = st.text_input(L["f_zip"])
                ph = st.text_input(L["f_phone"])
            
            if st.form_submit_button(L["btn_order"], type="primary", use_container_width=True):
                if fn and ln and adr and ph and zp:
                    st.balloons()
                    st.success(L["success"]); st.info(L["thanks"])
                    st.session_state.cart = {}
                else: st.error("❌ Popunite sva polja!")

# --- OSTALI TABOVI ---
with tabs[1]: st.markdown(L["ugostitelji_txt"])
with tabs[2]: st.markdown(L["suppliers_txt"])
with tabs[3]: st.markdown(L["haccp_txt"])
with tabs[4]: 
    st.markdown(L["about_txt"])
    st.markdown("### 📍 Sisak")
    components.html('<iframe src="https://www.google.com" width="100%" height="350" style="border:0; border-radius:15px;"></iframe>', height=400)
