import hashlib

message = b"hello world"

sha256 = hashlib.sha256(message).hexdigest()
sha384 = hashlib.sha384(message).hexdigest()
sha512 = hashlib.sha512(message).hexdigest()

print("SHA-256:", sha256)
print("SHA-384:", sha384)
print("SHA-512:", sha512)