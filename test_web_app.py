import os
os.environ['DATABASE_URL'] = 'sqlite://'

from app import app, db
import unittest
from app.models import User


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['SECRET_KEY'] = 'harry'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        db.create_all()
        self.populate_db()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None
        self.client = None

    def populate_db(self):
        user = User(username='harry')
        user.set_password('harry')
        db.session.add(user)
        db.session.commit()

    def login(self):
        self.client.post('/login', data={
            'username': 'harry',
            'password': 'harry'
        })

    def test_app(self):
        assert self.app is not None
        assert app == self.app

    def test_profile_page_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login'

    def test_login_form(self):
        response = self.client.get('/login')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'name="username"' in html
        assert 'name="password"' in html
        assert 'name="remember_me"' in html
        assert 'name="submit"' in html

    def test_user_login(self):
        response = self.client.post('/login', data={
            'username': 'harry',
            'password': 'harry'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/profile'

        response = self.client.post('/profile', data={
            'body': 'test post',
            'author': 'harry'
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Username: harry' in html

    def test_user_post(self):
        self.login()
        response = self.client.post('/', data={
            'body': 'Test post'
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Username: harry' in html
        assert 'Test post' in html
        assert 'Your post has been saved' in html

    def test_password_mismatched_password(self):
        response = self.client.post('/register', data={
            'username': 'harry',
            'password': '12345',
            'confirm_password': '1234'
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Field must be equal to password." in html
