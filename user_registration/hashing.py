from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# for  encrypted password
class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
