import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. FIKSNA KONFIGURACIJA (SISAK 2026) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. USIDRENI PROŠIRENI TEKSTOVI ---
T = {
    "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
    "title_sub": "OBITELJSKA MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
    "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
    "note_vaga": "⚖️ **VAŽNO:** Cijene proizvoda su točne, dok je ukupni iznos u košarici informativan. Točan iznos znat ćete pri preuzimanju paketa, a mi ćemo se truditi da težina i cijena budu što bliži Vašoj narudžbi.",
    "note_delivery": "🚚 **DOSTAVA:** Proizvode šaljemo dostavom, a plaćate ih pouzećem.",
    "horeca_title": "🏨 HoReCa Partnerstvo: Vrhunska sirovina",
    "horeca_text": "Nudimo namjenski program za restorane i hotele uz veleprodajne cijene i brzu dostavu. Kontakt: [tomislavtomi90@gmail.com](mailto:tomislavtomi90@gmail.com)",
    "suppliers_title": "🚜 Podrijetlo: Banovina, Posavina i Lonjsko polje",
    "suppliers_text": "Svo meso dolazi s domaćih pašnjaka Banovine i Posavine, te rubnih dijelova **Parka prirode Lonjsko polje** gdje tradicionalna ispaša jamči vrhunsku kvalitetu.",
    "haccp_title": "🛡️ HACCP",
    "haccp_text": "Primjenjujemo najstrože higijenske standarde uz potpunu digitalnu sljedivost pod stalnim veterinarskim nadzorom.",
    "info_title": "ℹ️ O nama",
    "info_text": "Obitelj Kojundžić u Sisku čuva vještinu tradicionalne pripreme mesa. 📍 Gradska tržnica Kontroba, Sisak.",
    "form_name": "Ime i Prezime primatelja*", "form_tel": "Kontakt telefon*", "form_country": "Država*", "form_city": "Grad/Mjesto*", "form_addr": "Ulica i kućni broj*",
    "btn_order": "🚀 POŠALJI NARUDŽBU", "success": "NARUDŽBA JE USPJEŠNO PREDANA!", "unit_kg": "kg", "unit_pc": "kom", "total": "Ukupni informativni iznos", "shipping_info": "📍 PODACI ZA DOSTAVU"
}

# --- 3. PROIZVODI ---
PRODUCTS = [
    {"id": "p1", "price": 9.50, "unit": "kg", "name": "Dimljeni hamburger"},
    {"id": "p2", "price": 7.80, "unit": "pc", "name": "Dimljeni buncek"},
    {"id": "p3", "price": 6.50, "unit": "pc", "name": "Dimljeni prsni vršci"},
    {"id": "p4", "price": 14.20, "unit": "kg", "name": "Slavonska kobasica"},
    {"id": "p5", "price": 17.50, "unit": "kg", "name": "Domaća salama"},
    {"id": "p6", "price": 3.80, "unit": "kg", "name": "Dimljene kosti"},
    {"id": "p7", "price": 4.50, "unit": "kg", "name": "Dimljene nogice mix"},
    {"id": "p8", "price": 16.90, "unit": "kg", "name": "Panceta"},
    {"id": "p9", "price": 12.50, "unit": "kg", "name": "Dimljeni vrat (BK)"},
    {"id": "p10", "price": 13.50, "unit": "kg", "name": "Dimljeni kare (BK)"},
    {"id": "p11", "price": 15.00, "unit": "kg", "name": "Dimljena pečenica"},
    {"id": "p12", "price": 18.00, "unit": "kg", "name": "Domaći čvarci"},
    {"id": "p13", "price": 10.00, "unit": "pc", "name": "Svinjska mast (kanta)"},
    {"id": "p14", "price": 9.00, "unit": "kg", "name": "Krvavice"},
    {"id": "p15", "price": 10.50, "unit": "kg", "name": "Pečenice za roštilj"},
    {"id": "p16", "price": 8.50, "unit": "kg", "name": "Suha rebra"},
    {"id": "p17", "price": 5.00, "unit": "pc", "name": "Dimljena glava"},
    {"id": "p18", "price": 9.00, "unit": "kg", "name": "Slanina sapunara"}
]

# INICIJALIZACIJA
if 'cart' not in st.session_state:
    st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")

# Kontejner za skočni prozor (postavljen na vrh radi vidljivosti)
pop_up_zona = st.empty()

col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title_sub"])
    tabs = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"]])
    
    with tabs[0]: # SHOP
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        for i, p in enumerate(PRODUCTS):
            with (c1 if i % 2 == 0 else c2):
                st.subheader(p["name"])
                st.write(f"**{p['price']:.2f} €** / {T['unit_'+p['unit']]}")
                curr_val = st.session_state.cart.get(p["id"], 0.0)
                step = 0.5 if p["unit"] == "kg" else 1.0
                
                new_val = st.number_input(f"Količina ({T['unit_'+p['unit']]})", min_value=0.0, step=step, value=float(curr_val), key=f"f_{p['id']}")
                
                if p["unit"] == "kg":
                    if curr_val == 0.0 and new_val == 0.5:
                        new_val = 1.0
                        st.session_state.cart[p["id"]] = 1.0
                        st.rerun()
                    elif curr_val == 1.0 and new_val == 0.5:
                        new_val = 0.0
                        st.session_state.cart.pop(p["id"], None)
                        st.rerun()
                
                if new_val != curr_val:
                    if new_val > 0: st.session_state.cart[p["id"]] = new_val
                    else: st.session_state.cart.pop(p["id"], None)
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
            st.write(f"✅ **{p_podaci['name']}**: {kolicina} {T['unit_'+p_podaci['unit']]} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{ukupan_iznos:.2f} €")
    st.markdown(T["note_delivery"])
    st.divider()
    
    with st.form("forma_dostave"):
        st.markdown(f"#### {T['shipping_info']}")
        ime = st.text_input(T["form_name"])
        tel = st.text_input(T["form_tel"])
        drzava = st.text_input(T["form_country"], value="Hrvatska")
        grad = st.text_input(T["form_city"])
        adresa = st.text_input(T["form_addr"])
        posalji = st.form_submit_button(T["btn_order"])
        
        if posalji:
            if ime and tel and adresa and st.session_state.cart:
                stavke = "".join([f"- {next(it['name'] for it in PRODUCTS if it['id']==pid)}: {q} {T['unit_'+next(it['unit'] for it in PRODUCTS if it['id']==pid)]}\n" for pid, q in st.session_state.cart.items()])
                
                # --- DRŽAVA UKLJUČENA U NARUDŽBU ---
                poruka = f"Kupac: {ime}\nTel: {tel}\nDržava: {drzava}\nGrad: {grad}\nAdresa: {adresa}\n\nNarudžba:\n{stavke}\nInformativni iznos: {ukupan_iznos:.2f} €"
                
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(poruka)
                    msg['Subject'] = f"Narudžba 2026 - {ime}"
                    msg['From'] = MOJ_EMAIL
                    msg['To'] = MOJ_EMAIL
                    server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
                    server.quit()
                    
                    # 1. Prikaz skočnog prozora (5 sekundi)
                    pop_up_zona.success("### VAŠA NARUDŽBA JE ZAPRIMLJENA, HVALA!")
                    
                    # 2. Prikaz obavijesti u formi (traje dok god traje sleep)
                    st.success(T["success"])
                    
                    # 3. Pražnjenje košarice
                    st.session_state.cart = {}
                    
                    # 4. Tajmer logika
                    time.sleep(5)
                    pop_up_zona.empty() # Briše skočni prozor nakon 5 sekundi
                    time.sleep(5) # Čeka dodatnih 5 sekundi (ukupno 10 za donju obavijest)
                    
                    st.rerun()
                except smtplib.SMTPAuthenticationError:
                    st.error("Google je odbio lozinku. Generirajte novu 'App Password'.")
                except Exception as e:
                    st.error(f"Detalji greške: {e}")
