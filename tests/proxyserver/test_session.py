import pytest
from proxywebsocket.session import read_session
from itsdangerous import BadSignature

expected = {
    '_fresh': True,
    '_id': '1eb1257d772b0e3aa9a6fabe5b392c5120c5e3a9c639af3a1bffc17ebf2372ef71382ac154568f718ce4f389833ce29b48060ee47a21a34b4e5e0710169f3274',
    '_permanent': True,
    'csrf_token': '2d5f160735446b20eb5431c6f059f930de272fbe',
    'user_id': 'gAAAAABd9p_P4VoQ3TYD2MnLTNn6Rm22yRIXHH0Kh5utoq6gYSqpCUL9s2y_6tymTzTX2tFW0OOmv-4kPAL2l2NPdOsb9_ckHw'
}

session = ".eJw1j8tOAkEQRf-l15p0V_Vjmh1qDEYExEFhNenuqQKDM8A8NGj8d8cY7-7excm5X6LghtqdGHVNTxeieC3FSCiKCowrnYMoCUPwwXKIZCJ6SEaBTGaYfbLoA2NQkTkpR5EBHRA7hRmEpIw2NhtalkgzZj5DTAQ-6kxaSaRdABVQR02GpFNSWc8ITotB5EhNFWqqu3-11DZcdIc91YMhlIaVlQ6N1jaCpGg0qmRZGs8eZUnggCMNpL6l5u_Wdvybq9Ifi4V-PjxivrmBh3qaz2q7rADOy7v1ZCLvd6bvDie73TydjterqW_hXNjuXOWf-Rq62xc5n1fvl3q_GE_hDWaLct5GX6T95EN8_wDIumTE.XfalYA.Cq3q6lin8HlptaJtfGRnEza0zjs"

def test_decode_session():
    result = read_session(session)
    assert result == expected

def test_decode_session_raises():
    with pytest.raises(BadSignature):
        result = read_session("invalid token")


from proxywebsocket.session import verify_password

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
