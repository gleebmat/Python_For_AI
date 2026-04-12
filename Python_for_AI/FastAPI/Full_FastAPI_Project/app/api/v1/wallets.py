from fastapi import FastAPI, HTTPException, APIRouter
from http import HTTPStatus
from pydantic import BaseModel, Field, field_validator
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest


router = APIRouter()


@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    return wallets_service.get_wallet(wallet_name)


@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    return wallets_service.create_wallet(wallet)
