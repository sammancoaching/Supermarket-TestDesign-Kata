
import dojo.supermarket.model.Product
import dojo.supermarket.model.SupermarketCatalog

class FakeCatalog : SupermarketCatalog {
    private val products: MutableMap<String?, Product?> = HashMap()
    private val prices: MutableMap<String?, Double?> = HashMap()

    override fun addProduct(product: Product, price: Double) {
        this.products[product.getName()] = product
        this.prices[product.getName()] = price
    }

    override fun getUnitPrice(p: Product): Double {
        return this.prices.get(p.getName())!!
    }
}