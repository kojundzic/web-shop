import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# =================================================================
# 🛡️ TRAJNO ZAKLJUČANA KONFIGURACIJA - KOJUNDŽIĆ SISAK 2026.
# =================================================================

MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- VIŠEJEZIČNI RJEČNIK (USIDRENO: HR, EN, DE) ---
LANG = {
    "HR 🇭🇷": {
        "title": "KOJUNDŽIĆ mesnica i prerada mesa | SISAK 2026.",
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_suppliers": "🚜 DOBAVLJAČI", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA", "nav_lang": "🌍 JEZIK",
        "cart_title": "🛒 Vaša košarica", "cart_empty": "Vaša košarica je trenutno prazna.",
        "total": "Ukupni informativni iznos", "unit_kg": "kg", "unit_pc": "kom",
        "note_vaga": "⚖️ **VAŽNO:** Cijene su točne, ali zbog ručne obrade težina može minimalno odstupati.",
        "note_cod": "🚚 Plaćanje pouzećem",
        "form_title": "📍 PODACI ZA DOSTAVU",
        "fname": "Ime*", "lname": "Prezime*", "tel": "Kontakt telefon*", "city": "Grad/Mjesto*", "addr": "Ulica i kućni broj*",
        "btn_order": "🚀 POŠALJI NARUDŽBU",
        "err_fields": "🛑 NARUDŽBA ODBIJENA: Molimo ispunite sva polja označena zvjezdicom (*).",
        "err_cart": "🛑 NARUDŽBA ODBIJENA: Vaša košarica ne smije biti prazna!",
        "success_msg": "Vaša narudžba je zaprimljena, hvala!",
        "about_txt": "Obitelj Kojundžić već generacijama njeguje tradiciju vrhunske prerade mesa u srcu Siska...",
        "horeca_txt": "Za hotele, restorane i kafiće nudimo posebne uvjete suradnje...",
        "suppliers_txt": "Naša sirovina dolazi isključivo s pašnjaka Banovine i Posavine...",
        "haccp_txt": "Sigurnost hrane nam je na prvom mjestu. Pogoni su usklađeni s HACCP sustavom...",
        "products": ["Dimljeni hamburger", "Dimljeni buncek", "Dimljeni prsni vršci", "Slavonska kobasica", "Domaća salama", "Dimljene kosti", "Dimljene nogice mix", "Panceta", "Dimljeni vrat (BK)", "Dimljeni kare (BK)", "Dimljena pečenica", "Domaći čvarci", "Svinjska mast (kanta)", "Krvavice", "Pečenice za roštilj", "Suha rebra", "Dimljena glava", "Slanina sapunara"]
    },
    "EN 🇬🇧": {
        "title": "KOJUNDŽIĆ Butcher Shop & Processing | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 SUPPLIERS", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US", "nav_lang": "🌍 LANGUAGE",
        "cart_title": "🛒 Your Cart", "cart_empty": "Your cart is currently empty.",
        "total": "Total informative amount", "unit_kg": "kg", "unit_pc": "pcs",
        "note_vaga": "⚖️ **IMPORTANT:** Prices are exact, but weight may vary slightly.",
        "note_cod": "🚚 Cash on Delivery",
        "form_title": "📍 DELIVERY INFORMATION",
        "fname": "First Name*", "lname": "Last Name*", "tel": "Phone*", "city": "City*", "addr": "Street & Number*",
        "btn_order": "🚀 PLACE ORDER",
        "err_fields": "🛑 ORDER REJECTED: Please fill in all required fields (*).",
        "err_cart": "🛑 ORDER REJECTED: Your cart is empty!",
        "success_msg": "Your order has been received, thank you!",
        "about_txt": "The Kojundžić family has been nurturing the tradition of quality meat processing in Sisak...",
        "horeca_txt": "Special terms for hotels, restaurants, and cafes...",
        "suppliers_txt": "Raw materials come exclusively from local pastures...",
        "haccp_txt": "Food safety is our priority. Compliant with HACCP standards...",
        "products": ["Smoked Hamburger", "Smoked Pork Hock", "Smoked Brisket Tips", "Slavonian Sausage", "Homemade Salami", "Smoked Bones", "Smoked Trotters Mix", "Pancetta", "Smoked Neck (Boneless)", "Smoked Loin (Boneless)", "Smoked Pork Tenderloin", "Homemade Pork Rinds", "Lard (Bucket)", "Blood Sausages", "Grilling Sausages", "Dry Ribs", "Smoked Pig Head", "Soap Bacon"]
    },
    "DE 🇩🇪": {
        "title": "KOJUNDŽIĆ Metzgerei & Verarbeitung | SISAK 2026.",
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 HORECA", "nav_suppliers": "🚜 LIEFERANTEN", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS", "nav_lang": "🌍 SPRACHE",
        "cart_title": "🛒 Warenkorb", "cart_empty": "Ihr Warenkorb ist leer.",
        "total": "Gesamtbetrag", "unit_kg": "kg", "unit_pc": "stk",
        "note_vaga": "⚖️ **WICHTIG:** Preise sind korrekt, Gewicht kann variieren.",
        "note_cod": "🚚 Nachnahme",
        "form_title": "📍 LIEFERINFORMATIONEN",
        "fname": "Vorname*", "lname": "Nachname*", "tel": "Telefon*", "city": "Stadt*", "addr": "Straße & Hausnummer*",
        "btn_order": "🚀 BESTELLUNG ABSCHICKEN",
        "err_fields": "🛑 ABGELEHNT: Pflichtfelder (*) ausfüllen.",
        "err_cart": "🛑 ABGELEHNT: Ihr Warenkorb ist leer!",
        "success_msg": "Ihre Bestellung ist eingegangen, danke!",
        "about_txt": "Familie Kojundžić pflegt seit Generationen die Tradition in Sisak...",
        "horeca_txt": "Sonderkonditionen für Hotels und Gastronomie...",
        "suppliers_txt": "Unsere Rohstoffe stammen von lokalen Weiden...",
        "haccp_txt": "Lebensmittelsicherheit nach HACCP-Standard...",
        "products": ["Geräucherter Hamburger", "Geräuchertes Eisbein", "Geräucherte Brustspitzen", "Slawonische Wurst", "Hausgemachte Salami", "Geräucherte Knochen", "Geräucherte Pfoten Mix", "Pancetta", "Geräucherter Nacken", "Geräuchertes Karree", "Geräuchertes Lendenstück", "Hausgemachte Grammeln", "Schweineschmalz", "Blutwurst", "Grillwürste", "Trockenrippen", "Geräucherter Schweinekopf", "Speck"]
    }
}

# --- INICIJALIZACIJA ---
if 'sel_lang_key' not in st.session_state: st.session_state.sel_lang_key = "HR 🇭🇷"
if 'cart' not in st.session_state: st.session_state.cart = {}

st.set_page_config(page_title="Kojundžić Sisak 2026", layout="wide")
T = LANG[st.session_state.sel_lang_key]

# --- IZGLED SUČELJA ---
pop_placeholder = st.empty()
col_left, col_right = st.columns([0.65, 0.35])

with col_left:
    st.header(T["title"])
    # Traka s karticama uključujući Jezik na kraju
    t1, t2, t3, t4, t5, t6 = st.tabs([T["nav_shop"], T["nav_horeca"], T["nav_suppliers"], T["nav_haccp"], T["nav_info"], T["nav_lang"]])
    
    with t1: # TRGOVINA
        st.info(T["note_vaga"])
        c1, c2 = st.columns(2)
        BASE_PRICES = [9.5, 7.8, 6.5, 14.2, 17.5, 3.8, 4.5, 16.9, 12.5, 13.5, 15.0, 18.0, 10.0, 9.0, 10.5, 8.5, 5.0, 9.0]
        UNITS = ["kg", "pc", "pc", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "pc", "kg", "kg", "kg", "pc", "kg"]
        for i in range(18):
            pid = f"p{i+1}"
            with (c1 if i % 2 == 0 else c2):
                st.subheader(T["products"][i])
                st.write(f"**{BASE_PRICES[i]:.2f} €** / {T['unit_'+UNITS[i]]}")
                cur_q = st.session_state.cart.get(pid, 0.0)
                new_q = st.number_input(f"{T['products'][i]}", 0.0, step=(0.5 if UNITS[i]=="kg" else 1.0), value=float(cur_q), key=f"inp_{pid}")
                if new_q != cur_q:
                    if new_q > 0: st.session_state.cart[pid] = new_q
                    else: st.session_state.cart.pop(pid, None)
                    st.rerun()

    with t2: st.write(T["horeca_txt"])
    with t3: st.write(T["suppliers_txt"])
    with t4: st.write(T["haccp_txt"])
    with t5: st.write(T["about_txt"])
    with t6: # JEZIK (Zadnja kartica)
        st.write("### Choose your language / Odaberite jezik / Sprache wählen")
        new_lang = st.radio("Selection:", list(LANG.keys()), index=list(LANG.keys()).index(st.session_state.sel_lang_key), label_visibility="collapsed")
        if new_lang != st.session_state.sel_lang_key:
            st.session_state.sel_lang_key = new_lang
            st.rerun()

with col_right:
    st.markdown(f"### {T['cart_title']}")
    ukupan_iznos = 0.0
    if not st.session_state.cart:
        st.info(T["cart_empty"])
    else:
        for pid, q in list(st.session_state.cart.items()):
            idx = int(pid[1:]) - 1
            sub = q * BASE_PRICES[idx]
            ukupan_iznos += sub
            st.write(f"✅ **{T['products'][idx]}**: {q} = **{sub:.2f} €**")
    
    st.divider()
    st.metric(label=T["total"], value=f"{ukupan_iznos:.2f} €")
    st.warning(T["note_cod"])
    
    with st.form("form_final"):
        st.markdown(f"#### {T['form_title']}")
        f_i = st.text_input(T["fname"]); f_p = st.text_input(T["lname"]); f_t = st.text_input(T["tel"])
        f_g = st.text_input(T["city"]); f_a = st.text_input(T["addr"])
        if st.form_submit_button(T["btn_order"], use_container_width=True):
            if not st.session_state.cart: st.error(T["err_cart"])
            elif not (f_i and f_p and f_t and f_g and f_a): st.error(T["err_fields"])
            else:
                # Slanje maila i prikaz skočnog prozora (20x10 cm)
                detalji = "".join([f"- {T['products'][int(pid[1:])-1]}: {q}\n" for pid, q in st.session_state.cart.items()])
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
                    msg = MIMEText(f"Kupac: {f_i} {f_p}\nTel: {f_t}\nNarudžba:\n{detalji}\nUKUPNO: {ukupan_iznos:.2f} €")
                    msg['Subject'] = f"ORDER 2026: {f_i} {f_p}"; server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
                    st.session_state.cart = {}
                    with pop_placeholder.container():
                        st.markdown(f"""<style>.ov {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20cm; height: 10cm; background: white; border: 8px solid #ff4b4b; border-radius: 25px; display: flex; justify-content: center; align-items: center; z-index: 999999; box-shadow: 0px 0px 60px rgba(0,0,0,0.6); }} .tx {{ color: #ff4b4b; font-size: 38px; font-weight: bold; text-align: center; padding: 30px; font-family: Arial; }}</style><div class="ov"><div class="tx">{T['success_msg']}</div></div>""", unsafe_allow_html=True)
                    time.sleep(4); pop_placeholder.empty(); st.rerun()
                except Exception as e: st.error(f"Error: {e}")
