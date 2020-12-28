# EPL Authentication Plugin
Apama EPL Plugin for handling passwords and password verification. Includes support for HTTP Basic headers

## Supported Apama version

This works with Apama 10.5 or later

## Building the plugin

In an Apama command prompt run:

    mkdir -p $APAMA_WORK/lib
	 g++ -std=c++11 -o $APAMA_WORK/lib/libAuthenticationPlugin.so -I$APAMA_HOME/include -L$APAMA_HOME/lib -lapclient -I. -shared -fPIC AuthenticationPlugin.cpp

## Running tests

To run the tests for the plugin you will need to use an Apama command prompt to run the tests from within the tests directory:

    pysys run

## Using HTTP basic authentication

TODO

## Using the Authentication DB

TODO

## API documentation

API documentation can be found here: [API documentation](https://mjj29.github.io/apama-authentication-plugin/)
