from fastapi import APIRouter,Depends
from app.dependencies import comon_parameters

router = APIRouter(
    prefix="/products",
    tags=["商品管理"]
)



@router.get("/")
def get_products(commons: dict = Depends(comon_parameters)):
    return commons