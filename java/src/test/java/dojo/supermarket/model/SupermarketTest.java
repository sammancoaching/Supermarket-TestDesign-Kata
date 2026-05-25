package dojo.supermarket.model;

import org.junit.jupiter.api.Test;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SupermarketTest {

    @Test
    void TwoNormalItems_TotalPriceIsSumOfIndividualPrices() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product toothbrush = new Product("toothbrush", ProductUnit.EACH);
        catalog.addProduct(toothbrush, 0.99);
        Product rice = new Product("rice", ProductUnit.EACH);
        catalog.addProduct(rice, 2.99);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        cart.addItem(toothbrush);
        cart.addItem(rice);
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(3.98, receipt.getTotalPrice(), 0.01);
    }

    @Test
    void ThreeForTwoOffer_ThirdItemIsFree() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product toothbrush = new Product("toothbrush", ProductUnit.EACH);
        catalog.addProduct(toothbrush, 0.99);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        teller.addSpecialOffer(SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.getUnitPrice(toothbrush));
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(1.98, receipt.getTotalPrice(), 0.01);
    }

    @Test
    void TwoForAmountOffer_PriceIsReducedToBundlePrice() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product cherryTomatoes = new Product("cherry Tomato box", ProductUnit.EACH);
        catalog.addProduct(cherryTomatoes, 0.69);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        cart.addItem(cherryTomatoes);
        cart.addItem(cherryTomatoes);
        teller.addSpecialOffer(SpecialOfferType.TWO_FOR_AMOUNT, cherryTomatoes, 0.99);
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(0.99, receipt.getTotalPrice(), 0.01);
    }

    @Test
    void FiveForAmountOffer_PriceIsReducedToBundlePrice() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product apples = new Product("apples", ProductUnit.KILO);
        catalog.addProduct(apples, 1.99);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        cart.addItemQuantity(apples, 5);
        teller.addSpecialOffer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99);
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(6.99, receipt.getTotalPrice(), 0.01);
    }

}
