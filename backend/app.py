import ipaddress
import re

from celery import Celery
from flask import Flask, request, jsonify
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

def _percentage(part, whole):
  return 100 * float(part)/float(whole)

@client.task
def resolve_ip(job_id, value, search_expression):
    job = Job.query.get(job_id)
    cache.set(f'job_{job_id}', str(0))
    try:
        ip_address = [str(ip) for ip in ipaddress.IPv4Network(value)]
        job.ips_resolved = len(ip_address)
        filtered_ips = list()
        filtered_list = list(filter(lambda x: re.search(search_expression, x), ip_address))[:1000]

        for ip in filtered_list:
            #  First 1000 elements what is accepted by search expression

            #  Uncomment this line to simulate long request
            # import time
            # time.sleep(2)
            filtered_ips.append(ip)
            job.ips = filtered_ips
            cache.set(f'job_{job_id}', str(round(_percentage(len(filtered_ips), len(filtered_list)), 2)))

        job.status = 'done'
        job.ips_matched = len(filtered_list)
    except Exception as e:
        job.status = 'error'

    db.session.add(job)
    db.session.commit()

@app.route('/job', methods=['POST'])
def create_job():
    data = request.get_json()

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