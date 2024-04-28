# 🌦️ WeatherLinkIP to InfluxDB Exporter

A WeatherLinkIP is a discontinued data logger for a Davis weather station, this project uses the work done by [ae-11](https://github.com/ae-11/WeatherLinkIP_Py) to get the data from the station and then capture it to an InfluxDB.

## Deployment

Currently you need to run `PublishData.py` script on a cronjob to get it to automatically collect data every minute, but this will eventually be converted into a Docker image.

First you need to make a copy of the `.env.example` file which is named `.env`. This should then be filled will the relevant information. Then add a cronjob task to run the `run.sh` file every minute (the `run.sh` file will ensure that the environment values are passed to the python script.)

You will then need to configure [InfluxDB2](https://www.influxdata.com/) and [Grafana](https://grafana.com/) (for prettier dashboards). Here is a sample Docker Compose file to bring up those services.

You should update the credentials for InfluxDB before you start the container. Grafana will ask you to change your credentials the first time you login (the default values are `admin`:`admin`).

```yaml
version: "3.8"

services:
  influxdb:
    container_name: influxdb
    image: "influxdb:latest"
    restart: unless-stopped
    environment:
      - TZ=Europe/London
      - DOCKER_INFLUXDB_INIT_USERNAME=myuser
      - DOCKER_INFLUXDB_INIT_PASSWORD=mypassword
      - DOCKER_INFLUXDB_INIT_ORG=myorg
      - DOCKER_INFLUXDB_INIT_BUCKET=mybucket
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
      - DOCKER_INFLUXDB_INIT_MODE=setup
    # - DOCKER_INFLUXDB_INIT_MODE=upgrade
    ports:
      - "8086:8086"
    volumes:
      - influx-data:/var/lib/influxdb2
      - influx-config:/etc/influxdb2
      - influx-backup:/var/lib/backup
    healthcheck:
      test: ["CMD", "influx", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  grafana:
    container_name: grafana
    image: grafana/grafana
    restart: unless-stopped
    user: "0"
    ports:
      - "3000:3000"
    environment:
      - TZ=Europe/London
      - GF_PATHS_DATA=/var/lib/grafana
      - GF_PATHS_LOGS=/var/log/grafana
    volumes:
      - grafana-data:/var/lib/grafana
      - grafana-log:/var/log/grafana
    healthcheck:
      test: ["CMD", "wget", "-O", "/dev/null", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  influx-data:
  influx-config:
  influx-backup:
  grafana-data:
  grafana-log:
```

