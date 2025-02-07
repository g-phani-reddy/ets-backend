import uuid
from models.category import Category
from models.transaction import Transaction
from sqlalchemy.orm import Session
from utils.constants import default_category_dict

def create_category(db, category_name, category_desc, type, owner):
    try:
        category_id = str(uuid.uuid4())
        category = Category(
            category_id=category_id,
            name=category_name,
            description=category_desc,
            type=type,
            owner=owner
        )
        db.add(category)
        db.flush()
        db.commit()
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def create_default_categories(user_id, db: Session):
    try:
        for category in default_category_dict:
            create_category(
                db=db,
                category_name=category["name"],
                category_desc=category["description"],
                type="default",
                owner=user_id)
        return True
    except Exception as exp:
        print(str(exp), "exception occured")
        raise



def get_category(category_id, user_id, db: Session):
    try:
        category_obj = db.query(Category).filter(
            Category.category_id == category_id,
            Category.owner == user_id
        ).first()
        if category_obj:
            return category_obj.repr_name()
        return {}
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def delete_category(category_id, user_id, db: Session):
    try:
        transactions_obj = db.query(Transaction).filter(
            Transaction.category_id == category_id,
            Transaction.user_id == user_id
        ).delete()

        category_obj = db.query(Category).filter(
            Category.category_id == category_id,
            Category.owner == user_id
        ).delete()
        
        if category_obj:
            db.commit()
            return True
        
        return False
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def get_categories(user_id, db: Session):
    try:
        data = []
        category_objs = db.query(Category).filter(
            Category.owner == user_id
        ).all()
        for category_obj in category_objs:
            data.append(category_obj.repr_name())
        return data
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def update_category(category_dict, category_id, user_id, db: Session):
    try:
        user_details = db.query(Category).filter(
                Category.category_id == category_id,
                Category.owner == user_id).first()
        columns = [attr for attr in vars(Category) if not attr.startswith('__')]

        if not user_details:
            raise Exception('User not found')

        else:
            for key in category_dict:
                if key not in ["created_at", "category_id"]:
                    if key in columns:
                        setattr(user_details, key, category_dict[key])

        db.flush()
        db.commit()
        return user_details._repr_dict()
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


