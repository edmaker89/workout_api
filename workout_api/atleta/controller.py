from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy import select
from pydantic import UUID4
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.model import CategoriaModel
from workout_api.centro_treinamento.model import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaDetailOut, AtletaIn, AtletaOut, AtletaUpdate
from sqlalchemy.exc import IntegrityError

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
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now() ,**atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centros_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro de integridade de dados no banco de dados")
    return atleta_out

@router.get('/', summary='Constular todos os Atletas', 
             status_code=status.HTTP_200_OK,
             response_model=Page[AtletaDetailOut],
             )
async def query_all_custom(db_session: DatabaseDependency, nome: str=None, cpf: str=None) -> Page[AtletaDetailOut]:
    query_filters = []
    
    if nome:
        query_filters.append(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query_filters.append(AtletaModel.cpf == cpf)
    atletas: list[AtletaModel] = (await db_session.execute(select(AtletaModel).filter(*query_filters))).scalars().all()
    
    response = []
    for atleta in atletas:
        centro_treinamento = atleta.centros_treinamento.nome if atleta.centros_treinamento else None
        categoria = atleta.categoria.nome if atleta.categoria else None
        
        print(categoria, centro_treinamento)
        
        atleta_detail = AtletaDetailOut(
            id=atleta.id,
            created_at=atleta.created_at,
            nome=atleta.nome,
            cpf=atleta.cpf,
            idade=atleta.idade,
            peso=atleta.peso,
            altura=atleta.altura,
            sexo=atleta.sexo,
            categoria=categoria,
            centros_treinamento=centro_treinamento,
        )
        response.append(atleta_detail)
    return paginate(response)

@router.get('/{id}', summary='Constular uma atletas pelo id', 
             status_code=status.HTTP_200_OK,
             response_model=AtletaOut,
             )
async def query(id:UUID4 ,db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrada no id: {id}')
    
    return AtletaOut.model_validate(atleta)


@router.patch('/{id}', summary='Editar uma atletas pelo id', 
             status_code=status.HTTP_200_OK,
             response_model=AtletaOut,
             )
async def query(id:UUID4 ,db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    print(atleta_up)
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrada no id: {id}')
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
        
    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta

@router.delete('/{id}', summary='Deletar uma atletas pelo id', 
             status_code=status.HTTP_204_NO_CONTENT,
             )
async def delete(id:UUID4 ,db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrada no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()
