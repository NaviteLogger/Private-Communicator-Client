from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes, padding
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# The following function deals with the generation of a key pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    return private_key, public_key

# The following function deals with the serialization of the key pair
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )

# The following function deals with the saving of the private key to a file
def save_private_key(private_key, filename, password):
    with open(filename + "_private_key", "wb") as key_file:
        key_file.write(
            private_key.private_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PrivateFormat.PKCS8,
                encryption_algorithm = serialization.BestAvailableEncryption(password)
            )
        )

# The following function deals with the saving of the public key to a file
def save_public_key(public_key, filename):
    with open(filename + "_public_key", "wb") as key_file:
        key_file.write(public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# The following function deals with the encryption of a message
def encrypt_message(message, recipient_public_key):
    return recipient_public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

# The following function deals with the decryption of a message
def decrypt_message(message, recipient_private_key):
    return recipient_private_key.decrypt(
        message,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
