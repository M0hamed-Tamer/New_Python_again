
# from cryptography.fernet import Fernet
# # مفتاح واحد بس
# key = Fernet.generate_key()
# cipher = Fernet(key)

# message = input("Enter The Message: ").encode()

# encrypted = cipher.encrypt(message)

# print(encrypted)

# # ================================

# decrypted = cipher.decrypt(encrypted).decode()
# print(decrypted)
# ==================================
# 1️⃣ فكرة الـ Hybrid Encryption
# زي ما شرحنا قبل كده:

# المفتاح السري (Symmetric Key) بيستخدم لتشفير البيانات نفسها → سريع جدًا.

# المفتاح العام (Asymmetric Key) بيستخدم لتشفير المفتاح السري → آمن لتبادل المفتاح بين طرفين.

# 💡 الفكرة الأساسية:

# تولد مفتاح AES (سري).

# تشفر البيانات بـ AES.

# تشفر مفتاح AES نفسه بمفتاح RSA (عام).

# الطرف التاني يفك مفتاح AES باستخدام مفتاح RSA (خاص).

# يفك البيانات بـ AES.
# =============================================================================/--------------------
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

# -----------------------------
# توليد مفاتيح RSA للطرف المستقبل
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048) #  الطرف المستقبل بيملك المفتاح الخاص
public_key = private_key.public_key()# والمفتاح العام يُعطى للطرف المرسل
# -----------------------------

# -----------------------------
# توليد مفتاح AES (Fernet)
Key = Fernet.generate_key()
cipher = Fernet(Key)

# البيانات اللي عايزين نشفرها
data = b"Main"
encrypted_data = cipher.encrypt(data)
print("Encrypted Data:", encrypted_data)
# -----------------------------

# -----------------------------
# تشفير مفتاح AES بمفتاح RSA العام
encrypted_symmetric_key = public_key.encrypt(
    Key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Encrypted Symmetric Key:\n", encrypted_symmetric_key)
# -----------------------------

# -----------------------------
# فك المفتاح السري بمفتاح RSA الخاص
decrypted_symmetric_key = private_key.decrypt(
    encrypted_symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# فك البيانات باستخدام مفتاح AES
cipher_for_decrypt = Fernet(decrypted_symmetric_key)
decrypted_data = cipher_for_decrypt.decrypt(encrypted_data)
print("Decrypted Data:\n", decrypted_data.decode())
# -----------------------------
# افهم تاني