import bcrypt

class gpEncryption:
    @staticmethod
    def encrypt_password(input):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(input, salt) #was encoded ASCII, but now it needs str, not bytes? O.o
        return hashed #was decoded ASCII, look ^
    
    @staticmethod
    def verify_password(input, hashed):
        return hashed == bcrypt.hashpw(input, hashed)