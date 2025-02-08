import uuid
from datetime import datetime, timedelta
from models.transaction import Transaction
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc


def create_transaction(db, amount, category_id, comment, user_id):
    try:
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            transaction_id=transaction_id,
            amount=amount,
            comment=comment,
            user_id=user_id,
            category_id=category_id
        )
        db.add(transaction)
        db.flush()
        db.commit()
        return transaction._repr_dict()
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def get_transaction_details(
        db: Session, user_id, transaction_id):
    try:
        transaction_details = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_id == transaction_id).first()
        if transaction_details:
            return transaction_details.repr_dict()
        else:
            return {}
    except Exception as exp:
        print(str(exp))
        raise

def update_transaction(transaction_dict, transaction_id, user_id, db: Session):
    try:
        transaction_details = db.query(Transaction).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_id == transaction_id).first()
        columns = [attr for attr in vars(Transaction) if not attr.startswith('__')]

        if not transaction_details:
            raise Exception('Transaction not found')

        else:
            for key in transaction_dict:
                if key not in ["created_at", "last_updated_at", "user_id"]:
                    if key in columns:
                        setattr(transaction_details, key, transaction_dict[key])

        transaction_details.last_updated_at = datetime.utcnow()
        db.flush()
        db.commit()
        return transaction_details._repr_dict()
    except Exception as exp:
        print(str(exp), "exception occured")
        raise


def get_transactions(
        db: Session, user_id, sort_order, sort_by, categories, start_date, end_date):
    try:
        # Base query with user_id and date range filters
        transactions_query = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        )
        
        # Apply category filter if categories are provided
        if categories:
            transactions_query = transactions_query.filter(
                Transaction.category.in_(categories)
            )
        
        # Apply sorting
        if sort_by and sort_order:
            order_column = getattr(Transaction, sort_by, None)
            if order_column:
                if sort_order == "asc":
                    transactions_query = transactions_query.order_by(asc(order_column))
                elif sort_order == "desc":
                    transactions_query = transactions_query.order_by(desc(order_column))
        
        # Execute the query and fetch results
        transactions = transactions_query.all()
        
        # Convert transactions to a list of dictionaries
        data = [transaction._repr_dict() for transaction in transactions]
        
        return data
    except Exception as exp:
        print(f"Error fetching transactions: {str(exp)}")
        raise

def delete_transaction_details(
        db: Session, user_id, transaction_id):
    try:
        transaction_details = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_id == transaction_id).first()
        if transaction_details:
            transaction_details.is_deleted = True
            db.flush()
            db.commit()
            return True
        else:
            return False
    except Exception as exp:
        print(str(exp))
        raise
