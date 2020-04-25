from flask import json


def test_can_see_empty_mail_list(client):
    rv = client.get('/api/mail')
    data = json.loads(rv.data)
    assert len(data) == 0


def test_can_create_a_new_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })
    data = json.loads(rv.data)
    assert 'id' in data
    assert 'created_at' in data
    assert data['content'] == 'lorem ipsum'


def test_can_see_all_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.get('/api/mail')
    data = json.loads(rv.data)
    assert data[0]['content'] == 'lorem ipsum'


def test_can_see_details_of_the_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.get('/api/mail/1')
    data = json.loads(rv.data)
    assert 'id' in data
    assert 'created_at' in data
    assert data['content'] == 'lorem ipsum'


def test_can_define_one_recipient(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1/recipient', json={
        'address': 'example@example.com',
    })
    data = json.loads(rv.data)
    assert 'id' in data
    assert 'name' in data
    assert data['mail_id'] == 1
    assert data['address'] == 'example@example.com'


def test_can_define_many_recipients(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1/recipient', json={
        'address': 'example1@example.com',
    })
    rv = client.post('/api/mail/1/recipient', json={
        'address': 'example2@example.com',
    })
    rv = client.post('/api/mail/1/recipient', json={
        'address': 'example3@example.com',
    })

    rv = client.get('/api/mail/1')
    data = json.loads(rv.data)
    assert len(data['recipients']) == 3
    assert 'example1@example.com' in data['recipients']
    assert 'example2@example.com' in data['recipients']
    assert 'example3@example.com' in data['recipients']


def test_cannot_define_recipient_with_wrong_address(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1/recipient', json={
        'address': '@invalid.com',
    })
    assert rv.status_code == 400
    data = json.loads(rv.data)
    assert 'errors' in data
