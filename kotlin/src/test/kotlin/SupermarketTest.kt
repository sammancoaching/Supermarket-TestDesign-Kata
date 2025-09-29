
import dojo.supermarket.model.*
import org.junit.jupiter.api.BeforeEach
import kotlin.test.Test
import kotlin.test.assertEquals


class SupermarketTest {

    private val catalog: SupermarketCatalog = FakeCatalog()
    private val cart = ShoppingCart()
    private val toothbrush = Product("toothbrush", ProductUnit.EACH)
    private val rice = Product("rice", ProductUnit.EACH)
    private val cherryTomatoes = Product("cherry Tomato box", ProductUnit.EACH)
    private val apples = Product("apples", ProductUnit.KILO)
    private val teller: Teller = Teller(catalog)

    @BeforeEach
    fun setup() {
        catalog.addProduct(toothbrush, 0.99)
        catalog.addProduct(rice, 2.99)
        catalog.addProduct(toothbrush, 0.99)
        catalog.addProduct(cherryTomatoes, 0.69)
        catalog.addProduct(apples, 1.99)
    }

    @Test
    fun twoNormalItems() {
        cart.addItem(toothbrush)
        cart.addItem(rice)

        val receipt = teller.checksOutArticlesFrom(cart)

        assertEquals(3.98, receipt.getTotalPrice(), 0.01)
    }

    @Test
    fun buyTwoGetOneFree() {
        cart.addItem(toothbrush)
        cart.addItem(toothbrush)
        cart.addItem(toothbrush)
        teller.addSpecialOffer(SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.getUnitPrice(toothbrush))

        val receipt = teller.checksOutArticlesFrom(cart)

        assertEquals(1.98, receipt.getTotalPrice(), 0.01)
    }

    @Test
    fun xForYDiscount() {
        cart.addItem(cherryTomatoes)
        cart.addItem(cherryTomatoes)
        teller.addSpecialOffer(SpecialOfferType.TWO_FOR_AMOUNT, cherryTomatoes, 0.99)

        val receipt = teller.checksOutArticlesFrom(cart)

        assertEquals(0.99, receipt.getTotalPrice(), 0.01)
    }

    @Test
    fun FiveForYDiscount() {
        cart.addItemQuantity(apples, 5.0)
        teller.addSpecialOffer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 6.99)

        val receipt = teller.checksOutArticlesFrom(cart)

        assertEquals(6.99, receipt.getTotalPrice(), 0.01)
    }
}