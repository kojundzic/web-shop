import streamlit as st
import smtplib
from email.mime.text import MIMEText

# =================================================================
# 🛡️ STABILNA VERZIJA - KOJUNDŽIĆ SISAK (BACKUP)
# =================================================================

# Povlačenje podataka iz Streamlit Secrets postavki
MOJ_EMAIL = st.secrets["moj_email"]
MOJA_LOZINKA = st.secrets["moja_lozinka"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# --- POPIS PROIZVODA I CIJENA (EUR) ---
# Ovdje možeš mijenjati cijene po potrebi
PROIZVODI = {
    "Domaća slanina (cca 1kg)": 15.00,
    "Kulenova seka (cca 0.5kg)": 12.00,
    "Domaći čvarci (250g)": 5.00,
    "Suha rebra (cca 1kg)": 9.00,
    "Domaća mast (kanta 2.5kg)": 10.00,
    "Slavonska kobasica (par)": 8.50,
    "Panceta narezana (100g)": 3.50
}

# --- NASLOV I INFO ---
st.title("🥩 KOJUNDŽIĆ - Mesnica i prerada mesa")
st.subheader("Tradicija iz Siska | Prodaja suhomesnatih delicija")

st.info("""
⚖️ **OBAVIJEST O TEŽINI I PLAĆANJU:** 
Svi proizvodi se važu u mesnici. Cijene na webu su informativne. 
Točan iznos bit će naveden na fiskalnom računu koji dobivate u paketu. 
Plaćanje je **POUZEĆEM** (gotovinom poštaru).
""")

# --- KOŠARICA ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- PRIKAZ PROIZVODA ---
cols = st.columns(3)
for idx, (proizvod, cijena) in enumerate(PROIZVODI.items()):
    with cols[idx % 3]:
        st.write(f"### {proizvod}")
        st.write(f"Cijena: **{cijena:.2f} €**")
        if st.button(f"Dodaj u košaricu", key=proizvod):
            st.session_state.cart[proizvod] = st.session_state.cart.get(proizvod, 0) + 1
            st.success(f"Dodano u košaricu!")

# --- PREGLED NARUDŽBE ---
st.divider()
st.header("🛒 Vaša košarica")

if not st.session_state.cart:
    st.write("Vaša košarica je trenutno prazna.")
else:
    ukupno_inf = 0
    narudžba_detalji = ""
    for stavka, kolicina in st.session_state.cart.items():
        iznos = kolicina * PROIZVODI[stavka]
        ukupno_inf += iznos
        st.write(f"✅ {stavka} x {kolicina} = **{iznos:.2f} €**")
        narudžba_detalji += f"- {stavka} x {kolicina}\n"
    
    st.write(f"### Ukupni informativni iznos: {ukupno_inf:.2f} €")
    
    if st.button("Obriši košaricu"):
        st.session_state.cart = {}
        st.rerun()

    # --- FORMA ZA DOSTAVU ---
    st.divider()
    st.header("📍 Podaci za slanje (Hrvatska Pošta)")
    with st.form("forma_narudzbe"):
        ime_prezime = st.text_input("Ime i Prezime*")
        adresa = st.text_input("Ulica i kućni broj*")
        grad = st.text_input("Poštanski broj i Grad*")
        telefon = st.text_input("Kontakt telefon*")
        napomena = st.text_area("Napomena za mesara (npr. želim deblje rezano, manji komad i sl.)")
        
        st.warning("🚚 Paket šaljemo putem Hrvatske pošte. Plaćate gotovinom prilikom preuzimanja.")
        
        posalji = st.form_submit_button("🚀 POTVRDI NARUDŽBU")
        
        if posalji:
            if not (ime_prezime and adresa and grad and telefon):
                st.error("🛑 Molimo ispunite sva polja označena zvjezdicom (*).")
            else:
                # Priprema sadržaja emaila
                sadrzaj_maila = f"""
                NOVA NARUDŽBA - MESNICA KOJUNDŽIĆ
                ----------------------------------
                KUPAC: {ime_prezime}
                ADRESA: {adresa}, {grad}
                TELEFON: {telefon}
                
                NAPOMENA: 
                {napomena if napomena else 'Nema napomene.'}
                
                NARUČENI PROIZVODI:
                {narudžba_detalji}
                
                INFORMATIVNI IZNOS: {ukupno_inf:.2f} EUR
                ----------------------------------
                Postupak: Izvažite robu, izdajte račun na kasi i pošaljite paket pouzećem.
                """
                
                try:
                    # Slanje emaila prodavaču
                    msg = MIMEText(sadrzaj_maila)
                    msg['Subject'] = f"Narudžba: {ime_prezime} ({grad})"
                    msg['From'] = MOJ_EMAIL
                    msg['To'] = MOJ_EMAIL
                    
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    
                    st.balloons()
                    st.success("✅ Hvala Vam na narudžbi! Vaši proizvodi će uskoro biti spakirani i poslani na Vašu adresu.")
                    st.session_state.cart = {} # Pražnjenje košarice nakon uspjeha
                except Exception as e:
                    st.error(f"Došlo je do greške pri slanju narudžbe. Molimo pokušajte ponovno ili nas nazovite. (Greška: {e})")
