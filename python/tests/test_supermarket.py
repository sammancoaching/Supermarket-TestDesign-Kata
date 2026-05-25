import pytest
from supermarket.catalog import ProductUnit, Product, SupermarketCatalog
from supermarket.teller import SpecialOfferType, ShoppingCart, Receipt, Teller

class FakeCatalog(SupermarketCatalog):
    def __init__(self) -> None:
        self._products = {}
        self._prices = {}

    def add_product(self, product: Product, price: float) -> None:
        self._products[product.name] = product
        self._prices[product.name] = price

    def unit_price(self, product: Product) -> float:
        return self._prices[product.name]

@pytest.fixture
def scenario():
    catalog = FakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    rice = Product("rice", ProductUnit.EACH)
    cherry_tomatoes = Product("cherry Tomato box", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(rice, 2.99)
    catalog.add_product(cherry_tomatoes, 0.69)
    catalog.add_product(apples, 1.99)
    return {
        "catalog": catalog,
        "teller": teller,
        "cart": cart,
        "toothbrush": toothbrush,
        "rice": rice,
        "cherry_tomatoes": cherry_tomatoes,
        "apples": apples
    }

def test_two_normal_items(scenario) -> None:
    cart = scenario["cart"]
    cart.add_item(scenario["toothbrush"])
    cart.add_item(scenario["rice"])
    receipt = scenario["teller"].checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(3.98)

def test_buy_two_get_one_free(scenario) -> None:
    cart = scenario["cart"]
    cart.add_item(scenario["toothbrush"])
    cart.add_item(scenario["toothbrush"])
    cart.add_item(scenario["toothbrush"])
    scenario["teller"].add_special_offer(
        SpecialOfferType.THREE_FOR_TWO, scenario["toothbrush"], scenario["catalog"].unit_price(scenario["toothbrush"])
    )
    receipt = scenario["teller"].checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(1.98)

def test_x_for_y_discount(scenario) -> None:
    cart = scenario["cart"]
    cart.add_item(scenario["cherry_tomatoes"])
    cart.add_item(scenario["cherry_tomatoes"])
    scenario["teller"].add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, scenario["cherry_tomatoes"], 0.99)
    receipt = scenario["teller"].checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(0.99)

def test_five_for_y_discount(scenario) -> None:
    cart = scenario["cart"]
    cart.add_item_quantity(scenario["apples"], 5.0)
    scenario["teller"].add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, scenario["apples"], 6.99)
    receipt = scenario["teller"].checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(6.99)
