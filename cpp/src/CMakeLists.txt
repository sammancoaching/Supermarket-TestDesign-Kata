set(SOURCE_FILES Discount.cpp
        Product.cpp
        Offer.cpp
        ProductQuantity.cpp
        ReceiptItem.cpp
        Receipt.cpp
        ShoppingCart.cpp
        Teller.cpp
        ReceiptPrinter.cpp)

add_library(src ${SOURCE_FILES})
target_include_directories(src  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})