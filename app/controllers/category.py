from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from main import get_db

from schemas.category import Category, CategoryCreate, CategoryUpdate
from schemas.user import BadResponse
from services import auth_services, category_services

category_router = APIRouter(
    prefix="/category",
    tags=["catgeory"]
)

@category_router.post(
    "/", 
    responses={
        200: {"model": Category, "description": "Category created successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def create_category_route(
        category: CategoryCreate,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Create a new category
    """
    try:
        category_data = category.dict()
        user_id = user_payload["user_id"]

        name = category_data.get("name", None)
        description = category_data.get("description", None)

        if not name or (not description):
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request. name and description are required."},
            )

        new_category = category_services.create_category(
            category_name=name,
            db = db,
            category_desc=description,
            owner=user_id,
            type="custom"
            )
        return JSONResponse(
            status_code=201,
            content={"data": new_category}
        )
    except Exception as e:
        print(f"Error creating category: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@category_router.get(
        "/{category_id}",
        responses={
        200: {"model": Category, "description": "Got the category"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def get_category_route(
        category_id: str,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Get the category by id.
    """
    try:
        user_id_jwt = user_payload.get("user_id")
        category_dict = category_services.\
            get_category(category_id, user_id_jwt, db)
        if category_dict:
            return JSONResponse(
                status_code=200,
                content={"data": category_dict}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"data": "Category not found"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )


@category_router.put(
    "/", 
    responses={
        200: {"model": Category, "description": "Category updated successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def update_category_route(
        category: CategoryUpdate,
        db: Session = Depends(get_db),
        user_payload = Depends(auth_services.validate_token)):
    """
    Update category details.
    """
    try:
        user_id = user_payload.get("user_id")

        category_data = category.dict()
        if not "category_id" in category_data:
            return {"message": 'catgeory_id is required'}, 400
        
        category_id = category_data["category_id"]
        update_dict = {}
        update_dict["name"] = category_data.get("name", None)
        update_dict["description"] = category_data.get("description", None)
        update_dict["type"] = category_data.get("type", None)

        category = category_services.update_category(update_dict, category_id, user_id, db)
        return JSONResponse(
            status_code=200,
            content={"data": category}
        )
    except Exception as e:
        print(f"Error creating user: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@category_router.get(
        "/",
        responses={
        200: {"model": Category, "description": "Got the categories"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def get_categories_route(
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Get the categories.
    """
    try:
        user_id_jwt = user_payload.get("user_id")
        category_data = category_services.\
            get_categories(user_id_jwt, db)
        if category_data:
            return JSONResponse(
                status_code=200,
                content={"data": category_data}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"data": "Categories not found"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )


@category_router.delete(
        "/{category_id}",
        responses={
        200: {"model": Category, "description": "category deleted"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def delete_category_route(
        category_id: str,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Get the category by id.
    """
    try:
        user_id_jwt = user_payload.get("user_id")
        category_dict = category_services.\
            delete_category(category_id, user_id_jwt, db)
        if category_dict:
            return JSONResponse(
                status_code=200,
                content={"message": 'deleted category'}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"data": "Category not found"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )

