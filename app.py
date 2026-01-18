import streamlit as st
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Final
from datetime import datetime

# =================================================================
# 1. DOMAIN LAYER (Entiteti i Poslovna Pravila)
# =================================================================

@dataclass(frozen=True)
class OrderItem:
    product_name: str
    quantity: float

@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    phone: str
    address: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

@dataclass(frozen=True)
class Order:
    customer: Customer
    items: List[OrderItem]
    timestamp: datetime = field(default_factory=datetime.now)

    def is_valid(self) -> bool:
        return len(self.items) > 0 and all(i.quantity > 0 for i in self.items)

# =================================================================
# 2. PORTS (Sučelja / Ugovori)
# =================================================================

class MessagingProvider(ABC):
    @abstractmethod
    def send_order(self, order: Order) -> bool:
        """Šalje detalje narudžbe primatelju."""
        pass

# =================================================================
# 3. APPLICATION LAYER (Use Cases - Poslovna Logika)
# =================================================================

class OrderProcessor:
    """
    Središnja logika koja ne ovisi o tehnologijama (Streamlit, SMTP).
    Provodi 'Dependency Injection' putem konstruktora.
    """
    def __init__(self, messenger: MessagingProvider):
        self._messenger = messenger

    def process_new_order(self, customer: Customer, cart_items: Dict[str, float]) -> bool:
        # Transformacija sirovih podataka u domenske objekte
        items = [OrderItem(name, qty) for name, qty in cart_items.items() if qty > 0]
        order = Order(customer=customer, items=items)

        if not order.is_valid():
            return False

        return self._messenger.send_order(order)

# =================================================================
# 4. INFRASTRUCTURE LAYER (Adapteri / Implementacije)
# =================================================================

class GmailSmtpAdapter(MessagingProvider):
    """Implementacija slanja obavijesti putem Gmail SMTP servisa."""
    
    def __init__(self, config: Dict[str, Any]):
        self._config = config

    def send_order(self, order: Order) -> bool:
        try:
            items_list = "\n".join([f"🥩 {i.product_name}: {i.quantity} kg" for i in order.items])
            content = (
                f"NOVA NARUDŽBA - SISAK 2026\n"
                f"{'='*30}\n"
                f"KLIJENT: {order.customer.full_name}\n"
                f"TELEFON: {order.customer.phone}\n"
                f"ADRESA: {order.customer.address}\n"
                f"VRIJEME: {order.timestamp.strftime('%d.%m.%Y. %H:%M')}\n"
                f"{'='*30}\n"
                f"STAVKE:\n{items_list}\n"
                f"{'='*30}"
            )

            msg = MIMEText(content)
            msg['Subject'] = f"Narudžba: {order.customer.full_name}"
            msg['From'] = self._config["EMAIL"]
            msg['To'] = self._config["EMAIL"]

            with smtplib.SMTP(self._config["SMTP_SERVER"], self._config["SMTP_PORT"]) as server:
                server.starttls()
                server.login(self._config["EMAIL"], self._config["PASS"])
                server.sendmail(self._config["EMAIL"], self._config["EMAIL"], msg.as_string())
            return True
        except Exception as e:
            st.error(f"Kritična greška u infrastrukturi: {e}")
            return False

# =================================================================
# 5. UI LAYER (Streamlit Presentation)
# =================================================================

# --- Konfiguracija i Konstante ---
CONFIG: Final = {
    "EMAIL": "tomislavtomi90@gmail.com",
    "PASS": "czdx ndpg owzy wgqu",
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "YEAR": 2026
}

PRODUCTS: Final = [
    "Dimljeni hamburger", "Dimljeni buncek", "Slavonska kobasica", 
    "Domaći čvarci", "Panceta", "Svinjska mast", "Dimljena glava"
]

def init_app():
    """Inicijalizacija servisa i stanja."""
    st.set_page_config(page_title="Kojundžić Mesnica 2026", layout="wide")
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    
    # Sastavljanje sustava (Composition Root)
    messenger = GmailSmtpAdapter(CONFIG)
    return OrderProcessor(messenger)

def render_ui(processor: OrderProcessor):
    st.title(f"🏬 KOJUNDŽIĆ Mesnica | Sisak {CONFIG['YEAR']}.")
    
    # --- Glavni dio: Katalog proizvoda ---
    cols = st.columns(len(PRODUCTS) // 2 + 1)
    for i, prod in enumerate(PRODUCTS):
        with cols[i % len(cols)]:
            st.subheader(prod)
            qty = st.number_input(f"kg", min_value=0.0, step=0.5, key=f"q_{prod}")
            if st.button(f"Dodaj {prod}", key=f"b_{prod}"):
                if qty > 0:
                    st.session_state.cart[prod] = qty
                    st.toast(f"Dodano: {prod} ({qty} kg)")

    # --- Sidebar: Košarica i Checkout ---
    st.sidebar.header("🛒 Vaša Narudžba")
    if not st.session_state.cart:
        st.sidebar.info("Košarica je prazna.")
    else:
        for p, q in list(st.session_state.cart.items()):
            if q > 0:
                st.sidebar.write(f"**{p}**: {q} kg")
        
        if st.sidebar.button("🗑️ Isprazni košaricu"):
            st.session_state.cart = {}
            st.rerun()

        st.sidebar.divider()

        with st.sidebar.form("order_form"):
            st.write("### Podaci za dostavu")
            fn = st.text_input("Ime*")
            ln = st.text_input("Prezime*")
            tel = st.text_input("Telefon*")
            adr = st.text_input("Adresa*")
            
            if st.form_submit_button("POŠALJI NARUDŽBU"):
                if all([fn, ln, tel, adr]):
                    client = Customer(first_name=fn, last_name=ln, phone=tel, address=adr)
                    if processor.process_new_order(client, st.session_state.cart):
                        st.success("Narudžba poslana! 🚀")
                        st.session_state.cart = {}
                        st.balloons()
                    else:
                        st.error("Došlo je do greške. Provjerite košaricu.")
                else:
                    st.warning("Molimo popunite sva polja označena zvjezdicom (*).")

# =================================================================
# ENTRY POINT
# =================================================================

if __name__ == "__main__":
    app_processor = init_app()
    render_ui(app_processor)
