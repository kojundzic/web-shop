import streamlit as st
import streamlit.components.v1 as components
import time

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - FINALNI PRO DIZAJN
# =================================================================

st.set_page_config(page_title="KOJUNDŽIĆ Mesnica", page_icon="🥩", layout="wide")

# --- CUSTOM CSS ZA ZELENI PROZOR (15x20 cm) I DIZAJN ---
st.markdown("""
    <style>
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0,0,0,0.7); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .success-modal {
        width: 15cm; height: 10cm; /* Prilagođeno radi preglednosti ekrana */
        background-color: white; border: 8px solid #28a745;
        border-radius: 30px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; text-align: center;
        padding: 40px; box-shadow: 0px 0px 50px rgba(0,0,0,0.5);
    }
    .success-text { color: #28a745; font-size: 38px; font-weight: bold; line-height: 1.2; }
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

if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_status' not in st.session_state: st.session_state.order_status = False

# --- PRIKAZ USPJEŠNOG PROZORA (5 SEKUNDI) ---
if st.session_state.order_status:
    st.markdown("""
        <div class="success-overlay">
            <div class="success-modal">
                <div class="success-text">USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.order_status = False
    st.session_state.cart = {}
    st.rerun()

# --- NASLOV ---
st.title("🥩 KOJUNDŽIĆ | Mesnica i prerada mesa Sisak")
st.markdown("---")

# --- KARTICE (IZNAD TRGOVINE) ---
tab_info, tab_dob, tab_haccp, tab_ug = st.tabs([
    "ℹ️ O NAMA", "🚜 DOBAVLJAČI", "🛡️ HACCP", "🏨 ZA UGOSTITELJE"
])

with tab_info:
    st.write("### Obiteljska tradicija Kojundžić\nNaša mesnica u Sisku simbol je vrhunske kvalitete i domaće obrade mesa još od davnina. Svi naši recepti su autentični i prirodni.")
with tab_dob:
    st.write("### Naši Dobavljači\nSurađujemo isključivo s probranim OPG-ovima Sisačko-moslavačke županije. Meso je 100% domaćeg podrijetla.")
with tab_haccp:
    st.write("### HACCP Standardi\nSigurnost hrane je naš prioritet. Naš pogon zadovoljava sve EU kriterije o higijeni i kontroli procesa prerade.")
with tab_ug:
    st.write("### Za Ugostitelje\nNudimo specijalne rezove i prioritetnu dostavu za restorane, hotele i catering službe. Kontaktirajte nas za partnerstvo.")

st.markdown("---")

# --- GLAVNI LAYOUT ---
col_main, col_checkout = st.columns([1.5, 1], gap="large")

# --- LIJEVA STRANA: TRGOVINA ---
with col_main:
    st.header("🏬 Ponuda trgovine")
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
                        c1, c2 = st.columns(2)
                        if c1.button("➕ Dodaj", key=f"add_{naziv}", use_container_width=True):
                            curr = st.session_state.cart.get(naziv, 0.0)
                            st.session_state.cart[naziv] = 1.0 if curr == 0 and jed == "kg" else curr + (0.5 if jed == "kg" else 1.0)
                            st.rerun()
                        if c2.button("➖ Smanji", key=f"rem_{naziv}", use_container_width=True):
                            if naziv in st.session_state.cart:
                                curr = st.session_state.cart[naziv]
                                step = 0.5 if jed == "kg" else 1.0
                                if curr <= step: del st.session_state.cart[naziv]
                                else: st.session_state.cart[naziv] -= step
                                st.rerun()
                        if naziv in st.session_state.cart:
                            st.info(f"U košarici: {st.session_state.cart[naziv]} {jed}")

# --- DESNA STRANA: CHECKOUT (STALNO VIDLJIVO) ---
with col_checkout:
    st.header("🛒 Pregled narudžbe")
    
    # 1. Košarica
    inf_total = 0
    if not st.session_state.cart:
        st.warning("Vaša košarica je trenutno prazna.")
    else:
        for it, q in st.session_state.cart.items():
            cijena_stavke = q * PROIZVODI[it]["cijena"]
            inf_total += cijena_stavke
            jed_oznaka = PROIZVODI[it]["jedinica"]
            st.write(f"✅ {it} ({q} {jed_oznaka}) = **{cijena_stavke:.2f} €**")
        
        st.markdown(f"### Informativni iznos: {inf_total:.2f} €")
    
    # 2. Fiksna napomena
    st.info("""
    **Napomena o iznosu:**  
    Istaknute cijene su točne, a konačan iznos računa saznat ćete u trenutku kada Vam dostavljač isporuči paket. Mi ćemo se maksimalno potruditi biti što bliži traženoj količini i informativnom iznosu.
    """)
    
    st.divider()
    
    # 3. Podaci o kupcu
    st.header("📍 Podaci za dostavu")
    f_ime = st.text_input("Ime i Prezime*")
    f_drzava = st.selectbox("Država*", ["Hrvatska", "Austrija", "Njemačka", "Slovenija"])
    f_grad = st.selectbox("Grad*", ["Sisak", "Zagreb", "Petrinja", "Velika Gorica", "Kutina", "Popovača", "Ostalo..."])
    f_zip = st.text_input("Poštanski broj*")
    f_adr = st.text_input("Adresa i kućni broj*")
    f_mob = st.text_input("Broj mobitela*")

    # VALIDACIJA
    podaci_ok = all([f_ime, f_zip, f_adr, f_mob])
    kosarica_ok = len(st.session_state.cart) > 0

    # PORUKE O NEDOSTATKU
    if not kosarica_ok:
        st.error("Niste odabrali niti jedan artikl za narudžbu!")
    elif not podaci_ok:
        st.error("Molimo popunite sva polja označena zvjezdicom (*)!")

    # GUMB ZA NARUDŽBU
    if st.button("🚀 POŠALJI NARUDŽBU", type="primary", use_container_width=True, disabled=not (podaci_ok and kosarica_ok)):
        st.session_state.order_status = True
        st.rerun()
