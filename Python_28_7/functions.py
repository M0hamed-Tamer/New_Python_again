import hashlib
# دالة لتشفير كلمة المرور (Hashing)
def hash_password(password):
    # نستخدم خوارزمية SHA-256 للتشفير
    return hashlib.sha256(password.encode('utf-8')).hexdigest()