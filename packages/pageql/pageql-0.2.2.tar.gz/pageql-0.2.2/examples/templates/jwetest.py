from jwcrypto import jwk, jwe
import json

from authlib.jose import JsonWebEncryption
import os, json

claims = {
    "sub": "user-123",
    "scope": ["read", "write"],
    "iat": 1717230000               # Unix time, e.g. 2024-06-01 T00:00Z
}
payload = json.dumps(claims).encode()

key = jwk.JWK.generate(kty='oct', size=256)
key_thumb = key.thumbprint()        # deterministic JWK thumbprint
key.update(kid=key_thumb)           # embed into key object


jwetoken = jwe.JWE(
    plaintext=payload,
    protected={
        "alg": "A256KW",            # AES-KeyWrap using the 256-bit key above
        "enc": "A256GCM",           # AES-256-GCM content encryption
        "kid": key_thumb,
        "typ": "JWE"
    }
)
jwetoken.add_recipient(key)
compact = jwetoken.serialize(compact=True)
print("Compact JWE:\n", compact)

received = compact                      # token from the wire
token = jwe.JWE()
token.deserialize(received, key=key)    # key selection by kid is automatic
print("Decrypted claims:", json.loads(token.payload))

from authlib.jose import JsonWebEncryption
import os, json

jwe = JsonWebEncryption()

# 256-bit random key.  "dir" means we use it directly (no wrapping part).
key = os.urandom(32)

header = {"alg": "dir", "enc": "A256GCM"}

ciphertext = jwe.serialize_compact(header, json.dumps(claims).encode(), key)
print("Authlib ciphertext:", ciphertext)
print("Authlib decrypt:", json.loads(jwe.deserialize_compact(ciphertext, key)["payload"]))