migrations: SeedSchool/manage.py
	python3 SeedSchool/manage.py makemigrations

migrate: SeedSchool/manage.py
	python3 SeedSchool/manage.py migrate

run:
	python3 SeedSchool/manage.py runserver

install:
	pip install -r requirements.txt
