import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from supermarket.catalog import Product, ProductQuantity, SupermarketCatalog


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


@dataclass(frozen=True)
class Offer:
    offer_type: SpecialOfferType
    product: Product
    argument: float


@dataclass(frozen=True)
class Discount:
    product: Product
    description: str
    discount_amount: float


@dataclass(frozen=True)
class ReceiptItem:
    product: Product
    quantity: float
    price: float
    total_price: float


class Receipt:
    def __init__(self) -> None:
        self._items: List[ReceiptItem] = []
        self._discounts: List[Discount] = []

    def total_price(self) -> float:
        total: float = 0.0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(
        self, product: Product, quantity: Any, price: Any, total_price: Any
    ) -> None:
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount) -> None:
        self._discounts.append(discount)

    @property
    def items(self) -> List[ReceiptItem]:
        return self._items[:]

    @property
    def discounts(self) -> List[Discount]:
        return self._discounts[:]


class ShoppingCart:
    def __init__(self) -> None:
        self._items: List[ProductQuantity] = []
        self._product_quantities: Dict[Product, float] = {}

    @property
    def items(self) -> List[ProductQuantity]:
        return self._items

    def add_item(self, product: Product) -> None:
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self) -> Dict[Product, float]:
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = (
                self._product_quantities[product] + quantity
            )
        else:
            self._product_quantities[product] = quantity

    def handle_offers(
        self,
        receipt: Receipt,
        offers: Dict[Product, Offer],
        catalog: SupermarketCatalog,
    ) -> None:
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = (
                            offer.argument * (quantity_as_int / x)
                            + quantity_as_int % 2 * unit_price
                        )
                        discount_n = unit_price * quantity - total
                        discount = Discount(
                            p, "2 for " + str(offer.argument), -discount_n
                        )

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5

                number_of_x = math.floor(quantity_as_int / x)
                if (
                    offer.offer_type == SpecialOfferType.THREE_FOR_TWO
                    and quantity_as_int > 2
                ):
                    discount_amount = quantity * unit_price - (
                        (number_of_x * 2 * unit_price)
                        + quantity_as_int % 3 * unit_price
                    )
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(
                        p,
                        str(offer.argument) + "% off",
                        -quantity * unit_price * offer.argument / 100.0,
                    )

                if (
                    offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT
                    and quantity_as_int >= 5
                ):
                    discount_total = unit_price * quantity - (
                        offer.argument * number_of_x + quantity_as_int % 5 * unit_price
                    )
                    discount = Discount(
                        p, str(x) + " for " + str(offer.argument), -discount_total
                    )

                if discount:
                    receipt.add_discount(discount)


class Teller:
    def __init__(self, catalog: SupermarketCatalog):
        self.catalog = catalog
        self.offers: Dict[Product, Offer] = {}

    def add_special_offer(
        self, offer_type: SpecialOfferType, product: Product, argument: float
    ) -> None:
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart: ShoppingCart) -> Receipt:
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt
