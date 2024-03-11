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


def test_two_normal_items() -> None:
    catalog: SupermarketCatalog = FakeCatalog()
    toothbrush: Product = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    rice: Product = Product("rice", ProductUnit.EACH)
    catalog.add_product(rice, 2.99)
    teller: Teller = Teller(catalog)
    cart: ShoppingCart = ShoppingCart()

    cart.add_item(toothbrush)
    cart.add_item(rice)
    receipt: Receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(3.98)


def test_buy_two_get_one_for_free() -> None:
    catalog: SupermarketCatalog = FakeCatalog()
    toothbrush: Product = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    teller: Teller = Teller(catalog)
    cart: ShoppingCart = ShoppingCart()

    cart.add_item(toothbrush)
    cart.add_item(toothbrush)
    cart.add_item(toothbrush)
    teller.add_special_offer(
        SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.unit_price(toothbrush)
    )
    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(1.98)


def test_x_for_y_discount() -> None:
    catalog: SupermarketCatalog = FakeCatalog()
    cherry_tomatoes: Product = Product("cherry Tomato box", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 0.69)
    teller: Teller = Teller(catalog)
    cart: ShoppingCart = ShoppingCart()

    cart.add_item(cherry_tomatoes)
    cart.add_item(cherry_tomatoes)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)
    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(0.99)


def test_five_for_y_discount() -> None:
    catalog: SupermarketCatalog = FakeCatalog()
    apples: Product = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)
    teller: Teller = Teller(catalog)
    cart: ShoppingCart = ShoppingCart()

    cart.add_item_quantity(apples, 5.0)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99)

    receipt: Receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == pytest.approx(6.99)
