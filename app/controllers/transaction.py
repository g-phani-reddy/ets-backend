from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from schemas.transaction import TransactionCreate, Transaction, TransactionUpdate
from schemas.user import BadResponse
from services import auth_services, transaction_services
from main import get_db
from datetime import date

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["transaction"]
)

from enum import Enum


class SortByOptions(str, Enum):
    CREATED_AT = "created_at"
    AMOUNT = "amount"
    CATEGORY = "category_id"
    LAST_UPDATED_AT = "last_updated_at"


@transaction_router.post(
    "/", 
    responses={
        200: {"model": TransactionCreate, "description": "Category created successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def create_transaction_route(
        transaction: TransactionCreate,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Create a new transaction
    """
    try:
        transaction_data = transaction.dict()
        user_id = user_payload["user_id"]

        amount = transaction_data.get("amount", 0.0)
        comment = transaction_data.get("comment", None)
        category_id = transaction_data.get("category_id", None)

        new_transaction = transaction_services.create_transaction(
            amount=amount,
            db = db,
            comment=comment,
            category_id=category_id,
            user_id=user_id
            )
        return JSONResponse(
            status_code=201,
            content={"data": new_transaction}
        )
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@transaction_router.get(
        "/{transaction_id}",
        responses={
        200: {"model": Transaction, "description": "Got the transaction"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def get_transaction_route(
        transaction_id: str,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Get the transaction by id.
    """
    try:
        user_id_jwt = user_payload.get("user_id")
        transaction_dict = transaction_services.\
            get_transaction_details(db, user_id_jwt, transaction_id)
        if transaction_dict:
            return JSONResponse(
                status_code=200,
                content={"data": transaction_dict}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"data": "Transaction not found"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )


@transaction_router.put(
    "/", 
    responses={
        200: {"model": Transaction, "description": "Transaction updated successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def update_transaction_route(
        transaction: TransactionUpdate,
        db: Session = Depends(get_db),
        user_payload = Depends(auth_services.validate_token)):
    """
    Update transaction details.
    """
    try:
        user_id = user_payload.get("user_id")

        transaction_data = transaction.dict()
        if not "transaction_id" in transaction_data:
            return {"message": 'catgeory_id is required'}, 400
        
        transaction_id = transaction_data["transaction_id"]
        update_dict = {}
        update_dict["comment"] = transaction_data.get("comment", None)
        update_dict["category_id"] = transaction_data.get("category_id", None)
        update_dict["amount"] = transaction_data.get("amount", None)

        transaction = transaction_services.update_transaction(
            update_dict, transaction_id, user_id, db)
        return JSONResponse(
            status_code=200,
            content={"data": transaction}
        )
    except Exception as e:
        print(f"Error creating user: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@transaction_router.get(
        "/",
        responses={
        200: {"model": Transaction, "description": "Got the transactions"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def get_transactions_route(
        start_date: date = Query(None, description="Start date for filtering transactions"),
        end_date: date = Query(None, description="End date for filtering transactions"),
        categories = Query([], description="List of Categories"),
        sort_by: SortByOptions = Query(None, description="Sort transactions by a specific field"),
        sort_order: str = Query("asc", description="Sort order (asc or desc)", regex="^(asc|desc)$"),
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Get the categories.
    """
    try:
        user_id_jwt = user_payload.get("user_id")

        if not start_date and end_date:
            return {"message": "start-date and end-date are required"}, 400
        if not sort_by:
            sort_by = "asc"
        if not sort_order:
            sort_order = "transaction_id"

        transactions_data = transaction_services.\
            get_transactions(
                user_id=user_id_jwt,
                start_date=start_date,
                end_date=end_date,
                categories=categories,
                sort_by=sort_by,
                sort_order=sort_order,
                db=db)
        if transactions_data:
            return JSONResponse(
                status_code=200,
                content={"data": transactions_data}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"data": "Transactions not found"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )


@transaction_router.delete(
        "/{transaction_id}",
        responses={
        200: {"model": Transaction, "description": "transaction deleted"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def delete_transaction_route(
        transaction_id: str,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Delete the transaction by id.
    """
    try:
        user_id_jwt = user_payload.get("user_id")
        transaction_dict = transaction_services.\
            delete_transaction_details(db, user_id_jwt, transaction_id)
        if transaction_dict:
            return JSONResponse(
                status_code=200,
                content={"data": transaction_dict}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"data": "Transaction not found"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )
