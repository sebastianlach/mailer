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


def test_can_create_a_new_mail_with_sender(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
        'address': 'example@example.com',
        'name': 'Example',
    })
    data = json.loads(rv.data)
    assert data['content'] == 'lorem ipsum'
    assert data['address'] == 'example@example.com'
    assert data['name'] == 'Example'


def test_cannot_create_a_new_mail_without_data(client):
    rv = client.post('/api/mail')
    assert rv.status_code == 400


def test_cannot_create_a_new_mail_without_content(client):
    rv = client.post('/api/mail', json={
        'address': 'example@example.com',
    })
    assert rv.status_code == 400
    data = json.loads(rv.data)
    assert 'errors' in data


def test_can_see_all_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.get('/api/mail')
    data = json.loads(rv.data)
    assert len(data) == 1
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


def test_cannot_see_details_of_non_existing_mail(client):
    rv = client.get('/api/mail/42')
    assert rv.status_code == 404


def test_can_check_the_status_of_the_email(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.get('/api/mail/1')
    data = json.loads(rv.data)
    assert data['state'] == 'MailStates.PENDING'


def test_cannot_update_non_existing_mail(client):
    rv = client.post('/api/mail/42')
    assert rv.status_code == 404


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


def test_cannot_define_existing_recipient(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1/recipient', json={
        'address': 'example@example.com',
    })
    data = json.loads(rv.data)
    assert data['mail_id'] == 1
    assert data['address'] == 'example@example.com'

    rv = client.post('/api/mail/1/recipient', json={
        'address': 'example@example.com',
    })
    assert rv.status_code == 409


def test_cannot_define_recipient_for_non_existing_mail(client):
    rv = client.post('/api/mail/42/recipient', json={
        'address': 'example@example.com',
    })
    assert rv.status_code == 404


def test_cannot_define_recipient_without_data(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1/recipient')
    assert rv.status_code == 400


def test_can_define_the_sender(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1', json={
        'address': 'example@example.com',
        'name': 'Example',
    })
    data = json.loads(rv.data)
    assert data['name'] == 'Example'
    assert data['address'] == 'example@example.com'


def test_cannot_define_the_sender_with_wrong_address(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1', json={
        'address': '@invalid.com',
        'name': 'Example',
    })
    assert rv.status_code == 400
    data = json.loads(rv.data)
    assert 'errors' in data


def test_cannot_update_mail_without_data(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.post('/api/mail/1')
    assert rv.status_code == 400
