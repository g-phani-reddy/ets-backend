from models.user import User
import uuid, bcrypt, jwt
from datetime import datetime, timedelta
from config import Config
from sqlalchemy.orm import Session
from services import category_services

def create_user(user_dict, db: Session):
    try:
        user_id = uuid.uuid4()
        username = user_dict.get("username")

        user_details = get_user_details(username=username, db=db)
        if user_details:
            raise Exception("User already exists")

        encrypted_password = hash_password(user_dict.get("password"))
        new_user = User(
            user_id=user_id,
            first_name=user_dict.get("first_name"),
            last_name=user_dict.get("last_name"),
            contact_num=user_dict.get("contact_num"),
            username=user_dict.get("username"),
            password=encrypted_password)
        
        status = category_services.\
            create_default_categories(user_id=user_id, db=db)
        db.add(new_user)
        db.flush()
        db.commit()
        return new_user._repr_dict()
    except Exception as exp:
        print(str(exp), "exception occured")
        raise

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def get_user_details(
        db: Session, user_id=None, username=None, hide_password=True):
    try:
        if user_id:
            user_details = db.query(User).filter(
                User.user_id == user_id).first()
        elif username:
            user_details = db.query(User).filter(
                User.username == username).first()
        if user_details:
            data = user_details._repr_dict()
            if hide_password:
                del data["password"]
                return data
            else:
                return data
        else:
            return None
    except Exception as exp:
        print(str(exp))
        raise

def generate_access_token(username, password, db: Session):
    try:
        user_details = get_user_details(db=db, username=username, hide_password=False)
        if not user_details:
            raise Exception("User not found")
        res = bcrypt.checkpw(
            password.encode('utf-8'),
            user_details["password"].encode('utf-8'))
        if res:
            expire = datetime.utcnow() + timedelta(
                seconds=Config.JWT_EXPIRY_SECS)
        
            data = {
                "username": user_details["username"],
                "user_id": user_details["user_id"],
                "exp": expire
            }
            encoded_jwt = jwt.encode(data, Config.JWT_KEY, algorithm="HS256")
            return encoded_jwt
        else:
            raise Exception("please provide correct password")
    except Exception as exp:
        print(str(exp))
        raise


def update_user(user_dict, user_id, db: Session):
    try:
        user_details = db.query(User).filter(
                User.user_id == user_id).first()
        columns = [attr for attr in vars(User) if not attr.startswith('__')]

        if not user_details:
            raise Exception('User not found')

        else:
            for key in user_dict:
                if key not in ["password", "user_id"]:
                    if key in columns:
                        setattr(user_details, key, user_dict[key])

        db.flush()
        db.commit()
        return user_details._repr_dict()
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def update_user_password(username, new_passord, db: Session):
    try:
        user_details = db.query(User).filter(
                User.username == username).first()
        if not user_details:
            raise Exception("User not found")
        else:
            new_hash = hash_password(new_passord)
            user_details.password = new_hash
            db.flush()
            db.commit()
            return True
    except Exception as exp:
        print(str(exp), "exception occured")
        raise

