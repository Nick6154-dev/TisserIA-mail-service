from pydantic import BaseModel


class PersonData(BaseModel):
    fullName: str
    identification: str = ""
    response: str = ""
    period: str = ""
    modePeriod: str = ""
    state: str = ""
    observations: str = ""
    userMail: str = ""
    password: str = ""
    toSend: str
    template_id: int
