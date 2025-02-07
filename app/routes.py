
from controllers.user import user_router
from controllers.category import category_router
from controllers.transaction import transaction_router

from main import app
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(category_router)
