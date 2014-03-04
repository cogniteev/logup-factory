import unittest

from flask.ext.mongoengine import MongoEngine
from models.models import User
import no_name_app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        no_name_app.configure_app('confs/test.cfg')
        self.app = no_name_app.app.test_client()
        print no_name_app.app.db.get_db()

    def tearDown(self):
        pass

    def test_index(self):
        self.app.get('/')

    def test_users(self):
        self.assertEquals(User.objects().count(), 0)


if __name__ == '__main__':
    unittest.main()
