# demo 1: proxy re-encryption
from zerodb.afgh import crypto

def encrypt(key_alice, data_id, data):
    alice = crypto.Key.from_passphrase(key_alice + data_id)
    enc_data = alice.encrypt(data)
    return enc_data

def do_rekey(key_alice, data_id, bob_public_key):
    alice = crypto.Key.from_passphrase(key_alice + data_id)
    re_key = alice.re_key(bob_public_key)
    return re_key.dump()

def re_encrypt(re_key_dump, enc_data):
    re_key = crypto.ReKey.load(re_key_dump)
    rencrypted_data = re_key.reencrypt(enc_data)
    return rencrypted_data;

def decrypt(key_bob, rencrypted_data):
    bob = crypto.Key.from_passphrase(key_bob)
    data = bob.decrypt_re(rencrypted_data)
    return data

# test code
def print_hex(s):
    print ":".join("{0:x}".format(ord(c)) for c in s)

# 1.enc
key_alice = 'key_alice'
data_id = 'data_id_001'
data = 'alice data txt is here'
enc_data = encrypt(key_alice, data_id, data)
print '1. alice encrypt & save data to IPFS (id, data)'
print data_id
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
rencrypted_data = re_encrypt(rekey, enc_data)
print '4. proxy use rekey to provide a data re-encryption (re-encrypted_data)'
print_hex(rencrypted_data)
# 5.decrypt
print '5. bob use private key to decryption data (data)'
data_dec = decrypt(key_bob, rencrypted_data)
print data_dec
assert data_dec == data
