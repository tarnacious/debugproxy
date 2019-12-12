import pytest
from proxyserver.session import read_session
from itsdangerous import BadSignature

expected = {'_fresh': True,
            '_id': 'b9125e4fa2de6499cc739e9522372487ab1fcdf6a738edc5538bb3ad95078f541eb5625eca2fb8aeda6dd34db4a87a27885ae4d9164245504483f6ab64d9d5b8',
            'csrf_token': 'bb965ca523deba73a95f3759620c067484036555',
            'user_id': '1'}

session = ".eJwlj0tqBDEMRO_i9Sxs_SzPZRrJkskwkED3zCrk7nHItuC9qvouxzrz-ij31_nOWzkeUe7FRwNOWgaRQmPM2XHkYADsQNrN25qxxDpqxmRGdUeLwbXrYmrpLNswDZarZZhEIIWTbRi6KltSjCYExFyJFLfNZWfBruVW5nWu4_X1zM-_PT6EpzFgpO9SG7yw8xCos0onpYrCzJt7X3n-n2jl5xfqET61.C3a5Yw.SJYmreVBjbqaliT3R_oXp6FwUDk"

def test_decode_session():
    result = read_session(session)
    assert result == expected

def test_decode_session_raises():
    with pytest.raises(BadSignature):
        result = read_session("invalid token")


from proxyserver.session import verify_password

def test_verify_password():
    hashed_password = "$2b$12$YpeVYWRSprTD85DlOxn6S.2w4ErvnVYuWYdR6jGPtsnbg9noclzp2"
    password = "password"
    assert verify_password(password, hashed_password) is True

def test_verify_password_bad_password():
    hashed_password = "$2b$12$YpeVYWRSprTD85DlOxn6S.2w4ErvnVYuWYdR6jGPtsnbg9noclzp2"
    password = "bad-password"
    assert verify_password(password, hashed_password) is False

def test_verify_password_bad_hash():
    hashed_password = "bad-hash"
    password = "password"
    with pytest.raises(ValueError):
        verify_password(password, hashed_password)
