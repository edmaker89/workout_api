from typing import Annotated

from pydantic import Field
from workout_api.contrib.schemas import BaseSchema
from pydantic import UUID4


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome da centro de treinamento', examples=['CT KING'], max_length=20)]
    endereco: Annotated[str, Field(description='Endereço centro de treinamento', examples=['Rua x, qd2'], max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do centro de treinamento', examples=['Minotauro'], max_length=30)]
    
class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome da centro de treinamento', examples=['CT KING'], max_length=20)]
    
class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='identificação do centro de treinamento')]