
import dojo.supermarket.model.*
import kotlin.test.Test
import kotlin.test.assertEquals


class SupermarketTest {

    @Test
    fun twoNormalItems() {
        val catalog: SupermarketCatalog = FakeCatalog()
        val toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.addProduct(toothbrush, 0.99)
        val rice = Product("rice", ProductUnit.EACH)
        catalog.addProduct(rice, 2.99)
        val teller = Teller(catalog)
        val cart = ShoppingCart()

        // ACT
        cart.addItem(toothbrush)
        cart.addItem(rice)
        val receipt = teller.checksOutArticlesFrom(cart)

        // ASSERT
        assertEquals(3.98, receipt.getTotalPrice(), 0.01)
    }


    @Test
    fun buyTwoGetOneFree() {
        val catalog: SupermarketCatalog = FakeCatalog()
        val toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.addProduct(toothbrush, 0.99)
        val teller = Teller(catalog)
        val cart = ShoppingCart()

        // ACT
        cart.addItem(toothbrush)
        cart.addItem(toothbrush)
        cart.addItem(toothbrush)
        teller.addSpecialOffer(SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.getUnitPrice(toothbrush))
        val receipt = teller.checksOutArticlesFrom(cart)

        // ASSERT
        assertEquals(1.98, receipt.getTotalPrice(), 0.01)
    }

    @Test
    fun xForYDiscount() {
        val catalog: SupermarketCatalog = FakeCatalog()
        val cherryTomatoes = Product("cherry Tomato box", ProductUnit.EACH)
        catalog.addProduct(cherryTomatoes, 0.69)
        val teller = Teller(catalog)
        val cart = ShoppingCart()

        // ACT
        cart.addItem(cherryTomatoes)
        cart.addItem(cherryTomatoes)
        teller.addSpecialOffer(SpecialOfferType.TWO_FOR_AMOUNT, cherryTomatoes, 0.99)
        val receipt = teller.checksOutArticlesFrom(cart)

        // ASSERT
        assertEquals(0.99, receipt.getTotalPrice(), 0.01)
    }

    @Test
    fun FiveForYDiscount() {
        val catalog: SupermarketCatalog = FakeCatalog()
        val apples = Product("apples", ProductUnit.KILO)
        catalog.addProduct(apples, 1.99)
        val teller = Teller(catalog)
        val cart = ShoppingCart()

        // ACT
        cart.addItemQuantity(apples, 5.0)
        teller.addSpecialOffer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99)
        val receipt = teller.checksOutArticlesFrom(cart)

        // ASSERT
        assertEquals(6.99, receipt.getTotalPrice(), 0.01)
    }
}