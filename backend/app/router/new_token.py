from fastapi import APIRouter, Depends




router = APIRouter(prefix = "/new_token",
                   tags = ["New_Token"]
                   )

@router.post("/token", response_mode = )
async def create_new_token(input : ):
    