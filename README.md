# mailer

## Setup application
```bash
virtulenv venv
source venv/bin/active
pip install -e .
python -m mailer
```

You server should be started by now.
Update `mailer/settings.py` and provide appropriate values.
Server restart is required.

## Testing
```bash
pip install -r tests/requirements.txt
pytest
```

## Scaling
Following changes would be necessary to prepare this microservice for
sending millions of emails a day:
* use production WSGI server
* implement queue for sending emails
* implement worker for sending emails
* add load balancer, add `n` nodes of microservice and `m` workers
* use scalable SQL database (for example AWS RDS)
