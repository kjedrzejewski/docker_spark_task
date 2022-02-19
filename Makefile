start_sevices:
	docker compose up -d

stop_services:
	docker compose stop

restart_services:
	docker compose restart

reset_services:
	docker compose stop
	docker compose rm -f
	docker compose up -d
	
create_schema:
	@echo "This one doesn't need to be run as pandas may create a table on his own"
	docker exec -i mysql_cont /bin/bash -c 'mysql --user="$$MYSQL_USER" --password="$$MYSQL_PASSWORD" --database="$$MYSQL_DATABASE"' < ./create_schema.sql

submit_job:
	docker exec spark_cont ./bin/spark-submit /job/job.py
