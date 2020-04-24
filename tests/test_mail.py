def test_can_see_empty_mail_list(client):
    rv = client.get('/api/mail')
    assert b'[]' in rv.data


def test_can_create_a_new_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })
    assert b'"id"' in rv.data
    assert b'"content"' in rv.data
    assert b'"created_at"' in rv.data
    assert b'"lorem ipsum"' in rv.data


def test_can_see_all_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.get('/api/mail')
    assert b'"lorem ipsum"' in rv.data


def test_can_see_details_of_the_mail(client):
    rv = client.post('/api/mail', json={
        'content': 'lorem ipsum',
    })

    rv = client.get('/api/mail/1')
    assert b'"lorem ipsum"' in rv.data
