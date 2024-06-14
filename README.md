## Introduction
This repository contains two services: `api_service` and `log_service`. `log_service` processes and stores logs in PostgreSQL, and `api_service` provides an API for querying Apache log data.

### Installation Instructions

### Step 1: Clone the repository
Upload the repository:
```bash
sudo git clone https://github.com/shershunov/apache_logs
cd apache_logs
```

### Step 2: Configuring the Python virtual environment
Create a Python virtual environment named apache_env and activate it:
```bash
sudo apt-get install python3-venv
python3 -m venv apache_env
source apache_env/bin/activate
```

### Step 3: Install dependencies
Install the required Python libraries from the requirements.txt file:
```bash
pip install -r requirements.txt
```
You may need to install psycopg2-binary
```bash
pip install psycopg2-binary
```

### Step 4: Configuration setup
It is required to specify data for connection to PostgreSQL database.
#### config.ini
```
[log_service]
DB_HOST = localhost
DB_NAME = postgres
DB_USER = watchdog_agent
DB_PASSWORD = Pa$$w0rd
DB_PORT = 5432
LOG_FILE_PATH = /var/log/apache2/access.log
LAST_POSITION_FILE = last_position.temp

[api_service]
DB_HOST = localhost
DB_NAME = postgres
DB_USER = api_agent
DB_PASSWORD = Pa$$w0rd
DB_PORT = 5432
```

### Step 5: Set the Apache log format
Set the log format:
```bash
nano /etc/apache2/apache2.conf
```
```
LogFormat "%h %l %t \"%r\" %>s %b" combined
```

### Step 6: Run the installation scripts
Run the installation scripts to configure the services:
```bash
sudo bash install_api_service.sh
sudo bash install_log_service.sh
```

# API Documentation
The api_service provides an API endpoint at http://host:5000/logs to query Apache log data. The endpoint accepts the following parameters:

ip_address: Filter logs by IP address.<br>
status_code: Filter logs by status code.<br>
start_time: Filter logs by timestamp after the specified time.<br>
end_time: Filter logs by timestamp before the specified time.<br>
group_by_ip: If true, grouping results by IP address.<br>

#### Example request:
```bash
curl -X GET "http://host:5000/logs"
curl -X GET "http://host:5000/logs?group_by_ip=true"
curl -X GET "http://host:5000/logs?ip_address=192.168.1.1"
curl -X GET "http://host:5000/logs?start_time=2024-06-01T00:00:00&end_time=2024-06-10T23:59:59"
```
# Application
<img src="https://github.com/shershunov/apache_logs/assets/71601841/83b29eca-a7ce-4003-a332-06438958672d"/>

### Configuration settings
It is required to specify Host, Port and URL of the located API server.

#### config.ini
```
[API]
host = 0.0.0.0
port = 5000
url = /logs
```

#### You can enable and disable filters.

Selection by specific ip address or status code is possible.<br>
Selection from and to a specific date.<br>
Grouping by ip displays the number of records, date of first and last access.
