import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (TRAJNO ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. JEZICI I PROŠIRENA LISTA ARTIKALA (180+ STAVKI) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛒 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.", 
        "cart_title": "🛍️ Vaša Košarica", "cart_empty": "Vaša košarica je prazna.",
        "note_vaga": "⚖️ **Napomena:** Cijene su točne, ali konačan iznos ovisi o vaganju proizvoda.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "🚀 POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom",
        "horeca_title": "B2B i Ugostiteljstvo", 
        "horeca_text": "Nudimo uslužnu proizvodnju po vašem receptu, veleprodajne cijene i vlastitu dostavu hladnjačom na području cijele Hrvatske.",
        "haccp_title": "Sigurnost hrane (HACCP)", "haccp_text": "Naša proizvodnja u 2026. udovoljava svim EU standardima. Meso prolazi strogu veterinarsku kontrolu, a procesi prerade su pod stalnim nadzorom.",
        "info_title": "Obiteljska Tradicija Kojundžić",
        "info_text": "Od uzgoja do stola. Meso nabavljamo isključivo od malih proizvođača iz Parka prirode Lonjsko polje i Banovine. Tradicionalno dimljenje na bukovini daje našim proizvodima prepoznatljiv miris i okus.",
        "p1": "Dimljeni hamburger", "p2": "Dimljeni buncek", "p3": "Dimljeni prsni vršci",
        "p4": "Slavonska kobasica", "p5": "Domaća salama", "p6": "Dimljene kosti",
        "p7": "Dimljene nogice mix", "p8": "Panceta (Vrhunska)", "p9": "Dimljeni vrat (BK)",
        "p10": "Dimljeni kremenadl (BK)", "p11": "Dimljena pečenica", "p12": "Domaći čvarci",
        "p13": "Svinjska mast (kanta)", "p14": "Krvavice (domaće)", "p15": "Pečenice za roštilj",
        "p16": "Suha rebra", "p17": "Dimljena glava", "p18": "Slanina sapunara"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 B2B", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER KOJUNDŽIĆ | 2026.", "cart_title": "🛍️ Your Cart", "cart_empty": "Your cart is empty.",
        "total": "Total approx.", "btn_order": "🚀 CONFIRM ORDER", "success": "Thank you! Order received.",
        "note_vaga": "⚖️ Final price confirmed after weighing.", "unit_kg": "kg", "unit_pc": "pcs",
        "p1": "Smoked bacon", "p2": "Smoked hock", "p12": "Pork rinds", "p13": "Lard", "p8": "Pancetta"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛒 SHOP", "nav_horeca": "🏨 B2B", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI KOJUNDŽIĆ | 2026.", "cart_title": "🛍️ Warenkorb", "cart_empty": "Warenkorb ist leer.",
        "total": "Gesamt ca.", "btn_order": "🚀 BESTELLEN", "success": "Vielen Dank!",
        "note_vaga": "⚖️ Endpreis nach dem Wiegen.", "unit_kg": "kg", "unit_pc": "Stk",
        "p1": "Geräucherter Speck", "p2": "Stelze", "p12": "Grieben", "p13": "Schweineschmalz", "p8": "Pancetta"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 3. LOGIKA ZA EMAIL ---
def posalji_email(ime, telefon, grad, adr, detalji, ukupno, jezik, country, ptt):
    predmet = f"🔴 NOVA NARUDŽBA 2026: {ime}"
    tijelo = f"KUPAC: {ime}\nTEL: {telefon}\nADRESA: {adr}, {ptt} {grad}, {country}\nJEZIK: {jezik}\n\nSTAVKE:\n{detalji}\nUKUPNO: {ukupno:.2f} €\n\n--- Kraj poruke ---"
    msg = MIMEText(tijelo)
    msg['Subject'] = predmet
    msg['From'] = MOJ_EMAIL
    msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Greška sustava: {e}")
        return False

# --- 4. DIZAJN ---
st.markdown("""<style>
    .brand-name { color: #8B0000; font-size: 38px; font-weight: 900; text-align: center; margin-bottom:0; }
    .brand-sub { color: #444; font-size: 14px; text-align: center; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
    .product-card { background: white; border-radius: 10px; padding: 12px; border: 1px solid #eee; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s; }
    .product-card:hover { border-color: #8B0000; }
    .qty-display { font-size: 18px; font-weight: bold; color: #8B0000; text-align: center; padding: 5px; }
    div.stButton > button:first-child { background-color: #8B0000; color: white; border-radius: 5px; border: none; width: 100%; }
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 5. NAVIGACIJA ---
izabrani_jezik = st.sidebar.selectbox("Language / Jezik", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
choice = st.sidebar.radio("Meni", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

# --- 6. TRGOVINA ---
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)
    
    col_proizvodi, col_kosarica = st.columns([0.65, 0.35])
    
    # Lista 18 artikala s cijenama
    proizvodi = [
        {"id": 1, "name": T.get("p1", "Artikl"), "price": 12.0}, {"id": 2, "name": T.get("p2", "Artikl"), "price": 8.0},
        {"id": 3, "name": T.get("p3", "Artikl"), "price": 9.5}, {"id": 4, "name": T.get("p4", "Artikl"), "price": 16.0},
        {"id": 5, "name": T.get("p5", "Artikl"), "price": 25.0}, {"id": 6, "name": T.get("p6", "Artikl"), "price": 3.0},
        {"id": 7, "name": T.get("p7", "Artikl"), "price": 3.0}, {"id": 8, "name": T.get("p8", "Artikl"), "price": 17.5},
        {"id": 9, "name": T.get("p9", "Artikl"), "price": 15.0}, {"id": 10, "name": T.get("p10", "Artikl"), "price": 15.0},
        {"id": 11, "name": T.get("p11", "Artikl"), "price": 22.0}, {"id": 12, "name": T.get("p12", "Artikl"), "price": 11.0},
        {"id": 13, "name": T.get("p13", "Artikl"), "price": 18.0}, {"id": 14, "name": T.get("p14", "Artikl"), "price": 10.0},
        {"id": 15, "name": T.get("p15", "Artikl"), "price": 11.5}, {"id": 16, "name": T.get("p16", "Artikl"), "price": 14.5},
        {"id": 17, "name": T.get("p17", "Artikl"), "price": 5.0}, {"id": 18, "name": T.get("p18", "Artikl"), "price": 7.0}
    ]

    with col_proizvodi:
        for i in range(0, len(proizvodi), 3):
            red = st.columns(3)
            for j in range(3):
                if i + j < len(proizvodi):
                    p = proizvodi[i + j]
                    with red[j]:
                        st.markdown(f'<div class="product-card"><h4>{p["name"]}</h4><p>{p["price"]:.2f} €</p></div>', unsafe_allow_html=True)
                        c1, c2, c3 = st.columns([1, 1, 1])
                        if c1.button("➖", key=f"m_{p['id']}"):
                            if st.session_state.cart.get(p['id'], 0) > 0:
                                st.session_state.cart[p['id']] -= 1
                                st.rerun()
                        c2.markdown(f'<div class="qty-display">{st.session_state.cart.get(p["id"], 0)}</div>', unsafe_allow_html=True)
                        if c3.button("➕", key=f"p_{p['id']}"):
                            st.session_state.cart[p['id']] = st.session_state.cart.get(p['id'], 0) + 1
                            st.rerun()

    with col_kosarica:
        st.subheader(T["cart_title"])
        ukupno, lista_za_email = 0.0, ""
        for p in proizvodi:
            kolicina = st.session_state.cart.get(p["id"], 0)
            if kolicina > 0:
                iznos = kolicina * p['price']
                ukupno += iznos
                st.write(f"🏷️ **{p['name']}** - {kolicina}x = {iznos:.2f} €")
                lista_za_email += f"- {p['name']} (Količina: {kolicina}, Iznos: {iznos:.2f} €)\n"
        
        if ukupno > 0:
            st.divider()
            st.markdown(f"### {T['total']}: **{ukupno:.2f} €**")
            st.info(T["note_vaga"])
            with st.form("forma_narudzbe"):
                ime = st.text_input(T["form_name"])
                tel = st.text_input(T["form_tel"])
                adr = st.text_input(T["form_addr"])
                grad = st.text_input(T["form_city"])
                ptt = st.text_input(T["form_zip"])
                zemlja = st.text_input(T["form_country"])
                
                if st.form_submit_button(T["btn_order"]):
                    if ime and tel and grad and adr:
                        if posalji_email(ime, tel, grad, adr, lista_za_email, ukupno, izabrani_jezik, zemlja, ptt):
                            st.success(T["success"])
                            st.session_state.cart = {}
                            time.sleep(3)
                            st.rerun()
                    else:
                        st.warning("Molimo popunite sva polja s oznakom *")
        else:
            st.info(T["cart_empty"])

elif choice == T["nav_horeca"]:
    st.header(T["horeca_title"])
    st.write(T["horeca_text"])
    st.markdown(f"📧 **Kontakt:** {MOJ_EMAIL}")

elif choice == T["nav_haccp"]:
    st.header(T["haccp_title"])
    st.write(T["haccp_text"])

elif choice == T["nav_info"]:
    st.header(T["info_title"])
    st.write(T["info_text"])
