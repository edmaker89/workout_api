run:
	@uvicorn workout_api.main:app --reload

req:
	@pip freeze > requirements.txt