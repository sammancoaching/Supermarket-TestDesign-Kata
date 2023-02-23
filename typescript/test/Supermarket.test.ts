import {FakeCatalog} from "./FakeCatalog"
import {Product} from "../src/model/Product"
import {SupermarketCatalog} from "../src/model/SupermarketCatalog"
import {Receipt} from "../src/model/Receipt"
import {ShoppingCart} from "../src/model/ShoppingCart"
import {Teller} from "../src/model/Teller"
import {SpecialOfferType} from "../src/model/SpecialOfferType"
import {ProductUnit} from "../src/model/ProductUnit"
import {expect} from "chai";


describe('Supermarket', function () {

    let catalog: SupermarketCatalog
    let cart: ShoppingCart;
    const toothbrush = new Product("toothbrush", ProductUnit.Each);
    const rice: Product = new Product("rice", ProductUnit.Each);
    const cherryTomatoes: Product = new Product("cherry Tomato box", ProductUnit.Each);
    const apples: Product = new Product("apples", ProductUnit.Kilo);
    let teller: Teller;

    beforeEach(() => {
        catalog = new FakeCatalog();
        cart = new ShoppingCart();

        catalog.addProduct(toothbrush, 0.99);
        catalog.addProduct(rice, 2.99);
        catalog.addProduct(toothbrush, 0.99);
        catalog.addProduct(cherryTomatoes, 0.69);
        catalog.addProduct(apples, 1.99);

        teller = new Teller(catalog);
    })

    it("two normal items", () => {

        // ACT
        cart.addItem(toothbrush);
        cart.addItem(rice)
        const receipt: Receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        expect(receipt.getTotalPrice()).closeTo(3.98, 0.01);

    })


    it("two get one free", () => {

        // ACT
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        cart.addItem(toothbrush);
        teller.addSpecialOffer(SpecialOfferType.ThreeForTwo, toothbrush, catalog.getUnitPrice(toothbrush));
        const receipt: Receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        expect(receipt.getTotalPrice()).closeTo(1.98, 0.01);

    })


    it("x for y discount", () => {

        // ACT
        cart.addItem(cherryTomatoes);
        cart.addItem(cherryTomatoes);
        teller.addSpecialOffer(SpecialOfferType.TwoForAmount, cherryTomatoes, 0.99);
        const receipt: Receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        expect(receipt.getTotalPrice()).closeTo(0.99, 0.01);

    })

    it("five for y discount", () => {

        // ACT
        cart.addItemQuantity(apples, 5);
        teller.addSpecialOffer(SpecialOfferType.FiveForAmount, apples, 6.99);
        const receipt: Receipt = teller.checksOutArticlesFrom(cart);

        // ASSERT
        expect(receipt.getTotalPrice()).closeTo(6.99, 0.01);
    })
});
