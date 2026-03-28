from typing import Dict
import pytest

from supermarket.catalog import ProductUnit, Product, SupermarketCatalog
from supermarket.teller import SpecialOfferType, ShoppingCart, Receipt, Teller


class FakeCatalog(SupermarketCatalog):
    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}
        self._prices: Dict[str, float] = {}

    def add_product(self, product: Product, price: float) -> None:
        self._products[product.name] = product
        self._prices[product.name] = price

    def unit_price(self, product: Product) -> float:
        return self._prices[product.name]

@pytest.fixture
def toothbrush() -> Product:
	return Product("toothbrush", ProductUnit.EACH)


@pytest.fixture
def rice() -> Product:
	return Product("rice", ProductUnit.EACH)


@pytest.fixture
def cherry_tomatoes() -> Product:
	return Product("cherry Tomato box", ProductUnit.EACH)


@pytest.fixture
def apples() -> Product:
	return Product("apples", ProductUnit.KILO)



@pytest.fixture
def catalog(toothbrush, rice, cherry_tomatoes, apples) -> FakeCatalog:
    catalog = FakeCatalog()
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(rice, 2.99)
    catalog.add_product(cherry_tomatoes, 3.49)
    catalog.add_product(apples, 1.99)
    return catalog

@pytest.fixture
def teller(catalog: FakeCatalog) -> Teller:
    return Teller(catalog)

@pytest.fixture
def cart() -> ShoppingCart:
    return ShoppingCart()

def test_two_normal_items(teller: Teller, cart: ShoppingCart, toothbrush: Product, rice: Product) -> None:
    cart.add_item(toothbrush)
    cart.add_item(rice)

    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(3.98)


def test_buy_two_get_one_for_free(catalog: FakeCatalog, teller: Teller, cart: ShoppingCart, toothbrush: Product) -> None:
    cart.add_item(toothbrush)
    cart.add_item(toothbrush)
    cart.add_item(toothbrush)

    teller.add_special_offer(
        SpecialOfferType.THREE_FOR_TWO,
        toothbrush,
        catalog.unit_price(toothbrush),
    )

    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(1.98)


def test_x_for_y_discount(teller: Teller, cart: ShoppingCart, cherry_tomatoes: Product) -> None:
    cart.add_item(cherry_tomatoes)
    cart.add_item(cherry_tomatoes)

    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)

    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(0.99)


def test_five_for_y_discount(teller: Teller, cart: ShoppingCart, apples: Product) -> None:
    cart.add_item_quantity(apples, 5.0)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99)

    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(6.99)
