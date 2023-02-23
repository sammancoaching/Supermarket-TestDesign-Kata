## How to build and run tests written in C++ using Google Test

### Build tests

Assumes current directory is root of Supermarket repository.

    $ mkdir build
    $ cd build
    $ cmake ..
    $ make

### Run test using ctest

    $ cd build
    $ ctest

Use extra verbose to show name of tests.

    $ ctest -VV

### Run test binary

    $ cd build
    $ ./test-googletest/supermarket-google-test

## Google Test documentation

* https://google.github.io/googletest/primer.html#same-data-multiple-tests
* https://google.github.io/googletest/faq.html#CtorVsSetUp