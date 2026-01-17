import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. USIDRENI PROŠIRENI TEKSTOVI ---
T = {
    "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
    "title_sub": "OBITELJSKA MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
    "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna. Molimo odaberite proizvode iz ponude.",
    
    # PROŠIRENE RUBRIKE
    "horeca_title": "🏨 HoReCa Partnerstvo: Vrhunska sirovina za Vaš ugostiteljski objekt",
    "horeca_text": """
    Kao pouzdan partner brojnim restoranima i hotelima, Mesnica Kojundžić nudi namjenski program za HoReCa sektor. 
    Razumijemo specifične potrebe modernog ugostiteljstva te osiguravamo:
    * **Konstantnu kvalitetu:** Meso s kontroliranim udjelom masnoće i preciznim rezovima prema Vašim specifikacijama.
    * **Fleksibilnu dostavu:** Prilagođavamo termine dostave Vašem radnom vremenu u hladnom lancu.
    * **Veleprodajne cijene:** Posebni cjenici za stalne partnere i veće količine.
    * **Savjetovanje:** Pomoć pri odabiru rezova za specifična jela (dry age, pečenja, roštilj program).
    
    Za ponudu i dogovor termina prezentacije kontaktirajte nas izravno na: [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)
    """,
    
    "suppliers_title": "🚜 Podrijetlo: Iz srca Banovine, Posavine i Lonjskog polja",
    "suppliers_text": """
    Temelj naše kvalitete su naši dobavljači – mali obiteljski OPG-ovi koji dijele našu viziju.
    * **Lokalni uzgoj:** Svo meso dolazi s farmi iz okolice Siska, Gline i Petrinje. Kratak put od pašnjaka do prerade jamči svježinu koju ne možete naći u trgovačkim lancima.
    * **Prirodna prehrana:** Životinje se hrane domaćim žitaricama, bez uporabe GMO dodataka, što rezultira bogatim okusom i optimalnom teksturom mesa.
    * **Poticanje sela:** Kupnjom kod nas izravno pomažete opstanku malih proizvođača u našoj županiji.
    """,
    
    "haccp_title": "🛡️ Sigurnost hrane: Najviši standardi higijene",
    "haccp_text": """
    U Mesnici Kojundžić sigurnost potrošača je prioritet broj jedan. Naš proces proizvodnje strogo prati **HACCP (Hazard Analysis and Critical Control Points)** sustav.
    * **Digitalna sljedivost:** Svaki komad mesa ima zabilježen put od farme do prodajnog pulta.
    * **Stalna kontrola:** Redovito provodimo mikrobiološke analize u suradnji s ovlaštenim laboratorijima.
    * **Veterinarski nadzor:** Svi procesi klanja i prerade vrše se pod stalnim nadzorom državne veterinarske službe.
    * **Higijenski režim:** Naši djelatnici prolaze stalne edukacije o higijeni, a prostor se dezinficira svakodnevno najmodernijim ekološkim sredstvima.
    """,
    
    "info_title": "ℹ️ O nama: Tradicija sisačkog mesarstva",
    "info_text": """
    Obitelj Kojundžić već generacijama čuva tajne tradicionalne pripreme mesa. Naša priča počinje u Sisku, s vizijom da građanima ponudimo izvorne okuse domaćeg doma.
    Danas smo moderna prerada koja spaja djedove recepte za dimljenje mesa na prirodnom drvetu s najsuvremenijom tehnologijom pakiranja. 
    Ponosni smo što se naši proizvodi, poput slavonske kobasice i pancete, i dalje pripremaju bez nepotrebnih aditiva.
    
    📍 **LOKACIJA:** Nađite nas svaki dan na Gradskoj tržnici Kontroba u Sisku. Dođite, probajte i uvjerite se u kvalitetu koju stvaramo s ljubavlju.
    """,

    # OSTALI ELEMENTI
    "note_vaga": "⚖️ **VAŽNA NAPOMENA:** Cijene su fiksne po jedinici mjere, no točan iznos računa znat ćemo tek nakon preciznog vaganja prije pakiranja.",
    "note_delivery": "🚚 **DOSTAVA:** Šaljemo u termo-izoliranoj ambalaži. Plaćanje **pouzećem**.",
    "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*", "form_country": "Država*", "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
    "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "total": "Informativni iznos", "shipping_info": "📍 PODACI ZA DOSTAVU",
    "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci", "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
    "p7": "Dimljene nogice mix", "p8": "Panceta", "p9": "Dimljeni vrat (BK)", "p10": "Dimljeni kare (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
    "p13": "Svinjska mast (kanta)", "p14": "Krvavice", "p15": "Pečenice za roštilj", "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
}

# --- 3. PROIZVODI ---
PRODUCTS = [
    {"id": "p1", "price": 9.50, "unit": "kg"}, {"id": "p2", "price": 7.80, "unit": "pc"},
    {"id": "p3", "price": 6.50, "unit": "pc"}, {"id": "p4", "price": 14.20, "unit": "kg"},
    {"id": "p5", "price": 17.50, "unit": "kg"}, {"id": "p6", "price": 3.80, "unit": "kg"},
    {"id": "p7", "price": 4.50, "unit": "kg"}, {"id": "p8", "price": 16.90, "unit": "kg"},
    {"id": "p9", "price": 12.50, "unit": "kg"}, {"id": "p10", "price": 13.50, "unit": "kg"},
    {"id": "p11", "price": 15.00, "unit": "kg"}, {"id": "p12", "price": 18.00, "unit": "kg"},
    {"id": "p13", "price": 10.00, "unit": "pc"}, {"id": "p14", "price": 9.00, "unit": "kg"},
    {"id": "p15", "price": 10.50, "unit": "kg"}, {"id": "p16", "price": 8.50, "unit": "kg"},
    {"id": "p17", "price": 5.00, "unit": "pc"}, {"id": "p18", "price": 9.00, "unit": "kg"}
]

# --- 4. LOGIKA APLIKACIJE ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")

col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # TRGOVINA
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        for i, p in enumerate(PRODUCTS):
            with (c1 if i % 2 == 0 else c2):
                st.subheader(T[p["id"]])
                st.write(f"**{p['price']:.2f} €** / {T['unit_'+p['unit']]}")
                
                curr_val = st.session_state.cart.get(p["id"], 0.0)
                step = 0.5 if p["unit"] == "kg" else 1.0
                
                new_val = st.number_input(f"Količina ({T['unit_'+p['unit']]})", min_value=0.0, step=step, value=float(curr_val), key=f"f_{p['id']}")
                
                if p["unit"] == "kg" and curr_val == 0.0 and new_val == 0.5:
                    new_val = 1.0
                    st.session_state.cart[p["id"]] = 1.0
                    st.rerun()
                elif new_val != curr_val:
                    if new_val > 0:
                        st.session_state.cart[p["id"]] = new_val
                    else:
                        st.session_state.cart.pop(p["id"], None)
                    st.rerun()

    with tabs[1]: st.header(T["horeca_title"]); st.write(T["horeca_text"])
    with tabs[2]: st.header(T["suppliers_title"]); st.write(T["suppliers_text"])
    with tabs[3]: st.header(T["haccp_title"]); st.write(T["haccp_text"])
    with tabs[4]: st.header(T["info_title"]); st.write(T["info_text"])

with col_right:
    st.markdown(f"### {T['cart_title']}")
    ukupan_iznos = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, kolicina in list(st.session_state.cart.items()):
            p_podaci = next(item for item in PRODUCTS if item["id"] == pid)
            sub = kolicina * p_podaci["price"]
            ukupan_iznos += sub
            st.write(f"✅ **{T[pid]}**: {kolicina} {T['unit_'+p_podaci['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    st.markdown(T["note_delivery"])
    
    with st.form("forma_dostave"):
        st.metric(label=T["total"], value=f"{ukupan_iznos:.2f} €")
        ime = st.text_input(T["form_name"])
        tel = st.text_input(T["form_tel"])
        drzava = st.text_input(T["form_country"], value="Hrvatska")
        grad = st.text_input(T["form_city"])
        zip_kod = st.text_input(T["form_zip"])
        adresa = st.text_input(T["form_addr"])
        
        posalji = st.form_submit_button(T["btn_order"])
        
        if posalji:
            if ime and tel and adresa and st.session_state.cart:
                stavke = "".join([f"- {T[pid]}: {q} {T['unit_'+next(it['unit'] for it in PRODUCTS if it['id']==pid)]}\n" for pid, q in st.session_state.cart.items()])
                poruka = f"Kupac: {ime}\nTel: {tel}\nAdresa: {adresa}, {zip_kod} {grad}\n\nNarudžba:\n{stavke}\nUkupno: {ukupan_iznos:.2f} €"
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(poruka); msg['Subject'] = f"Narudžba 2026 - {ime}"
                    msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    st.success(T["success"])
                    st.session_state.cart = {}
                    time.sleep(2); st.rerun()
                except:
                    st.error("Greška s mail serverom.")
            else:
                st.error("Popunite polja (*) i dodajte proizvode.")
