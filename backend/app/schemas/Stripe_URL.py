from pydantic import BaseModel, ConfigDict

class Stripe_Url_Out(BaseModel):
    stripe_url : str

    model_config = ConfigDict(
        from_attributes = True
    )