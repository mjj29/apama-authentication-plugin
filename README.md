[![PySys tests](https://github.com/mjj29/apama-authentication-plugin/workflows/Apama/badge.svg)](https://github.com/mjj29/apama-authentication-plugin/actions)
[![Apama version](https://img.shields.io/badge/Uses-Apama%20v10.5.3+-blue)](http://www.apamacommunity.com/)

# EPL Authentication Plugin

The standard Apama product can host an HTTP server which provides basic usename/password authentication via HTTP basic and a static password file. This new community plug-in provides a more fully-featured authentication layer for storing hashed and salted passwords using MemoryStore in a persistent but dynamically-updatable fashion. It also provides Base64 and HTTP Basic Authorization header encoding and decoding so that it can replace the static HTTP authentication seamlessly from EPL. Lastly, it provides a session-cache layer to provide authentication tokens which can be stored by web applications in cookies, with automatic session expiry and renewal.

## Supported Apama version

This works with Apama 10.5 or later, on Linux only.

## Building the plugin

In an Apama command prompt run:

    mkdir -p $APAMA_WORK/lib
	 g++ -std=c++11 -o $APAMA_WORK/lib/libAuthenticationPlugin.so -I$APAMA_HOME/include -L$APAMA_HOME/lib -lapclient -I. -shared -lcrypt -fPIC AuthenticationPlugin.cpp

## Running tests

To run the tests for the plugin you will need to use an Apama command prompt to run the tests from within the tests directory:

    pysys run

## Using HTTP basic authentication

The [HTTPBasic](https://mjj29.github.io/apama-authentication-plugin/com/apamax/authentication/HTTPBasic.html) event can be used to parse HTTP Authentication headers. First of all you will need to remove the authentication configuration from your HTTP Basic chain. Secondly you'll need to use your mapping configuration to map the `metadata.http.headers.authorization` item into your event. Once you've done that you can use:

	on all RESTEvent() as re {
		HTTPBasic auth := HTTPBasic.createFromAuth(re.authorization);
		authenticateUser(auth.getUser(), auth.getPassword());
	}

Alternatively, the HTTPBasic event can be used to set the authorization header in an HTTP request:

	HTTPBasic auth := HTTPBasic.createFromCreds(username, password);
	string authHeader := auth.getAuthHeader(); // get the auth header
	Request req := new Request;
	auth.addAuthHeader(req); // alternatively, add it directly to a Request object

## Using the Authentication DB

The [Authentication](https://mjj29.github.io/apama-authentication-plugin/com/apamax/authentication/Authentication.html) event can be configured either in an existing MemoryStore database within your application, or create a dedicated one:

	Authentication auth1 := Authentication.createFromStore(myStore); // Use an existing store object
	Authentication auth2 := Authentication.createFromPath(myPath); // Create a new memory store persisted in the given path

`Authentication` events must first be initialized before use. This is an asynchronous process which returns an identifier. An event will be sent with the matching identifier once initialization is complete:

	on AuthenticationInitialized(auth.initialize()) {
		// auth can now be used
	}

To manage the database use the `addUser`, `removeUser` and `hasUser` functions. To validate a user, use one of the check methods:

	boolean valid := auth.checkUser(username, password); // check from user/password
	boolean valid := auth.checkHeader(authHeader); // check an HTTP authorization header

Users can also be assigned groups which can be checked with the `hasGroup` and `getGroups` actions. 

## Using a session cache

You can also use the [CachedAuthentication](https://mjj29.github.io/apama-authentication-plugin/com/apamax/authentication/CachedAuthentication.html) event to provide a session cache on top of the authentication database. Creating and initializing the authentication database is the same as with the Authentication event, as is user management. The difference is with validation. When validating, use the `checkHeader` method, which returns an `AuthResult` type to handle caching.

	AuthResult result := auth.checkHeader(authHeader);
	if (result.result=AuthResult.AUTH_FAILED) {
		// return a 403 permanent auth failure 
	} else if (result.result=AuthResult.AUTH_REQUIRED) {
		// return a 401 auth required message
	} else if (result.result=AuthResult.TOKEN_EXPIRED) {
		// return a 401 auth required message, to re-auth with password
	} else if (result.result=AuthResult.NEW_TOKEN) {
		// return a 200 with the content and a header providing the token to store and use instead of basic auth
		// result.user contains the authenticated user
	} else if (result.result=AuthResult.AUTH_SUCCEEDED) {
		// return a 200 with the content. Optionally re-send the token in the header
		// result.user contains the authenticated user
	}

The `checkHeader` action on a `CachedAuthentication` will authenticate either an HTTP basic auth header, or the cache token header previously supplied after a `NEW_TOKEN` result

## API documentation

API documentation can be found here: [API documentation](https://mjj29.github.io/apama-authentication-plugin/)

