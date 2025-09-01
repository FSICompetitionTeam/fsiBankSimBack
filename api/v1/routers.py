from fastapi import APIRouter
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.user import router as user_router
from api.v1.endpoints.account import router as account_router
from api.v1.endpoints.transaction import router as transaction_router
from api.v1.endpoints.banks import router as banks_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(account_router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transaction_router, prefix="/transactions", tags=["transactions"])
api_router.include_router(banks_router, prefix="/banks", tags=["banks"])
