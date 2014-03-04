import json
import unittest


from models.models import User, Token
import no_name_app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        no_name_app.configure_app('confs/test.cfg')
        self.app = no_name_app.app.test_client()
        User.drop_collection()
        Token.drop_collection()

    def test_empty_mongo(self):
        self.assertEquals(User.objects().count(), 0)
        self.assertEquals(Token.objects().count(), 0)

    def test_index(self):
        response =  self.app.get('/')
        self.assertEquals(response.status_code, 200)

    def test_signup(self):
        data = {'email': 'test@test.com', 'password': 'test'}
        response = self.app.post('/signup', data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data), {'email': 'test@test.com'})

    def test_login(self):
        data = {'email': 'test@test.com', 'password': 'test'}
        response = self.app.post('/signup', data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data), {'email': 'test@test.com'})
        login_response = self.app.post('/login', data=data)
        self.assertEquals(login_response.status_code, 200)
        self.assertEquals(json.loads(login_response.data),
                          {'email': 'test@test.com'})

    def test_signup_invalid(self):
        data = {'email': 'testtest.com', 'password': 'test'}
        response = self.app.post('/signup', data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data),
                          {'error': 'Invalid email address'})

    def test_signup_already(self):
        data = {'email': 'test@test.com', 'password': 'test'}
        response = self.app.post('/signup', data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data), {'email': 'test@test.com'})

        failed = self.app.post('/signup', data=data)
        self.assertEquals(failed.status_code, 200)
        self.assertEquals(json.loads(failed.data),
                          {'error': 'Already registered email'})

    def test_login_failure(self):
        data = {'email': 'test@test.com', 'password': 'test'}
        login_response = self.app.post('/login', data=data)
        self.assertEquals(login_response.status_code, 200)
        self.assertEquals(json.loads(login_response.data),
                          {'error': 'Invalid credentials'})

if __name__ == '__main__':
    unittest.main()
