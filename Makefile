run:
	@uvicorn workout_api.main:app --reload

req:
	@pip freeze > requirements.txt

create-migrations:
	@set PYTHONPATH=%cd% && alembic revision --autogenerate -m "Descrição_da_migração"

run-migrations:
	@set PYTHONPATH=%cd% && alembic upgrade head

