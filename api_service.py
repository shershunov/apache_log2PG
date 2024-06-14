import configparser
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

DB_USER = config['api_service']['DB_USER']
DB_PASSWORD = config['api_service']['DB_PASSWORD']
DB_HOST = config['api_service']['DB_HOST']
DB_PORT = config['api_service']['DB_PORT']
DB_NAME = config['api_service']['DB_NAME']

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Base = declarative_base()


class ApacheLogs(db.Model):
    __tablename__ = 'apache_logs'
    id_apache_logs = db.Column(db.BigInteger, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    log_name = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    request = db.Column(db.Text, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    response_size = db.Column(db.Integer, nullable=False)


@app.route('/logs', methods=['GET'])
def get_logs():
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        try:
            ip_address = request.args.get('ip_address')
            status_code = request.args.get('status_code')
            start_time = request.args.get('start_time')
            end_time = request.args.get('end_time')
            group_by_ip = request.args.get('group_by_ip', 'false').lower() == 'true'

            query = session.query(ApacheLogs)

            if ip_address:
                query = query.filter(ApacheLogs.ip_address == ip_address)

            if status_code:
                query = query.filter(ApacheLogs.status_code == status_code)

            if start_time:
                query = query.filter(ApacheLogs.timestamp >= start_time)

            if end_time:
                query = query.filter(ApacheLogs.timestamp <= end_time)

            if group_by_ip:
                query = query.with_entities(
                    ApacheLogs.ip_address,
                    func.count(ApacheLogs.id_apache_logs).label('count'),
                    func.min(ApacheLogs.timestamp).label('first_seen'),
                    func.max(ApacheLogs.timestamp).label('last_seen')
                ).group_by(ApacheLogs.ip_address)
                results = query.all()
                logs = [{'ip_address': result.ip_address, 'count': result.count, 'first_seen': result.first_seen,
                         'last_seen': result.last_seen} for result in results]
            else:
                results = query.all()
                logs = [{'id': log.id_apache_logs, 'ip_address': log.ip_address, 'log_name': log.log_name,
                         'timestamp': log.timestamp, 'request': log.request, 'status_code': log.status_code,
                         'response_size': log.response_size} for log in results]

            return jsonify(logs)
        except SQLAlchemyError as e:
            return jsonify({'error': f'Error while working with the database: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': f'Error while retrieving logs: {str(e)}'}), 500
        finally:
            session.close()


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"Error when launching the API: {e}")
