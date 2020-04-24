def test_can_see_empty_email_list(client):
    rv = client.get('/api/mail')
    assert b'[]' in rv.data
