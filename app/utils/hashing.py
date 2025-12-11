from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

class Hash:
    @staticmethod
    def hash_password(password: str):
        truncated_password = password[:72]
        return pwd_context.hash(truncated_password)
    

    @staticmethod
    def verify(plain_password: str, hashed_password:str):
        truncated_password = plain_password[:72]
        return pwd_context.verify(truncated_password, hashed_password)
    