from passlib.context import CryptContext

"""
외부 기능 이용? 테스트하기 힘든거?
유틸 클래스 만드는 거랑 뭐가 다를까?
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)