using System;
using System.Collections.Generic;
using System.Text;
using SupermarketReceipt;
using Xunit;
using Assert = Xunit.Assert;

namespace TestSupermarket;

public class SupermarketXUnitTest
{
    
    [Fact]
    public void TwoNormalItems()
    {
        SupermarketCatalog catalog = new FakeCatalog();
        var toothbrush = new Product("toothbrush", ProductUnit.Each);
        catalog.AddProduct(toothbrush, 0.99);
        var rice = new Product("rice", ProductUnit.Each);
        catalog.AddProduct(rice, 2.99);
        var teller = new Teller(catalog);   
        var shoppingCart = new ShoppingCart();
        
        shoppingCart.AddItem(toothbrush);
        shoppingCart.AddItem(rice);
        Receipt receipt = teller.ChecksOutArticlesFrom(shoppingCart);
        
        Assert.Equal(3.98, receipt.GetTotalPrice(), 0.01);
    }
    
    [Fact]
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
        
        Assert.Equal(1.98, receipt.GetTotalPrice(), 0.01);
    }

    [Fact]
    public void XForYDiscount()
    {
        SupermarketCatalog catalog = new FakeCatalog();
        var cherryTomatoes = new Product("cherry tomato box", ProductUnit.Each);
        catalog.AddProduct(cherryTomatoes, 0.69);
        var teller = new Teller(catalog);   
        var shoppingCart = new ShoppingCart();
        
        shoppingCart.AddItem(cherryTomatoes);
        shoppingCart.AddItem(cherryTomatoes);
        teller.AddSpecialOffer(SpecialOfferType.TwoForAmount, cherryTomatoes, 0.99);
        Receipt receipt = teller.ChecksOutArticlesFrom(shoppingCart);
        
        Assert.Equal(0.99, receipt.GetTotalPrice(), 0.01);
    } 
    
    [Fact]
    public void FiveForYDiscount()
    {
        SupermarketCatalog catalog = new FakeCatalog();
        var apples = new Product("apples", ProductUnit.Kilo);
        catalog.AddProduct(apples, 1.99);
        var teller = new Teller(catalog);   
        var shoppingCart = new ShoppingCart();
        
        shoppingCart.AddItemQuantity(apples, 5);
        teller.AddSpecialOffer(SpecialOfferType.FiveForAmount, apples, 6.99);
        Receipt receipt = teller.ChecksOutArticlesFrom(shoppingCart);
        
        Assert.Equal(6.99, receipt.GetTotalPrice(), 0.01);
    } 
}