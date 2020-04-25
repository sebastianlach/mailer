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
