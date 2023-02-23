package dojo.supermarket.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SupermarketTest {

    private final SupermarketCatalog catalog = new FakeCatalog();
    private final ShoppingCart cart = new ShoppingCart();
    private final Product toothbrush = new Product("toothbrush", ProductUnit.EACH);
    private final Product rice = new Product("rice", ProductUnit.EACH);
    private final Product cherryTomatoes = new Product("cherry Tomato box", ProductUnit.EACH);
    private final Product apples = new Product("apples", ProductUnit.KILO);
    private Teller teller;

    @BeforeEach
    public void setup() {
        catalog.addProduct(toothbrush, 0.99);
        catalog.addProduct(rice, 2.99);
        catalog.addProduct(toothbrush, 0.99);
        catalog.addProduct(cherryTomatoes, 0.69);
        catalog.addProduct(apples, 1.99);
        teller = new Teller(catalog);
    }

    @Test
    public void twoNormalItems() {
        cart.addItem(toothbrush);
        cart.addItem(rice);

        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(3.98, receipt.getTotalPrice(), 0.01);
    }

    @Test
    public void buyTwoGetOneFree() {
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        teller.addSpecialOffer(SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.getUnitPrice(toothbrush));

        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(1.98, receipt.getTotalPrice(), 0.01);
    }

    @Test
    public void xForYDiscount() {
        cart.addItem(cherryTomatoes);
        cart.addItem(cherryTomatoes);
        teller.addSpecialOffer(SpecialOfferType.TWO_FOR_AMOUNT, cherryTomatoes, 0.99);

        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(0.99, receipt.getTotalPrice(), 0.01);
    }

    @Test
    public void FiveForYDiscount() {
        cart.addItemQuantity(apples, 5);
        teller.addSpecialOffer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99);

        Receipt receipt = teller.checksOutArticlesFrom(cart);

        assertEquals(6.99, receipt.getTotalPrice(), 0.01);
    }
}
