import streamlit as st
import smtplib
import time
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - FINAL MULTILINGUAL EDITION
# =================================================================

st.set_page_config(
    page_title="KOJUNDŽIĆ Mesnica i prerada mesa", 
    page_icon="🥩", 
    layout="wide"
)

# --- KONFIGURACIJA EMAILA ---
def posalji_email(predmet, poruka):
    try:
        primatelj = st.secrets["moj_email"]
        posiljatelj = st.secrets["moj_email"]
        lozinka = st.secrets["moja_lozinka"]
        
        msg = MIMEText(poruka, 'plain', 'utf-8')
        msg['Subject'] = predmet
        msg['From'] = posiljatelj
        msg['To'] = primatelj
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(posiljatelj, lozinka)
        server.sendmail(posiljatelj, primatelj, msg.as_string())
        server.quit()
        return True
    except:
        return False

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .main-header { text-align: center; padding: 30px; background: #fcfcfc; border-bottom: 3px solid #1e4620; margin-bottom: 20px; }
    .luxury-title { font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 900; color: #1a1a1a; text-transform: uppercase; }
    .luxury-subtitle { font-family: 'Lato', sans-serif; font-size: 16px; color: #1e4620; letter-spacing: 4px; }
    
    div.stButton > button {
        border-radius: 10px !important;
    }
    
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.9); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 80%; max-width: 600px; background: white; border: 10px solid #28a745;
        border-radius: 40px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; text-align: center; padding: 40px;
    }
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

DRZAVE_LISTA = ["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Španjolska", "Švedska"]

# --- PRIJEVODI ---
LANG = {
    "Hrvatska": {
        "nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚠️ INFORMACIJE", "nav_info": "ℹ️ O NAMA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Način plaćanja:** Isključivo pouzećem (gotovinom prilikom preuzimanja).",
        "info_vaga": "### ⚖️ Napomena o vaganim proizvodima\nKod artikala poput mesa i suhomesnatih proizvoda, zbog specifičnosti rezanja nemoguće je postići u gram preciznu težinu. Iz tog je razloga iznos u vašoj košarici informativne prirode. Prilikom pripreme vaše narudžbe nastojat ćemo maksimalno poštovati tražene količine kako bi konačan račun bio što bliži informativnom iznosu koji vidite u košarici. Točan iznos računa za meso i dostavu paketa znati ćete kada vam dostavna služba dostavi paket. Hvala na razumijevanju.",
        "success": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!", "client_info": "Podaci za dostavu"
    },
    "Njemačka": {
        "nav_shop": "🏬 SHOP", "nav_info_tab": "⚠️ INFOS", "nav_info": "ℹ️ ÜBER UNS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 SPRACHE",
        "cart_title": "🛒 WARENKORB", "total": "Informativer Betrag", "btn_order": "BESTELLEN",
        "pay_note": "💳 **Zahlungsart:** Nur per Nachnahme (Barzahlung bei Lieferung).",
        "info_vaga": "### ⚖️ Hinweis zu gewogenen Produkten\nBei Artikeln wie Fleisch und Wurstwaren ist es unmöglich, ein grammgenaues Gewicht zu erreichen. Daher ist der Betrag in Ihrem Warenkorb informativ. Wir bemühen uns, die Mengen einzuhalten. Den genauen Rechnungsbetrag erfahren Sie bei der Lieferung. Danke für Ihr Verständnis.",
        "success": "ERFOLGREICH ABGESENDET!<br><br>DANKE!", "client_info": "Lieferdaten"
    },
    "Italija": {
        "nav_shop": "🏬 NEGOZIO", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ SU DI NOI", "nav_con": "📞 CONTATTO", "nav_lang": "🌍 LINGUA",
        "cart_title": "🛒 CARRELLO", "total": "Importo informativo", "btn_order": "ORDINA",
        "pay_note": "💳 **Metodo di pagamento:** Solo contrassegno.",
        "info_vaga": "### ⚖️ Nota sui prodotti pesati\nPer carne e salumi è impossibile raggiungere un peso preciso al grammo. L'importo nel carrello è informativo. L'importo esatto sarà confermato alla consegna. Grazie.",
        "success": "ORDINE INVIATO!<br><br>GRAZIE!", "client_info": "Dati di consegna"
    },
    "Austrija": {"nav_shop": "🏬 SHOP", "nav_info_tab": "⚠️ INFOS", "nav_info": "ℹ️ ÜBER UNS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 SPRACHE", "cart_title": "🛒 WARENKORB", "total": "Informativer Betrag", "btn_order": "BESTELLEN", "pay_note": "💳 **Zahlungsart:** Nachnahme.", "info_vaga": "### ⚖️ Hinweis zu gewogenen Produkten...", "success": "DANKE!", "client_info": "Lieferdaten"},
    "Slovenija": {"nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚠️ INFORMACIJE", "nav_info": "ℹ️ O NAS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK", "cart_title": "🛒 KOŠARICA", "total": "Informativni znesek", "btn_order": "ODDAJ NAROČILO", "pay_note": "💳 **Plačilo:** Po povzetju.", "info_vaga": "### ⚖️ Opomba o tehtanih izdelkih...", "success": "HVALA!", "client_info": "Podatki za dostavo"},
    "Francuska": {"nav_shop": "🏬 BOUTIQUE", "nav_info_tab": "⚠️ INFOS", "nav_info": "ℹ️ À PROPOS", "nav_con": "📞 CONTACT", "nav_lang": "🌍 LANGUE", "cart_title": "🛒 PANIER", "total": "Montant indicatif", "btn_order": "COMMANDER", "pay_note": "💳 **Paiement:** Contre remboursement.", "info_vaga": "### ⚖️ Note sur les produits pesés...", "success": "MERCI !", "client_info": "Infos livraison"},
    "Mađarska": {"nav_shop": "🏬 BOLT", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ RÓLUNK", "nav_con": "📞 KAPCSOLAT", "nav_lang": "🌍 NYELV", "cart_title": "🛒 KOSÁR", "total": "Tájékoztató összeg", "btn_order": "RENDELÉS", "pay_note": "💳 **Fizetés:** Utánvét.", "info_vaga": "### ⚖️ Megjegyzés...", "success": "KÖSZÖNJÜK!", "client_info": "Szállítási adatok"},
    "Češka": {"nav_shop": "🏬 OBCHOD", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ O NÁS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JAZYK", "cart_title": "🛒 KOŠÍK", "total": "Informativní částka", "btn_order": "OBJEDNAT", "pay_note": "💳 **Platba:** Dobírka.", "info_vaga": "### ⚖️ Poznámka...", "success": "DĚKUJEME!", "client_info": "Dodací údaje"},
    "Poljska": {"nav_shop": "🏬 SKLEP", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ O NAS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JĘZYK", "cart_title": "🛒 KOSZYK", "total": "Kwota informacyjna", "btn_order": "ZAMÓW", "pay_note": "💳 **Płatność:** Za pobraniem.", "info_vaga": "### ⚖️ Uwaga...", "success": "DZIĘKUJEMY!", "client_info": "Dane do dostawy"},
    "Belgija": {"nav_shop": "🏬 SHOP", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ ABOUT US", "nav_con": "📞 CONTACT", "nav_lang": "🌍 LANGUAGE", "cart_title": "🛒 CART", "total": "Estimated Total", "btn_order": "ORDER", "pay_note": "💳 **Payment:** COD.", "info_vaga": "### ⚖️ Note...", "success": "THANK YOU!", "client_info": "Delivery Details"},
    "Španjolska": {"nav_shop": "🏬 TIENDA", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ NOSOTROS", "nav_con": "📞 CONTACTO", "nav_lang": "🌍 IDIOMA", "cart_title": "🛒 CARRITO", "total": "Importe informativo", "btn_order": "PEDIR", "pay_note": "💳 **Pago:** Contra reembolso.", "info_vaga": "### ⚖️ Nota...", "success": "¡GRACIAS!", "client_info": "Datos de envío"},
    "Švedska": {"nav_shop": "🏬 BUTIK", "nav_info_tab": "⚠️ INFO", "nav_info": "ℹ️ OM OSS", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 SPRÅK", "cart_title": "🛒 VARUKORG", "total": "Informativt belopp", "btn_order": "BESTÄLL", "pay_note": "💳 **Betalning:** Postförskott.", "info_vaga": "### ⚖️ Information...", "success": "TACK!", "client_info": "Leveransuppgifter"}
}

# Za jezike koji nisu detaljno ispisani iznad, sustav koristi engleski/hrvatski predložak.

# --- SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = "Hrvatska"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG.get(st.session_state.lang, LANG["Hrvatska"])

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.order_done = False
    st.rerun()

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">KOJUNDŽIĆ</div><div class="luxury-subtitle">MESNICA I PRERADA MESA SISAK</div></div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs([L["nav_shop"], L["nav_info_tab"], L["nav_info"], L["nav_con"], L["nav_lang"]])

# --- 1. TRGOVINA ---
with tabs[0]:
    col_t, col_k = st.columns([1.5, 1], gap="large")
    
    with col_t:
        st.header(L["nav_shop"])
        itms = list(PROIZVODI.items())
        for i in range(0, len(itms), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(itms):
                    nz, info = itms[i+j]
                    with cols[j]:
                        with st.container(border=True):
                            st.subheader(nz)
                            st.write(f"Cijena: **{info['cijena']:.2f} € / {info['jedinica']}**")
                            c1, c2, c3 = st.columns([1,1,1])
                            if c1.button("➖", key=f"m_{nz}"):
                                if nz in st.session_state.cart:
                                    st.session_state.cart[nz] -= (0.5 if info['jedinica'] == "kg" else 1.0)
                                    if st.session_state.cart[nz] <= 0: del st.session_state.cart[nz]
                                    st.rerun()
                            val = st.session_state.cart.get(nz, 0.0)
                            c2.markdown(f"<h3 style='text-align:center;margin:0;'>{val}</h3>", unsafe_allow_html=True)
                            if c3.button("➕", key=f"p_{nz}"):
                                st.session_state.cart[nz] = st.session_state.cart.get(nz, 0.0) + (0.5 if info['jedinica'] == "kg" else 1.0)
                                st.rerun()

    with col_k:
        st.header(L["cart_title"])
        ukupno = 0.0
        if not st.session_state.cart:
            st.info("Košarica je prazna.")
        else:
            for s, k in st.session_state.cart.items():
                iznos = k * PROIZVODI[s]["cijena"]
                ukupno += iznos
                st.write(f"**{s}** ({k} {PROIZVODI[s]['jedinica']}) = {iznos:.2f} €")
            
            st.divider()
            st.subheader(f"{L['total']}: {ukupno:.2f} €")
            st.warning(L["pay_note"])
            
            with st.form("form_order"):
                st.write(f"### {L['client_info']}")
                ime = st.text_input("Ime i Prezime")
                tel = st.text_input("Mobitel / Phone")
                adr = st.text_area("Adresa / Address")
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr and tel:
                        detalji = "\n".join([f"- {k}: {v}" for k, v in st.session_state.cart.items()])
                        poruka = f"KUPAC: {ime}\nTEL: {tel}\nADRESA: {adr}\nDRŽAVA: {st.session_state.lang}\n\nNARUDŽBA:\n{detalji}\n\nTOTAL: {ukupno:.2f} €\nPLAĆANJE: POUZEĆEM"
                        if posalji_email(f"Narudžba: {ime}", poruka):
                            st.session_state.cart = {}
                            st.session_state.order_done = True
                            st.rerun()
                    else:
                        st.error("Molimo ispunite sve podatke.")

# --- 2. INFORMACIJE ---
with tabs[1]:
    st.markdown(L["info_vaga"])

# --- 3. O NAMA ---
with tabs[2]:
    st.header(L["nav_info"])
    st.write("Obiteljska tradicija Kojundžić iz Siska...")

# --- 4. KONTAKT ---
with tabs[3]:
    st.header(L["nav_con"])
    st.write("📍 Gradska tržnica Sisak")
    st.write("📞 +385 44 123 456")

# --- 5. JEZIK ---
with tabs[4]:
    st.header(L["nav_lang"])
    odabir = st.selectbox("Odaberite državu / Select country", DRZAVE_LISTA, index=DRZAVE_LISTA.index(st.session_state.lang))
    if odabir != st.session_state.lang:
        st.session_state.lang = odabir
        st.rerun()
