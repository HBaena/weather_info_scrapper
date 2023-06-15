tests = `find ./tests -name "*.py"`
app = `pwd`/app.py
log_file = `pwd`/app.log
current_location = `pwd`/dags
install:
	@poetry install -vvv --with dev
	@poetry self add poetry-dotenv-plugin
	@poetry run python -m pip install 'apache-airflow[cncf.kubernetes]'
start:
	@poetry shell
	@airflow db init
	@airflow dags unpause weather_info
	@airflow scheduler
run:
	PYTHONPATH=":."  poetry run python app.py $(city)
test:
	PYTHONPATH=":." poetry run mamba $(tests) --format documentation --enable-coverage
lint:
	@ruff check --fix .
