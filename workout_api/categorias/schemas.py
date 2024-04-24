from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', examples='Scale', max_length=10)]
    
class CategoriaIn(Categoria):
    nome: Annotated[str, Field(description='Nome da categoria', examples=['Scale'])]

class CategoriaOut(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', examples=['Scale'])]
    id: Annotated[UUID4, Field(description='identificação da categoria', examples=['59858b1d-2c5f-4bef-af0d-f34d0c0184b0'])]
