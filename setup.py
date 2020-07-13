import subprocess
import requests
from urllib.parse import urlencode, quote_plus

from common import consts



INFLUXDB_ADMIN_USER="admin"
INFLUXDB_ADMIN_PASSWORD="admin123"

print("==== Initiate Fantom Node Monitor Setup ====\n")

command = "docker network create monitoring"
network_setup = subprocess.Popen(command.split())
network_setup.wait()

command = "docker volume create grafana-volume"
grafana_volume_creation = subprocess.Popen(command.split())
grafana_volume_creation.wait()

command = "docker volume create influxdb-volume"
influxdb_volume_creation = subprocess.Popen(command.split())
influxdb_volume_creation.wait()

print("\n==== Initialize InfluxDB ====")
command = '''docker run --rm -e INFLUXDB_HTTP_AUTH_ENABLED=true \
         -e INFLUXDB_ADMIN_USER={} \
         -e INFLUXDB_ADMIN_PASSWORD={} \
         -v /var/lib/influxdb:/var/lib/influxdb \
         -v /etc/influxdb/scripts:/docker-entrypoint-initdb.d \
         influxdb /init-influxdb.sh '''.format(INFLUXDB_ADMIN_USER, INFLUXDB_ADMIN_PASSWORD)
init_influxdb = subprocess.Popen(command.split())
init_influxdb.wait()


print("\n==== Start Grafana and InfluxDB Container ====")
command = 'docker-compose up -d'
spin_up_containers = subprocess.Popen(command.split())
spin_up_containers.wait()


print("\n==== Create Database ====")
create_db = "q=CREATE DATABASE node_metrics"
response = requests.post(consts.DATABASE_URL + "query" + urlencode(create_db, quote_via=quote_plus))
print(response.text)

print("\n==== Start Monitoring Service ====")

command = "python3 ./scripts/monitor.py"
create_db = subprocess.Popen(command.split())


print("\n==== Setup complete! ====")

# TODO 
#     - replace USER_NAME and USER_PASSWORD in datasource_template.yaml
#     - store substituted version in container grafana at /usr/share/grafana/conf/provisioning/datasources 
#     - check out how to create dashboard graph automatically 

# Next steps:
#     - maybe use memory usage as first metric#     
#     - use python to query data from lachesis api (dunno anything about api yet)
#     - use telegraf as input method for influxdb 
