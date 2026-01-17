# --- 2. MASTER PRIJEVODI (AŽURIRANO S PROŠIRENIM TEKSTOVIMA) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🏬 TRGOVINA", "nav_horeca": "🏨 ZA UGOSTITELJE", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA KOJUNDŽIĆ | SISAK 2026.",
        "horeca_title": "Partnerstvo temeljeno na povjerenju i tradiciji",
        "horeca_text": """Kao obiteljski posao, duboko cijenimo rad naših kolega u ugostiteljstvu. Razumijemo da vrhunski tanjur u restoranu ili hotelu počinje s beskompromisnom sirovinom. 

**Što nudimo našim HoReCa partnerima u 2026. godini:**
* **Autentični miris dima:** Posjedujemo vlastite komore za tradicionalno dimljenje na hladnom dimu bukve i graba.
* **Sigurna dostava:** Raspolažemo vlastitim vozilima s kontroliranim temperaturnim režimom (hladnjače).
* **Veleprodajna podrška:** Redovnim partnerima osiguravamo prioritetnu obradu narudžbi i prilagođene rezove mesa.""",
        
        "haccp_title": "Sigurnost hrane: Od polja do Vašeg stola",
        "haccp_text": """U mesnici Kojundžić, higijena je temelj našeg obraza. U 2026. godini primjenjujemo najstrože standarde kontrole kvalitete kako biste bili sigurni u svaki zalogaj.
* **Potpuna sljedivost:** Svaki komad mesa u našoj ponudi ima svoj 'rodni list' – točno znamo s koje farme dolazi.
* **Strogi HACCP protokoli:** Naš moderni pogon u Sisku pod stalnim je nadzorom, uz redovite laboratorijske kontrole i sanitarne standarde koji nadilaze zakonske okvire.""",
        
        "info_title": "Naša priča: Obitelj, Sisak i istinska kvaliteta",
        "info_text": """Smješteni u srcu Siska, obitelj Kojundžić već naraštajima čuva vještinu tradicionalne pripreme mesa. Naša filozofija je jednostavna: Poštuj prirodu i ona će ti uzvratiti najboljim okusima. 
Meso pripremamo polako, uz korištenje isključivo prirodnih začina, bez nepotrebnih aditiva i kemijskih dodataka. Mi ne proizvodimo samo hranu – mi čuvamo baštinu sisačkog kraja.""",
        
        # ... (ostali ključevi: cart_title, note_vaga, note_delivery, btn_order, unit_kg, itd.)
    },
    "EN 🇬🇧": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FOR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ABOUT US",
        "horeca_title": "Partnership Based on Trust and Tradition",
        "horeca_text": """As a family business, we deeply value the work of our colleagues in the hospitality industry. We understand that a top-tier plate in a restaurant or hotel starts with uncompromising raw materials.

**What we offer our HoReCa partners in 2026:**
* **Authentic Smoke Aroma:** We own our chambers for traditional smoking over cold beech and hornbeam smoke.
* **Safe Delivery:** We have our own refrigerated vehicles with controlled temperature regimes.
* **Wholesale Support:** We provide priority order processing and custom meat cuts for regular partners.""",
        
        "haccp_title": "Food Safety: From Field to Your Table",
        "haccp_text": """At Kojundžić Butchery, hygiene is the foundation of our reputation. In 2026, we apply the strictest quality control standards to ensure safety in every bite.
* **Full Traceability:** Every piece of meat has its own 'birth certificate' – we know exactly which farm it comes from.
* **Strict HACCP Protocols:** Our modern facility in Sisak is under constant supervision, with regular laboratory checks and sanitary standards that exceed legal requirements.""",
        
        "info_title": "Our Story: Family, Sisak, and True Quality",
        "info_text": """Located in the heart of Sisak, the Kojundžić family has preserved the skill of traditional meat preparation for generations. Our philosophy is simple: Respect nature, and it will reward you with the best flavors.
We prepare meat slowly, using only natural spices, without unnecessary additives or chemicals. We don't just produce food – we preserve the heritage of the Sisak region.""",
    },
    "DE 🇩🇪": {
        "nav_shop": "🏬 SHOP", "nav_horeca": "🏨 FÜR HORECA", "nav_haccp": "🛡️ HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "horeca_title": "Partnerschaft auf Basis von Vertrauen und Tradition",
        "horeca_text": """Als Familienunternehmen schätzen wir die Arbeit unserer Kollegen im Gastgewerbe sehr. Wir wissen, dass ein erstklassiges Gericht im Restaurant oder Hotel mit kompromisslosen Rohstoffen beginnt.

**Was wir unseren HoReCa-Partnern im Jahr 2026 bieten:**
* **Authentisches Raucharoma:** Wir besitzen eigene Kammern für das traditionelle Kalträuchern über Buchen- und Hainbuchenrauch.
* **Sichere Lieferung:** Wir verfügen über eigene Kühlfahrzeuge mit kontrolliertem Temperaturregime.
* **Großhandelssupport:** Wir garantieren Stammpartnern vorrangige Auftragsbearbeitung und individuelle Fleischschnitte.""",
        
        "haccp_title": "Lebensmittelsicherheit: Vom Feld bis auf Ihren Tisch",
        "haccp_text": """In der Metzgerei Kojundžić ist Hygiene das Fundament unseres Ansehens. Im Jahr 2026 wenden wir strengste Qualitätskontrollstandards an, damit Sie bei jedem Bissen sicher sein können.
* **Vollständige Rückverfolgbarkeit:** Jedes Stück Fleisch hat seine eigene 'Geburtsurkunde' – wir wissen genau, von welchem Bauernhof es stammt.
* **Strenge HACCP-Protokolle:** Unsere moderne Anlage in Sisak steht unter ständiger Aufsicht, mit regelmäßigen Laborkontrollen und Hygienestandards, die über die gesetzlichen Anforderungen hinausgehen.""",
        
        "info_title": "Unsere Geschichte: Familie, Sisak und wahre Qualität",
        "info_text": """Im Herzen von Sisak ansässig, bewahrt die Familie Kojundžić seit Generationen die Kunst der traditionellen Fleischzubereitung. Unsere Philosophie ist einfach: Respektiere die Natur, und sie wird dich mit den besten Aromen belohnen.
Wir bereiten Fleisch langsam zu, verwenden ausschließlich natürliche Gewürze und verzichten auf unnötige Zusatzstoffe oder Chemikalien. Wir produzieren nicht nur Lebensmittel – wir bewahren das Erbe der Region Sisak.""",
    }
}

# --- 5. LOGIKA PRIKAZA RUBRIKA ---
if menu == T["nav_horeca"]:
    st.title(T["horeca_title"])
    st.markdown(T["horeca_text"])
elif menu == T["nav_haccp"]:
    st.title(T["haccp_title"])
    st.markdown(T["haccp_text"])
elif menu == T["nav_info"]:
    st.title(T["info_title"])
    st.markdown(T["info_text"])
