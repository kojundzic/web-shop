import streamlit as st
import streamlit.components.v1 as components
import time

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - VERIFICIRANA FINALNA VERZIJA
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica i prerada mesa", 
    page_icon="🥩", 
    layout="wide"
)

# --- CUSTOM CSS ZA MODAL I STILIZACIJU ---
st.markdown("""
    <style>
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.85); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 15cm; height: 10cm; background-color: white; 
        border: 10px solid #28a745; border-radius: 40px; 
        display: flex; flex-direction: column; justify-content: center; 
        align-items: center; text-align: center; padding: 30px;
    }
    .success-text { color: #28a745; font-size: 42px; font-weight: bold; line-height: 1.2; }
    .qty-display { text-align: center; font-size: 1.3rem; font-weight: bold; padding-top: 5px; color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# --- PODACI O PROIZVODIMA ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"}
}

# --- DINAMIČKI EU PODACI ---
EU_DATA = {
    "Hrvatska": ["Sisak", "Zagreb", "Split", "Rijeka", "Osijek", "Zadar", "Varaždin", "Petrinja", "Kutina", "Popovača"],
    "Austrija": ["Beč (Wien)", "Salzburg", "Graz", "Linz", "Innsbruck", "Klagenfurt"],
    "Njemačka": ["Berlin", "München", "Hamburg", "Frankfurt", "Stuttgart", "Köln", "Düsseldorf"],
    "Slovenija": ["Ljubljana", "Maribor", "Celje", "Kranj", "Velenje", "Koper"],
    "Italija": ["Rim", "Milano", "Venecija", "Napulj", "Torino", "Firenca"]
}
SVE_EU_DRZAVE = sorted(["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Bugarska", "Cipar", "Danska", "Estonija", "Finska", "Grčka", "Irska", "Latvija", "Litva", "Luksemburg", "Malta", "Nizozemska", "Portugal", "Rumunjska", "Slovačka", "Španjolska", "Švedska"])

# --- JEZIČNI PAKETI ---
LANG = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_ug": "🏨 ZA UGOSTITELJE", "nav_dob": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title": "KOJUNDŽIĆ | Tradicija koja se okusi",
        "cart_title": "🛒 KOŠARICA", "total_label": "Informativni iznos narudžbe",
        "weight_note": "### ⚖️ Važna napomena o obračunu\nIstaknute cijene po jedinici mjere su točne i fiksne. Međutim, s obzirom na to da su naši proizvodi plod prirodnog uzgoja i tradicionalne ručne obrade, konačan iznos računa bit će utvrđen tek u trenutku preciznog vaganja paketa. Naš tim će uložiti maksimalan trud da isporučena količina bude što bliža Vašem zahtjevu i informativnom iznosu koji vidite u košarici.",
        "form_title": "🚚 PODACI ZA DOSTAVU", "f_name": "Ime*", "f_lname": "Prezime*", "f_country": "Država EU*", "f_city": "Grad*", "f_zip": "Poštanski broj*", "f_addr": "Adresa i kućni broj*", "f_phone": "Broj mobitela*",
        "btn_order": "🚀 POŠALJI NARUDŽBU", "success_msg": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!",
        "err_cart": "Košarica ne smije biti prazna!", "err_form": "Popunite sve podatke za dostavu!",
        "about_txt": "### Obiteljska tradicija i vizija kvalitete\nDobrodošli u Mesnicu Kojundžić, mjesto gdje se strast prema vrhunskom mesu prenosi generacijama. Smješteni u Sisku, ponosni smo na očuvanje autentičnih okusa uz primjenu najmodernijih standarda higijene i obrade. Naša priča je priča o očuvanju sisačkog kraja i povratku mirisa prave domaće kuhinje u svaki dom.",
        "dob_txt": "### Partnerstvo s lokalnim OPG-ovima\nVjerujemo u podršku lokalnoj zajednici i održivi razvoj hrvatskog sela. Naši dobavljači su isključivo probrani obiteljski poljoprivredni obrtnici iz Sisačko-moslavačke županije. Svaki komad mesa prolazi rigoroznu selekciju kako bismo osigurali da je stoka hranjena prirodno i bez GMO dodataka.",
        "haccp_txt": "### Sigurnost hrane bez kompromisa (HACCP)\nNaš pogon implementira vrhunski HACCP sustav koji jamči maksimalnu higijenu u svakoj sekundi proizvodnje. Od ulaza sirovine do vakuumiranja i transporta, svaki korak je digitalno nadziran i usklađen s najstrožim EU regulativama o zdravstvenoj ispravnosti hrane.",
        "ugostitelji_txt": "### Ekskluzivna ponuda za ugostiteljske objekte\nNudimo specijalizirani asortiman za restorane, hotele i catering službe koje ne pristaju na kompromise. Uz personaliziranu uslugu rezanja mesa, dry-age zrenje i prioritetnu dostavu u ranim jutarnjim satima, osiguravamo da Vaša kuhinja raspolaže najboljim hrvatskim namirnicama."
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_ug": "🏨 FOR CHEFS", "nav_dob": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title": "KOJUNDŽIĆ | Taste the Tradition",
        "cart_title": "🛒 SHOPPING CART", "total_label": "Informative Order Total",
        "weight_note": "### ⚖️ Important Billing Note\nThe unit prices shown are fixed and accurate. However, as our products are natural and manually processed, the final invoice amount will be determined at the time of precise weighing. We will make every effort to ensure the quantity is as close as possible to your request and the informative total in your cart.",
        "form_title": "🚚 DELIVERY DETAILS", "f_name": "First Name*", "f_lname": "Last Name*", "f_country": "EU Country*", "f_city": "City*", "f_zip": "ZIP Code*", "f_addr": "Address & House Number*", "f_phone": "Phone Number*",
        "btn_order": "🚀 PLACE ORDER", "success_msg": "YOUR ORDER HAS BEEN PLACED!<br><br>THANK YOU!",
        "err_cart": "Your cart must not be empty!", "err_form": "Please fill in all delivery details!",
        "about_txt": "### Family Tradition and Vision\nWelcome to Kojundžić Butchers, where passion for premium meat is passed down through generations. Based in Sisak, we preserve authentic flavors while applying the highest modern standards of processing.",
        "dob_txt": "### Local Supplier Partnership\nWe believe in supporting the local community. Our suppliers are exclusively selected family farms from the Sisak-Moslavina region, guaranteeing natural and GMO-free feeding.",
        "haccp_txt": "### Food Safety (HACCP)\nOur facility implements the HACCP system, ensuring maximum hygiene at every stage of production, from raw material intake to packaging, in full compliance with EU health standards.",
        "ugostitelji_txt": "### Exclusive Offer for Professionals\nWe offer specialized assortments for restaurants, hotels, and catering. With custom cuts, dry-aging services, and priority delivery, we ensure your kitchen has the best Croatian ingredients."
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_ug": "🏨 GASTRONOMIE", "nav_dob": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title": "KOJUNDŽIĆ | Tradition pur",
        "cart_title": "🛒 WARENKORB", "total_label": "Informativer Gesamtbetrag",
        "weight_note": "### ⚖️ Wichtiger Hinweis zur Abrechnung\nDie angegebenen Einzelpreise sind fest und korrekt. Da es sich um handverarbeitete Naturprodukte handelt, wird der endgültige Betrag erst bei der Verwiegung ermittelt. Wir bemühen uns, das Gewicht so nah wie möglich an Ihre Bestellung anzupassen.",
        "form_title": "🚚 LIEFERDATEN", "f_name": "Vorname*", "f_lname": "Nachname*", "f_country": "EU-Land*", "f_city": "Stadt*", "f_zip": "Postleitzahl*", "f_addr": "Adresse & Hausnummer*", "f_phone": "Telefonnummer*",
        "btn_order": "🚀 BESTELLEN", "success_msg": "BESTELLUNG ERFOLGREICH!<br><br>DANKE!",
        "err_cart": "Warenkorb leer!", "err_form": "Lieferdaten ausfüllen!",
        "about_txt": "### Familientradition\nWillkommen in der Metzgerei Kojundžić in Sisak. Wir pflegen authentische Aromen unter modernsten Standards der Fleischverarbeitung.",
        "dob_txt": "### Lokale Lieferanten\nWir unterstützen lokale Familienbetriebe. Unsere Lieferanten garantieren natürliche, gentechnikfreie Fütterung.",
        "haccp_txt": "### Sicherheit (HACCP)\nUnser Betrieb arbeitet nach dem HACCP-System für maximale Hygiene und EU-Gesundheitsstandards.",
        "ugostitelji_txt": "### Gastronomie-Service\nMaßgeschneiderte Schnitte, Dry-Aging und prioritäre Lieferung für Profis in Restaurants und Hotels."
    }
}

# --- INITIALIZATION ---
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

sel_lang = st.sidebar.selectbox("🌍 JEZIK / LANGUAGE", list(LANG.keys()))
L = LANG[sel_lang]

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f"""<div class="success-overlay"><div class="success-modal"><div class="success-text">{L['success_msg']}</div></div></div>""", unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.order_done = False
    st.session_state.cart = {}
    st.rerun()

# --- UI HEADER ---
st.title(L["title"])
st.markdown("---")

# --- NAVIGATION TABS ---
t_info, t_dob, t_haccp, t_ug = st.tabs([L["nav_info"], L["nav_dob"], L["nav_haccp"], L["nav_ug"]])
with t_info: st.markdown(L["about_txt"])
with t_dob: st.markdown(L["dob_txt"])
with t_haccp: st.markdown(L["haccp_txt"])
with t_ug: st.markdown(L["ugostitelji_txt"])

st.markdown("---")

# --- MAIN LAYOUT ---
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
                        st.write(f"**{info['cijena']:.2f} € / {jed}**")
                        
                        # LOGIKA GUMBA: MINUS | KOLICINA | PLUS
                        c_min, c_qty, c_plus = st.columns([1, 2, 1])
                        
                        with c_min:
                            if st.button("➖", key=f"min_{naziv}", use_container_width=True):
                                if naziv in st.session_state.cart:
                                    curr = st.session_state.cart[naziv]
                                    step = 0.5 if jed == "kg" else 1.0
                                    if curr <= step: del st.session_state.cart[naziv]
                                    else: st.session_state.cart[naziv] -= step
                                    st.rerun()
                        
                        with c_qty:
                            q_val = st.session_state.cart.get(naziv, 0.0)
                            display_q = f"{int(q_val) if q_val.is_integer() else q_val} {jed}" if q_val > 0 else "0"
                            st.markdown(f'<div class="qty-display">{display_q}</div>', unsafe_allow_html=True)
                            
                        with c_plus:
                            if st.button("➕", key=f"plus_{naziv}", use_container_width=True):
                                curr = st.session_state.cart.get(naziv, 0.0)
                                if jed == "kg":
                                    st.session_state.cart[naziv] = 1.0 if curr == 0 else curr + 0.5
                                else:
                                    st.session_state.cart[naziv] = curr + 1.0
                                st.rerun()

with col_kosarica:
    st.header(L["cart_title"])
    
    # 1. Shopping Cart Summary
    inf_total = 0
    if not st.session_state.cart:
        st.warning(L["err_cart"])
    else:
        for it, q in st.session_state.cart.items():
            sub = q * PROIZVODI[it]["cijena"]
            inf_total += sub
            st.write(f"🥩 **{it}** ({int(q) if q.is_integer() else q} {PROIZVODI[it]['jedinica']}) = {sub:.2f} €")
        st.markdown(f"### {L['total_label']}: {inf_total:.2f} €")
    
    st.info(L["weight_note"])
    st.divider()
    
    # 2. Delivery Form
    st.header(L["form_title"])
    f_ime = st.text_input(L["f_name"])
    f_prezime = st.text_input(L["f_lname"])
    
    # Dynamic Country/City Selection
    f_drzava = st.selectbox(L["f_country"], SVE_EU_DRZAVE)
    ponudeni_gradovi = EU_DATA.get(f_drzava, ["Ostalo (Manual entry)"])
    if "Ostalo (Manual entry)" not in ponudeni_gradovi: ponudeni_gradovi.append("Ostalo (Manual entry)")
    f_grad_sel = st.selectbox(L["f_city"], ponudeni_gradovi)
    
    if "Ostalo" in f_grad_sel:
        f_grad = st.text_input(f"{L['f_city']} (Input)*")
    else:
        f_grad = f_grad_sel
        
    f_zip = st.text_input(L["f_zip"])
    f_adr = st.text_input(L["f_addr"])
    f_mob = st.text_input(L["f_phone"])

    # Validation Logic
    form_ok = all([f_ime, f_prezime, f_grad, f_zip, f_adr, f_mob])
    cart_ok = len(st.session_state.cart) > 0

    if not cart_ok: st.error(L["err_cart"])
    elif not form_ok: st.error(L["err_form"])

    # Order Button
    if st.button(L["btn_order"], type="primary", use_container_width=True, disabled=not (form_ok and cart_ok)):
        st.session_state.order_done = True
        st.rerun()

# --- MAP SECTION ---
st.divider()
st.markdown("### 📍 Kojundžić Sisak")
components.html('<iframe src="https://www.google.com" width="100%" height="400" style="border:0; border-radius:15px;"></iframe>', height=420)
