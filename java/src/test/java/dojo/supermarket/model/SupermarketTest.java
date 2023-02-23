package dojo.supermarket.model;

import org.junit.jupiter.api.Test;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SupermarketTest {

    @Test
    public void twoNormalItems() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product toothbrush = new Product("toothbrush", ProductUnit.EACH);
        catalog.addProduct(toothbrush, 0.99);
        Product rice = new Product("rice", ProductUnit.EACH);
        catalog.addProduct(rice, 2.99);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        // ACT
        cart.addItem(toothbrush);
        cart.addItem(rice);
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        assertEquals(3.98, receipt.getTotalPrice(), 0.01);
    }

    @Test
    public void buyTwoGetOneFree() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product toothbrush = new Product("toothbrush", ProductUnit.EACH);
        catalog.addProduct(toothbrush, 0.99);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        // ACT
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        teller.addSpecialOffer(SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.getUnitPrice(toothbrush));
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        assertEquals(1.98, receipt.getTotalPrice(), 0.01);
    }

    @Test
    public void xForYDiscount() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product cherryTomatoes = new Product("cherry Tomato box", ProductUnit.EACH);
        catalog.addProduct(cherryTomatoes, 0.69);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        // ACT
        cart.addItem(cherryTomatoes);
        cart.addItem(cherryTomatoes);
        teller.addSpecialOffer(SpecialOfferType.TWO_FOR_AMOUNT, cherryTomatoes, 0.99);
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        assertEquals(0.99, receipt.getTotalPrice(), 0.01);
    }

    @Test
    public void FiveForYDiscount() {
        SupermarketCatalog catalog = new FakeCatalog();
        Product apples = new Product("apples", ProductUnit.KILO);
        catalog.addProduct(apples, 1.99);
        Teller teller = new Teller(catalog);
        ShoppingCart cart = new ShoppingCart();

        // ACT
        cart.addItemQuantity(apples, 5);
        teller.addSpecialOffer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99);
        Receipt receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        assertEquals(6.99, receipt.getTotalPrice(), 0.01);
    }
}
