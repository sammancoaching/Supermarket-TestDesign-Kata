# The Supermarket Test Design Kata

This is a variation of a kata described in https://github.com/emilybache/SupermarketReceipt-Refactoring-Kata. The aim is to introduce a test fixture to avoid code duplication in the arrange parts of the existing unit tests.

## The Supermarket receipt code

The supermarket has a catalog with different types of products (rice, apples, milk, toothbrushes,...). Each product has a price, and the total price of the shopping cart is the total of all the prices of the items. You get a receipt that details the items you've bought, the total price and any discounts that were applied.

The supermarket runs special deals, e.g.
 - Buy two toothbrushes, get one free. Normal toothbrush price is €0.99
 - 20% discount on apples, normal price €1.99 per kilo.
 - 10% discount on rice, normal price €2.49 per bag
 - Five tubes of toothpaste for €7.49, normal price €1.79
 - Two boxes of cherry tomatoes for €0.99, normal price €0.69 per box.

## The existing test cases

There are four test cases that all use the following pattern:
* Populate the supermarket catalog with products.
* Create a cart and add some products to it.
* Create a teller. Optionally add a special offer to the teller.
* Ask the teller to produce a receipt when providing it with the cart.
* Assert that the price on the receipt is correct.

## Introduce a test fixture

The arrange parts of the existing test contain duplicated code. Get rid of the duplicated code by introducing a test fixture.

