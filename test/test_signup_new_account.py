import string
import random

def random_username(maxlen):
    symbols = string.ascii_letters
    return 'user_' + ''.join([random.choice[symbols] for i in range(random.randrange(maxlen))])

def test_signup_new_account(app):
    username = random_username(10)
    email = username + '@localhost'
    password = 'test'
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.logout()
