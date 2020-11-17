import ipaddress
import re
import socket

from celery import Celery
from flask import Flask, request, jsonify, Response
from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from serializers import JobSerializer

cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fcache',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://redis:6379'
}

app = Flask(__name__)
CORS(app)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

#  Celery
client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)

#  Redis caching
app.config.from_mapping(cache_config)
cache = Cache(app)

#  ORM
db = SQLAlchemy(app)

from sqlalchemy.dialects.postgresql import ARRAY


#  TODO: move models out of app.py
class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    ips = db.Column(ARRAY(db.String, dimensions=1))
    status = db.Column(db.String)
    value = db.Column(db.String)
    search_expression = db.Column(db.String)
    ips_resolved = db.Column(db.Integer, default=0)
    ips_matched = db.Column(db.Integer, default=0)
    ips_received = db.Column(db.Integer, default=0)


def _percentage(part, whole):
    return 100 * float(part) / float(whole)


@client.task
def resolve_ip(job_id, value, search_expression):
    job = Job.query.get(job_id)
    cache.set(f'job_{job_id}', str(0))
    try:
        ip_address = [str(ip) for ip in ipaddress.IPv4Network(value)]
        job.ips_received = len(ip_address)
        filtered_ips = list()

        i = 0
        matched_count = 0
        resolved_count = 0
        while matched_count < 1000 and i < len(ip_address):
            try:
                resolved_ip = socket.gethostbyaddr(ip_address[i])
                resolved_count += 1

                if re.search(search_expression, resolved_ip[0]) or re.search(search_expression, resolved_ip[2][0]):
                    matched_count += 1
                    filtered_ips.append(f'{resolved_ip[0]}-{resolved_ip[2][0]}')
                    job.ips = filtered_ips
            except Exception as e:
                continue
            cache.set(f'job_{job_id}', str(round(_percentage(i, len(ip_address)), 2)))
            i += 1
        job.ips_resolved = resolved_count
        job.status = 'done'
        job.ips_matched = matched_count
    except Exception as e:
        job.status = 'error'

    db.session.add(job)
    db.session.commit()


@app.route('/job', methods=['POST'])
def create_job():
    data = request.get_json()

    if not data['search_expression'] or not data['value']:
        return Response('Expected data not provided', 417)

    job = Job(
        ips=list(),
        status='process',
        search_expression=data['search_expression'],
        value=data['value']
    )
    db.session.add(job)
    db.session.commit()

    resolve_ip.delay(job.id, **data)

    return jsonify({"new_job": JobSerializer(job).serialize()})


@app.route('/jobs', methods=['GET'])
def jobs():
    return jsonify([JobSerializer(job).serialize() for job in Job.query.order_by(Job.id).all()])


@app.route('/job/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    resp = JobSerializer(job).serialize()
    percentage = '100' if job.status != 'process' else cache.get(f'job_{job_id}')
    resp['percentage'] = percentage
    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
