# zerodb-afgh-pre
AFGH Proxy re-encryption for ZeroDB

Turns out the folks at ZeroDB have implemented a python wrapper around some Java libraries, the most important of which is the NICS’s Cryptography Library which implements the paper entitled “Improved Proxy Re-Encryption Schemes with Applications to Secure Distributed Storage“, or AFGH in short.

run sudo python setup.py install. If running ubuntu, you may get some zope errors which were resolved using: pip install –upgrade zope.interface

We can now use the library. Let’s run through the above scenario using the library:

Import required libraries:
from zerodb.afgh import crypto

Create Bob and my public/private key pairs:
me = crypto.Key.from_passphrase(“my passphrase“)
bob = crypto.Key.from_passphrase(“bob passphrase“)
bob_public_key = bob.dump_pub()

I encrypt my data and put the result into the cloud
my_data = “Hello World”
encrypted_data = me.encrypt(my_data)

Bob contacts me and asks for permission to look at “my_data”
I grab Bob’s public key and issue a re-encryption key to my cloud provider:
re_key = me.re_key(bob.dump_pub())

My cloud provider then grabs my already encrypted data and re-encrypts it, sending it to Bob. At no point does my cloud provider see my decrypted data:
rencrypted_msg = re_key.reencrypt(encrypted_data)

Bob decrypts the re-encrypted message and gets the secret message:
assert bob.decrypt_re(rencrypted_msg) == my_data
