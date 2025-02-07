from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from main import get_db
from schemas.user import (UserCreate,
                           User, BadResponse,
                            UserLogin, UserLoginResponse,
                             UserUpdate, UserPasswordResponse)
from services import user_services, auth_services

user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@user_router.post(
    "/signup", 
    responses={
        200: {"model": User, "description": "User created successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    try:
        user_data = user.dict()
        username = user_data.get("username", None)
        first_name = user_data.get("first_name", None)
        password = user_data.get("password", None)

        if not username or ("@" not in username):
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request. Username is required."},
            )
        if not first_name:
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request. first_name is required."},
            )
        if not password:
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request. password is required."},
            )

        new_user = user_services.create_user(user_data, db)
        del new_user["password"]
        return JSONResponse(
            status_code=201,
            content={"data": new_user}
        )
    except Exception as e:
        print(f"Error creating user: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@user_router.post(
    "/login", 
    responses={
        200: {"model": UserLoginResponse, "description": "User has verified"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def user_login_route(user: UserLogin, db: Session = Depends(get_db)):
    """
    Get access_token to access app.
    """
    try:
        user_data = user.dict()
        username = user_data.get("username", None)
        password = user_data.get("password", None)

        if not username or ("@" not in username):
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request. Username should be valid."},
            )
        if not password:
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request. password is required."},
            )

        access_token = user_services.generate_access_token(
            username=username,
            password=password,
            db = db)
        return JSONResponse(
            status_code = 200,
            content = {"access_token": access_token}
        )
    except Exception as e:
        print(f"Error generating access-token: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@user_router.get(
        "/{user_id}",
        responses={
        200: {"model": User, "description": "Got user details"},
        400: {"model": BadResponse, "description": "Bad Request"},
        },
    dependencies=[Depends(auth_services.validate_token)])
def get_user_route(
        user_id: str,
        db: Session = Depends(get_db),
        user_payload= Depends(auth_services.validate_token)):
    """
    Get a user by ID.
    """
    try:
        user_id_jwt = user_payload.get("user_id")
        if user_id_jwt == user_id: 
            db_user = user_services.get_user_details(user_id=user_id, db=db)
            return JSONResponse(
                status_code=200,
                content={"data": db_user}
            )
        else:
            return JSONResponse(
                status_code=401,
                content={"data": "Unauthorized"}
            )
    except Exception as exp:
        return JSONResponse(
            status_code=500,
            content={"message": str(exp)}
        )


@user_router.put(
    "/", 
    responses={
        200: {"model": User, "description": "User updated successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def update_user_route(
        user: UserUpdate,
        db: Session = Depends(get_db),
        user_payload = Depends(auth_services.validate_token)):
    """
    Update user details.
    """
    try:
        user_id = user_payload.get("user_id")

        user_data = user.dict()
        update_dict = {}
        update_dict["first_name"] = user_data.get("first_name", None)
        update_dict["last_name"] = user_data.get("last_name", None)
        update_dict["contact_num"] = user_data.get("contact_num", None)

        user = user_services.update_user(update_dict, user_id, db)
        return JSONResponse(
            status_code=200,
            content={"data": user}
        )
    except Exception as e:
        print(f"Error creating user: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@user_router.post(
    "/password", 
    responses={
        200: {"model": UserPasswordResponse, "description": "User password updated successfully"},
        400: {"model": BadResponse, "description": "Validation error"},
    },)
async def update_user_password_route(
        user: UserUpdate,
        db: Session = Depends(get_db),
        user_payload = Depends(auth_services.validate_token)):
    """
    Update user password.
    """
    try:
        user_data = user.dict()
        username = user_data.get("username")
        password = user_data.get("password")

        if user_payload.get("username") != username:
            return JSONResponse(
            status_code=200,
            content={"message": "Unauthorized"}
        )

        status = user_services.update_user_password(username, password, db)
        if status:
            return JSONResponse(
                status_code=200,
                content={"message": "sucessfully updated password"}
            )
    except Exception as e:
        print(f"Error creating user: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )
