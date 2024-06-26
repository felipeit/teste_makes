from dataclasses import field
from typing import Any, Literal
from uuid import UUID, uuid4
from pydantic import BaseModel
from app.application.services.mediator import Dispatch
from app.application.services.service_email import SendEmailNewUserHandler
from app.domain.user import User
from app.infra.repository.cat_repository import CatRepository
from app.infra.repository.user_repository import UserRepository


class Input(BaseModel):
    first_name: str
    last_name: str
    email: str
    cpf: str | None = None
    cnpj: str | None = None
    address: str
    phone_number: str
    age: int
    password: str = uuid4().hex
    events: Literal['pre-register', 'new-user', 'reset-password'] = 'new-user'
        
class OutputSuccess(BaseModel):
    id: UUID

class OutputError(BaseModel):
    errors: list[Any] = field(default_factory=list)

class CreateUser:
    def __init__(self, repo_user: UserRepository, repo_cat: CatRepository = CatRepository()) -> None:
        self._repo_user = repo_user
        self._repo_cat = repo_cat
    
    @Dispatch(SendEmailNewUserHandler())
    def execute(self, input: Input) -> OutputSuccess | OutputError:
        user, errors = User.create_instance(
            first_name=input.first_name, 
            last_name=input.last_name, 
            email=input.email, 
            cpf=input.cpf, 
            cnpj=input.cnpj, 
            address=input.address, 
            phone_number=input.phone_number, 
            age=input.age,
            password=input.password,
            image=self._repo_cat.get_random_pic(),
        )
        if not errors:
            self._repo_user.create_user(input=user)
            return OutputSuccess(id=user.id)
        return OutputError(errors=errors)