import streamlit as st
import streamlit.components.v1 as components
import time

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - EU DYNAMIC CHECKOUT EDITION
# =================================================================

st.set_page_config(page_title="KOJUNDŽIĆ Mesnica", page_icon="🥩", layout="wide")

# --- CUSTOM CSS ZA MODAL I DIZAJN ---
st.markdown("""
    <style>
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.8); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 15cm; height: 10cm; background-color: white; 
        border: 8px solid #28a745; border-radius: 30px; 
        display: flex; flex-direction: column; justify-content: center; 
        align-items: center; text-align: center; padding: 20px;
    }
    .success-text { color: #28a745; font-size: 35px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- PODACI O DRŽAVAMA I GRADOVIMA EU ---
EU_DATA = {
    "Hrvatska": ["Sisak", "Zagreb", "Split", "Rijeka", "Osijek", "Zadar", "Varaždin", "Petrinja", "Kutina", "Samobor"],
    "Austrija": ["Beč", "Salzburg", "Graz", "Linz", "Innsbruck", "Klagenfurt"],
    "Njemačka": ["Berlin", "München", "Hamburg", "Frankfurt", "Stuttgart", "Köln", "Düsseldorf"],
    "Slovenija": ["Ljubljana", "Maribor", "Celje", "Kranj", "Velenje", "Koper"],
    "Italija": ["Rim", "Milano", "Venecija", "Napulj", "Torino", "Firenca"],
    "Francuska": ["Pariz", "Lyon", "Marseille", "Nice", "Bordeaux"],
    "Mađarska": ["Budimpešta", "Debrecen", "Szeged", "Pečuh"],
    "Češka": ["Prag", "Brno", "Ostrava", "Plzeň"],
    "Poljska": ["Varšava", "Krakov", "Wrocław", "Poznań"],
    "Belgija": ["Bruxelles", "Antwerpen", "Gent", "Brugge"],
    # ... Ostale države se dodaju na isti način
}
SVE_EU_DRZAVE = sorted(["Hrvatska", "Austrija", "Njemačka", "Slovenija", "Italija", "Francuska", "Mađarska", "Češka", "Poljska", "Belgija", "Bugarska", "Cipar", "Danska", "Estonija", "Finska", "Grčka", "Irska", "Latvija", "Litva", "Luksemburg", "Malta", "Nizozemska", "Portugal", "Rumunjska", "Slovačka", "Španjolska", "Švedska"])

# --- PROIZVODI ---
PROIZVODI = {
    "Dimljeni hamburger": {"cijena": 15.00, "jedinica": "kg"},
    "Domaća Panceta": {"cijena": 12.00, "jedinica": "kg"},
    "Domaći Čvarci": {"cijena": 5.00, "jedinica": "kg"},
    "Suha rebra": {"cijena": 9.00, "jedinica": "kg"},
    "Slavonska kobasica": {"cijena": 4.50, "jedinica": "kom"},
    "Dimljeni buncek": {"cijena": 7.50, "jedinica": "kom"}
}

if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_status' not in st.session_state: st.session_state.order_status = False

# --- PRIKAZ MODALA ---
if st.session_state.order_status:
    st.markdown("""<div class="success-overlay"><div class="success-modal"><div class="success-text">USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!</div></div></div>""", unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.order_status = False
    st.session_state.cart = {}
    st.rerun()

st.title("🥩 KOJUNDŽIĆ | Mesnica Sisak")
st.markdown("---")

# --- KARTICE (IZNAD TRGOVINE) ---
t_info, t_dob, t_haccp, t_ug = st.tabs(["ℹ️ O NAMA", "🚜 DOBAVLJAČI", "🛡️ HACCP", "🏨 ZA UGOSTITELJE"])
with t_info: st.write("### Obiteljska tradicija\nNaša mesnica u Sisku simbol je kvalitete od 2026. godine.")
with t_dob: st.write("### Naši Dobavljači\nSurađujemo isključivo s lokalnim OPG-ovima.")
with t_haccp: st.write("### HACCP Standardi\nSigurnost hrane po najvišim EU kriterijima.")
with t_ug: st.write("### Za Ugostitelje\nSpecijalni rezovi i prioritetna dostava za restorane.")

st.markdown("---")

# --- MAIN LAYOUT ---
col_trgovina, col_checkout = st.columns([1.4, 1], gap="large")

with col_trgovina:
    st.header("🏬 Ponuda trgovine")
    items = list(PROIZVODI.items())
    for i in range(0, len(items), 2):
        r_cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                naziv, info = items[i+j]
                jed = info["jedinica"]
                with r_cols[j]:
                    with st.container(border=True):
                        st.subheader(naziv)
                        st.write(f"Cijena: **{info['cijena']:.2f} € / {jed}**")
                        c1, c2 = st.columns(2)
                        if c1.button("➕ Dodaj", key=f"a_{naziv}"):
                            curr = st.session_state.cart.get(naziv, 0.0)
                            st.session_state.cart[naziv] = 1.0 if curr == 0 and jed == "kg" else curr + (0.5 if jed == "kg" else 1.0)
                            st.rerun()
                        if c2.button("➖ Smanji", key=f"r_{naziv}"):
                            if naziv in st.session_state.cart:
                                curr = st.session_state.cart[naziv]
                                step = 0.5 if jed == "kg" else 1.0
                                if curr <= step: del st.session_state.cart[naziv]
                                else: st.session_state.cart[naziv] -= step
                                st.rerun()
                        if naziv in st.session_state.cart:
                            st.success(f"Količina: {st.session_state.cart[naziv]} {jed}")

with col_checkout:
    st.header("🛒 Pregled & Plaćanje")
    
    # 1. Košarica
    inf_total = 0
    if not st.session_state.cart:
        st.warning("Košarica je prazna.")
    else:
        for it, q in st.session_state.cart.items():
            sub = q * PROIZVODI[it]["cijena"]
            inf_total += sub
            st.write(f"✅ {it} ({q} {PROIZVODI[it]['jedinica']}) = **{sub:.2f} €**")
        st.markdown(f"### Informativni iznos: {inf_total:.2f} €")
    
    st.info("**Napomena:** Cijene su točne, a konačan iznos znat ćete pri dostavi. Pokušat ćemo biti što bliži traženoj količini.")
    
    st.divider()
    
    # 2. Dinamički Podaci o Kupcu
    st.header("📍 Dostava")
    f_ime = st.text_input("Ime*")
    f_prezime = st.text_input("Prezime*")
    
    # DINAMIČKI IZBORNIK DRŽAVA I GRADOVA
    f_drzava = st.selectbox("Odaberite državu EU*", SVE_EU_DRZAVE)
    
    # Filtriranje gradova na temelju države
    ponudeni_gradovi = EU_DATA.get(f_drzava, ["Ostalo (upiši ručno)"])
    if "Ostalo (upiši ručno)" not in ponudeni_gradovi:
        ponudeni_gradovi.append("Ostalo (upiši ručno)")
    
    f_grad_select = st.selectbox("Odaberite grad*", ponudeni_gradovi)
    
    # Ako kupac odabere 'Ostalo', pojavljuje se polje za ručni upis
    if f_grad_select == "Ostalo (upiši ručno)":
        f_grad = st.text_input("Upišite naziv vašeg grada*")
    else:
        f_grad = f_grad_select
        
    f_zip = st.text_input("Poštanski broj*")
    f_adr = st.text_input("Adresa (ulica i kućni broj)*")
    f_mob = st.text_input("Broj mobitela*")

    # VALIDACIJA
    podaci_ok = all([f_ime, f_prezime, f_grad, f_zip, f_adr, f_mob])
    kosarica_ok = len(st.session_state.cart) > 0

    if not kosarica_ok:
        st.error("Košarica ne smije biti prazna!")
    elif not podaci_ok:
        st.error("Molimo ispunite sve podatke za dostavu!")

    # GUMB
    if st.button("🚀 POŠALJI NARUDŽBU", type="primary", use_container_width=True, disabled=not (podaci_ok and kosarica_ok)):
        st.session_state.order_status = True
        st.rerun()
