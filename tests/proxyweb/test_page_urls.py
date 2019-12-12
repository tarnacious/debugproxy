from __future__ import print_function  # Use print() instead of print
import pytest
from flask import url_for
from proxyweb.startup.create_users import create_users


@pytest.mark.usefixtures('db')
def test_page_urls(client):

    create_users()

    # Visit home page
    response = client.get(url_for('home.home_page'), follow_redirects=True)
    assert b'class="landing-page"' in response.data

    # Visit login page
    response = client.get(url_for('user.login'), follow_redirects=True)
    assert b'<h1>Sign in</h1>' in response.data

    # Login as user and visit User page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='admin@debugproxy.de',
                                     password='password'))
    assert b'You have signed in successfully.' in response.data

    # Edit User Profile page
    response = client.get(url_for('users.user_profile_page'))
    assert b'<h1>User Profile</h1>' in response.data
    response = client.post(url_for('users.user_profile_page'),
                           follow_redirects=True,
                           data=dict(first_name='User', last_name='User'))

    # Logout, returns to landing page
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert b'class="landing-page"' in response.data
