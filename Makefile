run:
	@uvicorn workout_api.main:app --reload

req:
	@pip freeze > requirements.txt

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m &(d)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head 