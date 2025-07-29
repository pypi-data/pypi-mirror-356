eas2cli: Command line client for EAS
------------------------------------

This package contains the command line client to make use of the EIDA Authentication
System deployed at https://geofon.gfz.de/eas2 which will provide you with tokens to
operate with most of the available EIDA web services.

Installation
============

You can install this page by mean of `pip` just executing ::

    $ pip install eas2cli


Usage
=====

You can have a list of available commands and options by executing ::

    $ eas2cli --help
    Usage: eas2cli [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help  Show this message and exit.

    Commands:
      login    Open a webpage to allow the user to login
      logout   Remove the file with tokens
      refresh  Refresh the access and id tokens stored locally
      show     Show the tokens stored locally

The first time you use `eas2cli` you will need to use the `login` command. ::

    $ eas2cli login
    Enter user code "4812-4844" at https://geofon.gfz.de/eas2/device
    Time remaining to get a token  [#-----------------------------------]    5%  00:04:45
    Token saved in default location!

The system will provide you a user code to login through a redirection to the B2ACCESS system in the background,
that will allow you to log in within your institutional realm. As soon as your login is successful the application will
receive a token from EAS, which will be saved in teh default location (i.e. `~/.eidajwt`).

You can see the content of the token with the `show` command. ::

    $ eas2cli show
    access: {'sub': '519-XXXXXXXXXXX-3443', 'iss': 'https://geofon.gfz.de/eas2', 'aud': 'fdsn', 'iat': '2025-05-15T14:10:14', 'exp': '2025-05-15T15:16:54', 'email': 'username@datacenter.org'}
    refresh: 5txjYYYYYYYYYYYYYJd4
    scope: email profile USER_PROFILE eduperson_principal_name sys:scim:read_memberships openid eduperson_unique_id
    id: {'iss': 'https://geofon.gfz.de/eas2', 'sub': '519-XXXXXXXXXXX-3443', 'aud': 'eas', 'exp': '2025-05-15T15:10:13', 'iat': '2025-05-15T14:10:13'}
    token_type: Bearer
    expires_in: 4000

The token will not be validated when you show it, but you can do it with the `--validate` option. ::

    $ eas2cli show --validate
    access: {'sub': '519-XXXXXXXXXXX-3443', 'iss': 'https://geofon.gfz.de/eas2', 'aud': 'fdsn', 'iat': '2025-05-15T14:10:14', 'exp': '2025-05-15T15:16:54', 'email': 'javier@gfz.de'}
    refresh: 5txjYYYYYYYYYYYYYJd4
    scope: email profile USER_PROFILE eduperson_principal_name sys:scim:read_memberships openid eduperson_unique_id
    id: {'iss': 'https://geofon.gfz.de/eas2', 'sub': '519-XXXXXXXXXXX-3443', 'aud': 'eas', 'exp': '2025-05-15T15:10:13', 'iat': '2025-05-15T14:10:13'}
    token_type: Bearer
    expires_in: 4000

In the `expires_in` field you can see how many seconds the token will be valid. The expiration can be seen in
the `exp` attribute of the access (or ID) token. After that moment you can get a new access token by means of
the `refresh` command. ::

    $ eas2cli refresh

If you show the new tokens you will see that the expiration time is later than the original one. ::

    $ eas2cli show --validate
    access: {'sub': '519-XXXXXXXXXXX-3443', 'iss': 'https://geofon.gfz.de/eas2', 'aud': 'fdsn', 'iat': '2025-05-15T14:11:01', 'exp': '2025-05-15T15:17:41', 'email': 'javier@gfz.de'}
    refresh: 5txjYYYYYYYYYYYYYJd4
    scope: openid email profile eduperson_unique_id eduperson_principal_name sys:scim:read_memberships USER_PROFILE
    id: {'iss': 'https://geofon.gfz.de/eas2', 'sub': '519-XXXXXXXXXXX-3443', 'aud': 'eas', 'exp': '2025-05-15T15:17:41', 'iat': '2025-05-15T14:11:01'}
    token_type: Bearer
    expires_in: 4000

If at any moment for any reason you would like to login again, just use the `logout` command. All your local tokens
will be removed. ::

    $ eas2cli logout
    If you do this you will need to manually login again to get an access token.
    Do you really want to logout? [y/N]: y
    You have been successfully logged out

    $ eas2cli show
    Error: There is a problem reading your available tokens. Try to log in again.


Integration with other programs
===============================

This package provides 2 ways of reading and using the token from other programs.
The first one is to use the python function `gettoken()`. By means of this, the caller will always receive a valid
access token. In the case that the token is expired, this is refreshed in the background and after that it is
returned (printed) to the caller. ::

    >>> from eas2cli.core import gettoken
    >>> print(gettoken())
    eyJhbGci [...] SldUIn0.eyJzdW [...] 6LmRlIn0.K7VAEN [...] dbyUGQvc


Other option to show your access token is with the command `show` with the option to not decoding it. ::

    $ eas2cli show access --no-decode
    eyJhbGci [...] SldUIn0.eyJzdW [...] 6LmRlIn0.K7VAEN [...] dbyUGQvc

