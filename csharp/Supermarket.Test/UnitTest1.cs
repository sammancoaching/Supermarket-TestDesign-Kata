using SupermarketReceipt;

namespace Supermarket.Test;

public class Tests
{
    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void TwoNormalItems()
    {
        SupermarketCatalog catalog = new FakeCatalog();
        var toothbrush = new Product("toothbrush", ProductUnit.Each);
        catalog.AddProduct(toothbrush, 0.99);
        var rice = new Product("rice", ProductUnit.Each);
        catalog.AddProduct(rice, 2.99);
        catalog.AddProduct(new Product("apples", ProductUnit.Kilo), 1.99);
        catalog.AddProduct(new Product("cherry tomato box", ProductUnit.Each), 0.69);
        var teller = new Teller(catalog);   
        var shoppingCart = new ShoppingCart();
        
        shoppingCart.AddItem(toothbrush);
        shoppingCart.AddItem(rice);
        Receipt receipt = teller.ChecksOutArticlesFrom(shoppingCart);
        
        Assert.AreEqual(3.98, receipt.GetTotalPrice(), 0.01);
    }    
    
    [Test]
    public void BuyTwoGetOneFree()
    {
        SupermarketCatalog catalog = new FakeCatalog();
        var toothbrush = new Product("toothbrush", ProductUnit.Each);
        catalog.AddProduct(toothbrush, 0.99);
        var teller = new Teller(catalog);   
        var shoppingCart = new ShoppingCart();
        
        shoppingCart.AddItem(toothbrush);
        shoppingCart.AddItem(toothbrush);
        shoppingCart.AddItem(toothbrush);
        teller.AddSpecialOffer(SpecialOfferType.ThreeForTwo, toothbrush, catalog.GetUnitPrice(toothbrush));
        Receipt receipt = teller.ChecksOutArticlesFrom(shoppingCart);
        
        Assert.AreEqual(1.98, receipt.GetTotalPrice(), 0.01);
    }
}