## Введение
Этот репозиторий содержит два сервиса: `api_service` и `log_service`. `api_service` предоставляет API для запросов данных логов Apache, а `log_service` обрабатывает и сохраняет логи.

## Инструкции по установке

### Шаг 1: Клонирование репозитория
Загрузите репозиторий:
```bash
sudo git clone https://github.com/shershunov/apache_logs
cd apache_logs
```

### Шаг 2: Настройка виртуального окружения Python
Создайте виртуальное окружение Python с названием apache_env и активируйте его:
```bash
sudo apt-get install python3-venv
python3 -m venv apache_env
source apache_env/bin/activate
```

### Шаг 3: Установка зависимостей
Установите необходимые библиотеки Python из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Возможно потребуется установка psycopg2-binary
```bash
pip install psycopg2-binary
```

### Шаг 4: Настройка конфигурации
Требуется указать данные для подключения к БД PostgreSQL.
#### config.ini
```
[log_service]
DB_HOST = localhost
DB_NAME = internship
DB_USER = watchdog_agent
DB_PASSWORD = Pa$$w0rd
DB_PORT = 5432
LOG_FILE_PATH = /var/log/apache2/access.log
LAST_POSITION_FILE = last_position.temp

[api_service]
DB_HOST = localhost
DB_NAME = internship
DB_USER = api_agent
DB_PASSWORD = Pa$$w0rd
DB_PORT = 5432
```
### Шаг 5: Настройка формата логов Apache
Установим формат логов:
```bash
nano /etc/apache2/apache2.conf
```
```
LogFormat "%h %l %t \"%r\" %>s %b" combined
```

### Шаг 6: Запуск установочных скриптов
Запустите установочные скрипты для настройки сервисов:
```bash
sudo bash install_api_service.sh
sudo bash install_log_service.sh
```

# Документация API
api_service предоставляет конечную точку API по адресу http://host:5000/logs для запросов данных логов Apache. Конечная точка принимает следующие параметры:

ip_address: Фильтрация логов по IP-адресу.<br>
status_code: Фильтрация логов по статус-коду.<br>
start_time: Фильтрация логов по временной метке после указанного времени.<br>
end_time: Фильтрация логов по временной метке до указанного времени.<br>
group_by_ip: Если true, группировка результатов по IP-адресу.<br>
#### Пример запроса:
```
curl -X GET "http://host:5000/logs"
curl -X GET "http://host:5000/logs?group_by_ip=true"
curl -X GET "http://host:5000/logs?ip_address=192.168.1.1"
curl -X GET "http://host:5000/logs?start_time=2024-06-01T00:00:00&end_time=2024-06-10T23:59:59"
```
# Приложение
<img src="https://github.com/shershunov/apache_logs/assets/71601841/11c96e9c-1682-438f-bb9e-68073381871e"/>

### Настройка конфигурации
Требуется указать Host, Port и URL расположенного API сервера.

#### config.ini
```
[API]
host = 0.0.0.0
port = 5000
url = /logs
```

#### Можно включать и отключать фильтры.

Возможна выборка по конкретному ip адресу или status коду.<br>
Выборка от и до конкретной даты.<br>
Группировка по ip выводит кол-во записей, дата первого и последнего заходов.
