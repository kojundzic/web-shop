import streamlit as st
import smtplib
import time
from email.mime.text import MIMEText

# =================================================================
# 🥩 KOJUNDŽIĆ SISAK 2026. - ULTIMATE EXTENDED EDITION
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
    div.stButton > button { border-radius: 10px !important; }
    .success-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0,0,0,0.9); z-index: 9999; display: flex; justify-content: center; align-items: center; }
    .success-modal { width: 80%; max-width: 600px; background: white; border: 10px solid #28a745; border-radius: 40px; text-align: center; padding: 40px; }
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

# --- FUNKCIJA ZA DUGE TEKSTOVE (200+ riječi) ---
def GET_TEXT(tab, lang):
    hr_texts = {
        "about": """Obiteljski posao Kojundžić ponosno stoji kao simbol tradicije u Sisačko-moslavačkoj županiji. Naša proizvodnja temelji se isključivo na tradicionalnom načinu prerade mesa, onako kako su to radili naši stari, bez korištenja industrijskih kemikalija ili ubrzanih procesa zrenja. Svaki komad mesa koji izađe iz naše obiteljske radionice u Sisku plod je ručnog rada, strpljenja i dubokog poštovanja prema zanatu. Dimljenje obavljamo na prirodnom drvu bukve i grabovine, što našim proizvodima daje onu specifičnu, bogatu aromu koju je nemoguće postići u modernim pogonima. Kao obitelj, izravno smo uključeni u svaki korak – od odabira najbolje sirovine do finalnog pakiranja za naše vjerne kupce na gradskoj tržnici. Vjerujemo da se kvaliteta ne može požuriti, zbog čega svaka kobasica, panceta ili hamburger prolaze kroz prirodan proces sušenja. Naša misija je očuvati autentične okuse posavskog i banovinskog kraja te ih prenijeti budućim generacijama. Svjesni smo da kupci danas traže povjerenje i zdravu hranu, stoga u našoj mesnici nećete pronaći ništa osim čistog mesa i domaćih začina. Kojundžić ime jamči vam svježinu koja dolazi iz srca naše obitelji izravno na vaš stol. Pozivamo vas da okusite razliku koju donosi desetljeće iskustva i nepokolebljiva predanost tradicionalnoj proizvodnji koja ne poznaje kompromise.""",
        "suppliers": """Kvaliteta našeg mesa počinje na prostranim pašnjacima Parka prirode Lonjsko polje, Posavine i Banovine. Surađujemo isključivo s lokalnim uzgajivačima i OPG-ovima koji dijele našu viziju o etičkom i prirodnom uzgoju stoke. Naši dobavljači dolaze iz regija poznatih po netaknutoj prirodi i čistom zraku, gdje životinje borave na otvorenom tijekom većeg dijela godine. Lonjsko polje, kao jedno od najvećih zaštićenih vlažnih staništa u Europi, pruža specifičnu ispašu koja našem mesu daje jedinstvenu teksturu i bogatstvo nutrijenata. Banovina i Posavina, sa svojom dugom tradicijom stočarstva, osiguravaju nam stoku koja je hranjena domaćim žitaricama bez GMO dodataka. Ovakav pristup ne samo da jamči vrhunski okus, već i podupire opstanak malih seoskih gospodarstava u našoj regiji. Mi ne kupujemo meso na burzama ili iz masovnog uvoza; mi poznajemo ljude koji su uzgojili tu stoku. Kratki lanci opskrbe znače da meso putuje minimalno, zadržavajući svježinu i kvalitetu. Podupiranjem lokalne poljoprivrede osiguravamo održivost našeg kraja i jamčimo vam sljedivost svakog komada koji kupite. Svaki put kada odaberete Kojundžić proizvode, vi zapravo birate plodove suradnje između marljivih ljudi s Banovine i Posavine te naše obiteljske tradicije koja to meso pretvara u deliciju.""",
        "hygiene": """Higijena i sigurnost hrane u mesnici Kojundžić predstavljaju nulti prioritet od kojeg nikada ne odstupamo. U našem modernom pogonu u Sisku implementirali smo stroge HACCP protokole koji prate svaki korak proizvodnog procesa, od ulaza sirovine do krajnje dostave. Svaki alat, radna površina i prostorija dezinficiraju se svakodnevno prema najvišim sanitarnim standardima kako bi se osigurala apsolutna čistoća. Naša predanost higijeni nadilazi puko ispunjavanje zakonskih normi – mi to vidimo kao moralnu obvezu prema našim kupcima i obitelji. Redovito vršimo mikrobiološka ispitivanja uzoraka u ovlaštenim laboratorijima te vodimo digitalnu evidenciju temperature u svim rashladnim sustavima. Ovime osiguravamo da hladni lanac ostane neprekinut, što je ključno za očuvanje svježine mesa. Naši zaposlenici prolaze stalne edukacije o novim metodama zaštite hrane i osobne higijene, jer razumijemo da i najmanji propust može utjecati na kvalitetu. Prostorije za dimljenje i zrenje projektirane su tako da osiguravaju savršene mikroklimatske uvjete, dok suvremena oprema za pakiranje štiti gotove proizvode od vanjskih utjecaja. Kupujući kod nas, možete biti potpuno mirni znajući da je higijena na razini koja odgovara najvišim europskim standardima, uz zadržavanje onog starinskog, domaćeg okusa kojem težimo."""
    }

    en_texts = {
        "about": """The Kojundžić family business stands as a pillar of tradition in the Sisak-Moslavina County. Our production is based solely on traditional meat processing methods, just as our ancestors did, without chemicals. Each piece of meat leaving our Sisak workshop is handcrafted with patience and respect for the craft. We use natural beech and hornbeam wood for smoking, giving our products a rich aroma impossible to achieve in industrial facilities. As a family, we are involved in every step, ensuring quality from raw material selection to the Sisak city market...""",
        "suppliers": """The quality of our meat starts in the vast pastures of the Lonjsko Polje Nature Park, Posavina, and Banovina. We collaborate exclusively with local breeders who share our vision of ethical and natural livestock farming. These regions, known for untouched nature, provide a unique grazing environment that gives our meat its rich texture. By supporting local farms in Banovina and Posavina, we ensure sustainability for our rural communities and guarantee traceability for every piece of meat...""",
        "hygiene": """Hygiene and food safety at the Kojundžić butchery are our zero-priority. In our Sisak facility, we have implemented strict HACCP protocols monitoring every step of the process. Every tool and surface is disinfected daily to the highest sanitary standards. Our commitment goes beyond legal norms; it is a moral duty to our customers. We conduct regular microbiological tests to ensure freshness and safety, maintaining an unbroken cold chain from processing to your doorstep..."""
    }

    # Sustav odabira jezika (ako je odabrana HR, ide HR, za sve ostalo EN kao međunarodni standard)
    if lang == "Hrvatska":
        return hr_texts.get(tab, "")
    else:
        # Ovdje bi se dodali DE, IT, FR prijevodi istih 200 riječi. Za primjer koristimo EN za sve ostale jezike.
        return en_texts.get(tab, "")

# --- PRIJEVODI NAVIGACIJE ---
LANG = {
    "Hrvatska": {
        "nav_shop": "🏬 TRGOVINA", "nav_info_tab": "⚠️ INFORMACIJE", "nav_info": "ℹ️ O NAMA", "nav_supp": "🚜 DOBAVLJAČI", "nav_hyg": "🛡️ HIGIJENA", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 JEZIK",
        "cart_title": "🛒 KOŠARICA", "total": "Informativni iznos", "btn_order": "POŠALJI NARUDŽBU",
        "pay_note": "💳 **Način plaćanja:** Isključivo pouzećem (gotovinom prilikom preuzimanja).",
        "info_vaga": "### ⚖️ Napomena o vaganim proizvodima\nKod artikala poput mesa i suhomesnatih proizvoda, zbog specifičnosti rezanja nemoguće je postići u gram preciznu težinu. Iz tog je razloga iznos u vašoj košarici informativne prirode. Prilikom pripreme vaše narudžbe nastojat ćemo maksimalno poštovati tražene količine kako bi konačan račun bio što bliži informativnom iznosu koji vidite u košarici. Točan iznos računa za meso i dostavu paketa znati ćete kada vam dostavna služba dostavi paket. Hvala na razumijevanju.",
        "success": "USPJEŠNO STE PREDALI NARUDŽBU!<br><br>HVALA!", "client_info": "Podaci za dostavu"
    },
    "Njemačka": {
        "nav_shop": "🏬 SHOP", "nav_info_tab": "⚠️ INFOS", "nav_info": "ℹ️ ÜBER UNS", "nav_supp": "🚜 LIEFERANTEN", "nav_hyg": "🛡️ HYGIENE", "nav_con": "📞 KONTAKT", "nav_lang": "🌍 SPRACHE",
        "cart_title": "🛒 WARENKORB", "total": "Informativer Betrag", "btn_order": "BESTELLEN",
        "pay_note": "💳 **Zahlung:** Nur Nachnahme.",
        "info_vaga": "### ⚖️ Hinweis zu gewogenen Produkten\nAufgrund des Zuschnitts ist ein grammgenaues Gewicht nicht möglich...",
        "success": "ERFOLGREICH!<br><br>DANKE!", "client_info": "Lieferdaten"
    },
    # ... (Ostali jezici koriste HR ili EN logiku u tabovima ovisno o odabiru)
}

# --- SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = "Hrvatska"
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'order_done' not in st.session_state: st.session_state.order_done = False

L = LANG.get(st.session_state.lang, LANG["Hrvatska"])

# --- SUCCESS MODAL ---
if st.session_state.order_done:
    st.markdown(f'<div class="success-overlay"><div class="success-modal"><div style="color:#28a745;font-size:40px;font-weight:bold;">{L["success"]}</div></div></div>', unsafe_allow_html=True)
    time.sleep(3); st.session_state.order_done = False; st.rerun()

# --- HEADER ---
st.markdown(f'<div class="main-header"><div class="luxury-title">KOJUNDŽIĆ</div><div class="luxury-subtitle">MESNICA I PRERADA MESA SISAK</div></div>', unsafe_allow_html=True)

# --- TABS ---
# Dodana dva nova taba: nav_supp i nav_hyg
tabs = st.tabs([L["nav_shop"], L["nav_info_tab"], L["nav_info"], L.get("nav_supp", "🚜 DOBAVLJAČI"), L.get("nav_hyg", "🛡️ HIGIJENA"), L["nav_con"], L["nav_lang"]])

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
                            c1, c2, c3 = st.columns(3)
                            if c1.button("➖", key=f"m_{nz}"):
                                if nz in st.session_state.cart:
                                    st.session_state.cart[nz] -= (0.5 if info['jedinica'] == "kg" else 1.0)
                                    if st.session_state.cart[nz] <= 0: del st.session_state.cart[nz]
                                    st.rerun()
                            val = st.session_state.cart.get(nz, 0.0)
                            c2.markdown(f"<h3 style='text-align:center;'>{val}</h3>", unsafe_allow_html=True)
                            if c3.button("➕", key=f"p_{nz}"):
                                st.session_state.cart[nz] = st.session_state.cart.get(nz, 0.0) + (0.5 if info['jedinica'] == "kg" else 1.0)
                                st.rerun()
    with col_k:
        st.header(L["cart_title"])
        ukupno = 0.0
        if not st.session_state.cart: st.info("Prazno")
        else:
            for s, k in st.session_state.cart.items():
                iznos = k * PROIZVODI[s]["cijena"]
                ukupno += iznos
                st.write(f"**{s}** ({k}) = {iznos:.2f} €")
            st.divider()
            st.subheader(f"{L['total']}: {ukupno:.2f} €")
            st.warning(L["pay_note"])
            with st.form("f_ord"):
                ime = st.text_input("Ime i Prezime")
                tel = st.text_input("Mobitel")
                adr = st.text_area("Adresa")
                if st.form_submit_button(L["btn_order"], use_container_width=True):
                    if ime and adr:
                        if posalji_email(f"Narudžba {ime}", f"Kupac: {ime}\nAdresa: {adr}\nTel: {tel}\nStavke: {st.session_state.cart}"):
                            st.session_state.cart = {}; st.session_state.order_done = True; st.rerun()

# --- 2. INFORMACIJE ---
with tabs[1]:
    st.markdown(L["info_vaga"])

# --- 3. O NAMA ---
with tabs[2]:
    st.header(L["nav_info"])
    st.write(GET_TEXT("about", st.session_state.lang))

# --- 4. DOBAVLJAČI ---
with tabs[3]:
    st.header(L.get("nav_supp", "🚜 DOBAVLJAČI"))
    st.write(GET_TEXT("suppliers", st.session_state.lang))

# --- 5. HIGIJENA ---
with tabs[4]:
    st.header(L.get("nav_hyg", "🛡️ HIGIJENA"))
    st.write(GET_TEXT("hygiene", st.session_state.lang))

# --- 6. KONTAKT ---
with tabs[5]:
    st.header(L["nav_con"])
    st.write("📍 Gradska tržnica Sisak | 📞 +385 44 123 456")

# --- 7. JEZIK ---
with tabs[6]:
    st.header(L["nav_lang"])
    odabir = st.selectbox("Država / Country", DRZAVE_LISTA, index=DRZAVE_LISTA.index(st.session_state.lang))
    if odabir != st.session_state.lang:
        st.session_state.lang = odabir
        st.rerun()
