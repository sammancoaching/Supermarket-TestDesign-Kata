using SupermarketReceipt;
using Xunit;
using Assert = Xunit.Assert;

namespace TestSupermarket;

public class SupermarketXUnitTest
{
    private readonly SupermarketCatalog catalog;
    private readonly Teller teller;
    private readonly ShoppingCart cart;
    private readonly Product toothbrush;
    private readonly Product rice;
    private readonly Product cherryTomatoes;
    private readonly Product apples;

    public SupermarketXUnitTest()
    {
        catalog = new FakeCatalog();
        teller = new Teller(catalog);
        cart = new ShoppingCart();
        toothbrush = new Product("toothbrush", ProductUnit.Each);
        rice = new Product("rice", ProductUnit.Each);
        cherryTomatoes = new Product("cherry Tomato box", ProductUnit.Each);
        apples = new Product("apples", ProductUnit.Kilo);
        catalog.AddProduct(toothbrush, 0.99);
        catalog.AddProduct(rice, 2.99);
        catalog.AddProduct(cherryTomatoes, 0.69);
        catalog.AddProduct(apples, 1.99);
    }

    [Fact]
    public void TwoNormalItems()
    {
        cart.AddItem(toothbrush);
        cart.AddItem(rice);
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.Equal(3.98, receipt.GetTotalPrice(), 0.01);
    }

    [Fact]
    public void BuyTwoGetOneFree()
    {
        cart.AddItem(toothbrush);
        cart.AddItem(toothbrush);
        cart.AddItem(toothbrush);
        teller.AddSpecialOffer(SpecialOfferType.ThreeForTwo, toothbrush, catalog.GetUnitPrice(toothbrush));
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.Equal(1.98, receipt.GetTotalPrice(), 0.01);
    }

    [Fact]
    public void XForYDiscount()
    {
        cart.AddItem(cherryTomatoes);
        cart.AddItem(cherryTomatoes);
        teller.AddSpecialOffer(SpecialOfferType.TwoForAmount, cherryTomatoes, 0.99);
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.Equal(0.99, receipt.GetTotalPrice(), 0.01);
    }

    [Fact]
    public void FiveForYDiscount()
    {
        cart.AddItemQuantity(apples, 5);
        teller.AddSpecialOffer(SpecialOfferType.FiveForAmount, apples, 6.99);
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.Equal(6.99, receipt.GetTotalPrice(), 0.01);
    }
}