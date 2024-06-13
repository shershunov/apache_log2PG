import re
import os
import time
import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser


class LogHandler(FileSystemEventHandler):
    def __init__(self, connection, log_file_path, last_position_file):
        self.connection = connection
        self.log_file_path = log_file_path
        self.last_position_file = last_position_file
        self.log_pattern = re.compile(
            r'(?P<ip>\S+) '
            r'(?P<l>\S+) '
            r'\[(?P<time>[^\]]+)\] '
            r'"(?P<request>[^"]+)" '
            r'(?P<status>\d+) '
            r'(?P<size>\d+)'
        )
        self.last_position = self.load_last_position()

    def load_last_position(self):
        if os.path.exists(self.last_position_file):
            try:
                with open(self.last_position_file, 'r') as file:
                    return int(file.read().strip())
            except (ValueError, IOError):
                return 0
        return 0

    def save_last_position(self, position):
        with open(self.last_position_file, 'w') as file:
            file.write(str(position))

    def on_modified(self, event):
        if event.src_path == self.log_file_path:
            self.process_log()

    def process_log(self):
        try:
            with open(self.log_file_path, 'r') as file:
                file.seek(self.last_position)

                new_lines = file.readlines()

                self.last_position = file.tell()
                self.save_last_position(self.last_position)

                for line in new_lines:
                    match = self.log_pattern.match(line)
                    if match:
                        log_data = match.groupdict()
                        cursor = self.connection.cursor()
                        cursor.execute(
                            "CALL apache_log_insert(%s, %s, %s, %s, %s, %s)",
                            (log_data['ip'], log_data['l'], log_data['time'],
                             log_data['request'], log_data['status'], log_data['size'])
                        )
                        self.connection.commit()
                        cursor.close()
        except Exception as e:
            print(f"Ошибка при обработке логов: {e}")


class LogProcessor:
    def __init__(self, config):
        self.db_host = config['log_service']['DB_HOST']
        self.db_name = config['log_service']['DB_NAME']
        self.db_user = config['log_service']['DB_USER']
        self.db_password = config['log_service']['DB_PASSWORD']
        self.db_port = config['log_service'].getint('DB_PORT')
        self.log_file_path = config['log_service']['LOG_FILE_PATH']
        self.last_position_file = config['log_service']['LAST_POSITION_FILE']
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        try:
            return psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            return None

    def start_observer(self):
        if self.connection:
            try:
                event_handler = LogHandler(self.connection, self.log_file_path, self.last_position_file)
                observer = Observer()
                observer.schedule(event_handler, path=os.path.dirname(self.log_file_path), recursive=False)
                observer.start()

                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    observer.stop()
                    print("Обсервер остановлен.")
                except Exception as e:
                    print(f"Ошибка в цикле обсервера: {e}")

                observer.join()
            except Exception as e:
                print(f"Ошибка при настройке обсервера: {e}")
            finally:
                self.close_connection()

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Ошибка при закрытии соединения с базой данных: {e}")


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    log_processor = LogProcessor(config)
    log_processor.start_observer()


if __name__ == "__main__":
    main()
