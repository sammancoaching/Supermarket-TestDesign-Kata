#include <gtest/gtest.h>

#include "SupermarketCatalog.h"
#include "FakeCatalog.h"
#include "ShoppingCart.h"
#include "Teller.h"

TEST(SuperMarketTest, TwoNormalItems) {
    //Arrange
    auto catalog{FakeCatalog()};
    Product toothbrush("toothbrush", ProductUnit::Each);
    catalog.addProduct(toothbrush, 0.99);
    Product rice("rice", ProductUnit::Each);
    catalog.addProduct(rice, 2.99);
    Teller teller(catalog);
    ShoppingCart cart;

    //Act
    cart.addItem(toothbrush);
    cart.addItem(rice);
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(3.98, receipt.getTotalPrice());
}

TEST(SuperMarketTest, BuyTwoGetOneFree) {
    //Arrange
    auto catalog{FakeCatalog()};
    Product toothbrush("toothbrush", ProductUnit::Each);
    catalog.addProduct(toothbrush, 0.99);
    Teller teller(catalog);
    ShoppingCart cart;

    //Act
    cart.addItem(toothbrush);
    cart.addItem(toothbrush);
    cart.addItem(toothbrush);
    teller.addSpecialOffer(SpecialOfferType::ThreeForTwo, toothbrush, catalog.getUnitPrice(toothbrush));
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(1.98, receipt.getTotalPrice());
}

TEST(SuperMarketTest, XForYDiscount) {
    //Arrange
    auto catalog{FakeCatalog()};
    Product cherryTomatoes("cherry tomato box", ProductUnit::Each);
    catalog.addProduct(cherryTomatoes, 0.69);
    Teller teller(catalog);
    ShoppingCart cart;

    //Act
    cart.addItem(cherryTomatoes);
    cart.addItem(cherryTomatoes);
    teller.addSpecialOffer(SpecialOfferType::TwoForAmount, cherryTomatoes, 0.99);
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(0.99, receipt.getTotalPrice());
}

TEST(SuperMarketTest, 5ForYDiscount) {
    //Arrange
    auto catalog{FakeCatalog()};
    Product apples("apples", ProductUnit::Kilo);
    catalog.addProduct(apples, 1.99);
    Teller teller(catalog);
    ShoppingCart cart;

    //Act
    cart.addItemQuantity(apples, 5);
    teller.addSpecialOffer(SpecialOfferType::FiveForAmount, apples, 6.99);
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(6.99, receipt.getTotalPrice());
}