include(FetchContent)

# GoogleTest
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG release-1.12.1
)
FetchContent_MakeAvailable(googletest)

set(TEST_NAME supermarket-google-test)
set(SOURCE_FILES main.cpp SuperMarketTest.cpp FakeCatalog.cpp)
add_executable(${TEST_NAME})
target_sources(${TEST_NAME} PRIVATE ${SOURCE_FILES})
target_link_libraries(${TEST_NAME} src gtest)
add_test(NAME ${TEST_NAME} COMMAND ${TEST_NAME})

