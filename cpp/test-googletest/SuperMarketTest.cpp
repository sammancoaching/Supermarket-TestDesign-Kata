#include <gtest/gtest.h>

#include "SupermarketCatalog.h"
#include "FakeCatalog.h"
#include "ShoppingCart.h"
#include "Teller.h"


class SuperMarketTests : public ::testing::Test {
public:
    SuperMarketTests() : teller(catalog),
                         toothbrush("toothbrush", ProductUnit::Each),
                         rice("rice", ProductUnit::Each),
                         cherryTomatoes("cherry tomato box", ProductUnit::Each),
                         apples("apples", ProductUnit::Kilo) {
        catalog.addProduct(toothbrush, 0.99);
        catalog.addProduct(rice, 2.99);
        catalog.addProduct(cherryTomatoes, 0.69);
        catalog.addProduct(apples, 1.99);
    }

protected:
    FakeCatalog catalog;
    Teller teller;
    ShoppingCart cart;
    Product toothbrush;
    Product rice;
    Product cherryTomatoes;
    Product apples;
};

TEST_F(SuperMarketTests, TwoNormalItems) {
    //Act
    cart.addItem(toothbrush);
    cart.addItem(rice);
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(3.98, receipt.getTotalPrice());
}

TEST_F(SuperMarketTests, BuyTwoGetOneFree) {
    //Act
    cart.addItem(toothbrush);
    cart.addItem(toothbrush);
    cart.addItem(toothbrush);
    teller.addSpecialOffer(SpecialOfferType::ThreeForTwo, toothbrush, catalog.getUnitPrice(toothbrush));
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(1.98, receipt.getTotalPrice());
}

TEST_F(SuperMarketTests, XForYDiscount) {
    //Act
    cart.addItem(cherryTomatoes);
    cart.addItem(cherryTomatoes);
    teller.addSpecialOffer(SpecialOfferType::TwoForAmount, cherryTomatoes, 0.99);
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(0.99, receipt.getTotalPrice());
}

TEST_F(SuperMarketTests, 5ForYDiscount) {
    //Act
    cart.addItemQuantity(apples, 5);
    teller.addSpecialOffer(SpecialOfferType::FiveForAmount, apples, 6.99);
    Receipt receipt = teller.checksOutArticlesFrom(cart);

    //Assert
    EXPECT_FLOAT_EQ(6.99, receipt.getTotalPrice());
}