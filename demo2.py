# demo 2: proxy re-encryption + AES (better efficiency for big data file)
import string
import random

# from hashlib import sha256
from Crypto.Cipher import AES
from zerodb.afgh import crypto

BS = 16

def encrypt(key_alice, data_id, data):
    alice = crypto.Key.from_passphrase(key_alice + data_id)
    random_string = id_generator(16)
    enc_data = AES_enc(data, random_string)
    enc_key = alice.encrypt(random_string)
    return enc_key, enc_data

def do_rekey(key_alice, data_id, bob_public_key):
    alice = crypto.Key.from_passphrase(key_alice + data_id)
    re_key = alice.re_key(bob_public_key)
    return re_key.dump()

def re_encrypt(re_key_dump, enc_key):
    re_key = crypto.ReKey.load(re_key_dump)
    rencrypted_key = re_key.reencrypt(enc_key)
    return rencrypted_key;

def decrypt(key_bob, rencrypted_key, enc_data):
    bob = crypto.Key.from_passphrase(key_bob)
    key = bob.decrypt_re(rencrypted_key)
    return AES_dec(enc_data, key)

# supporting funcitons below
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unicode_to_utf8(s):
    if isinstance(s, unicode):
        s = s.encode("utf-8")
    return s

def pad(s):
    length = len(s)
    add = BS - length % BS
    byte = chr(BS - length % BS)
    return s + (add * byte)

def unpad(s):
    length = len(s)
    byte = s[length-1:]
    add = ord(byte)
    return s[:-add]

def AES_enc(raw_text, key):
    raw_text = unicode_to_utf8(raw_text)
    raw_text = pad(raw_text)
    cipher = AES.new(key, AES.MODE_CBC, key)
    return cipher.encrypt(raw_text)

def AES_dec(enc_text, key):
    cipher = AES.new(key, AES.MODE_CBC, key)
    return unpad(cipher.decrypt(enc_text))

# test code
def print_hex(s):
    print ":".join("{0:x}".format(ord(c)) for c in s)

# 1.enc
key_alice = 'key_alice'
data_id = 'data_id_001'
data = 'alice data txt is here'
enc_key, enc_data = encrypt(key_alice, data_id, data)
print '1. alice encrypt & save data to IPFS (id, key, data)'
print data_id
print_hex(enc_key)
print_hex(enc_data)
# 2.request
key_bob = 'key_bob'
bob = crypto.Key.from_passphrase(key_bob)
bob_public_key = bob.dump_pub()
print '2. bob request access with public key (key_bob)'
print_hex(bob_public_key)
# 3.rekey
rekey = do_rekey(key_alice, data_id, bob_public_key)
print '3. alice accept request and send rekey to proxy (rekey)'
print_hex(rekey)
# 4.re-encryption
rencrypted_key = re_encrypt(rekey, enc_key)
print '4. proxy use rekey to provide a key re-encryption (key2)'
print_hex(rencrypted_key)
# 5.decrypt
print '5. bob use key2 + private key to decryption key and data (key, data)'
data_dec = decrypt(key_bob, rencrypted_key, enc_data)
print data_dec
assert data_dec == data
