using NUnit.Framework;
using SupermarketReceipt;
using Assert = NUnit.Framework.Assert;

namespace TestSupermarket;

[TestFixture]
public class SupermarketNUnitTest
{
    private SupermarketCatalog catalog;
    private Teller teller;
    private ShoppingCart cart;
    private Product toothbrush;
    private Product rice;
    private Product cherryTomatoes;
    private Product apples;

    [SetUp]
    public void Setup()
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

    [Test]
    public void TwoNormalItems()
    {
        cart.AddItem(toothbrush);
        cart.AddItem(rice);
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.That(receipt.GetTotalPrice(), Is.EqualTo(3.98).Within(0.01));
    }

    [Test]
    public void BuyTwoGetOneFree()
    {
        cart.AddItem(toothbrush);
        cart.AddItem(toothbrush);
        cart.AddItem(toothbrush);
        teller.AddSpecialOffer(SpecialOfferType.ThreeForTwo, toothbrush, catalog.GetUnitPrice(toothbrush));
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.That(receipt.GetTotalPrice(), Is.EqualTo(1.98).Within(0.01));
    }

    [Test]
    public void XForYDiscount()
    {
        cart.AddItem(cherryTomatoes);
        cart.AddItem(cherryTomatoes);
        teller.AddSpecialOffer(SpecialOfferType.TwoForAmount, cherryTomatoes, 0.99);
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.That(receipt.GetTotalPrice(), Is.EqualTo(0.99).Within(0.01));
    }

    [Test]
    public void FiveForYDiscount()
    {
        cart.AddItemQuantity(apples, 5);
        teller.AddSpecialOffer(SpecialOfferType.FiveForAmount, apples, 6.99);
        Receipt receipt = teller.ChecksOutArticlesFrom(cart);
        Assert.That(receipt.GetTotalPrice(), Is.EqualTo(6.99).Within(0.01));
    }
}