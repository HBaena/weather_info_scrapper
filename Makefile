tests = `find ./tests -name "*.py"`
FILE_PATH = `pwd`/resumens/resumes.parquet
init:
	@poetry install -vvv --with dev
	@poetry self add poetry-dotenv-plugin
	@poetry run python -m pip install 'apache-airflow[cncf.kubernetes]'
	@poetry run python create_db.py
start:
	@poetry shell
	@airflow db init
	@airflow dags unpause weather_info
	@airflow scheduler
run_dashboard:
	make run_db_resume
	@poetry run python dashboard_app.py
test:
	@poetry run mamba $(tests) --format documentation --enable-coverage
lint:
	@ruff check --fix .
run_scrapper:
	@poetry run python weather_info_scrapping.py all
run_db_resume:
	@poetry run python generate_db_resume.py
