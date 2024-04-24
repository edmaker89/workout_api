from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import select

from workout_api.atleta.models import AtletaModel
from workout_api.categorias.model import CategoriaModel
from workout_api.centro_treinamento.model import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaOut

router = APIRouter()

@router.post('/', 
             summary='Criar novo atleta', 
             status_code=status.HTTP_201_CREATED,
             response_model=AtletaOut
             )
async def post(db_session: DatabaseDependency, 
               atleta_in: AtletaIn = Body(...)
               ) -> AtletaOut:
    
    categoria_name = atleta_in.categoria.nome
    centro_treinamento_name = atleta_in.centros_treinamento.nome
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_name} não foi encontrada'
        )
        
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name))).scalars().first()    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento, {centro_treinamento_name}, não foi encontrado'
        )
    
    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now() ,**atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centros_treinamento'}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    
    db_session.add(atleta_model)
    await db_session.commit()
    
    return atleta_out