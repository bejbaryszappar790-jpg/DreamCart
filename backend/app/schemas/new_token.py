from pydantic import BaseModel, ConfigDict


class New_Token_In(BaseModel):
    refresh_token : str


class New_Token_Out(BaseModel):
    refresh_token : str
    access_token : str
    token_type : str
    model_config = ConfigDict(
        from_attributes = True
    )
