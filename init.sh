pip install -r requirements.txt

docker run --name zluriPostgresDb -p 5455:5432 -e POSTGRES_USER=zluriUser -e POSTGRES_PASSWORD=jarvis -e POSTGRES_DB=zluriTransactionDB -v ${HOME}/docker-postgres-data:/var/lib/postgresql/data -d postgres

sleep 3

python3 code/start.py
