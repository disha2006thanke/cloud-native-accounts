
import os
import tempfile
import unittest

from service import create_app
from service.models import init_db


class AccountsTestCase(unittest.TestCase):
    def setUp(self):
        handle, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(handle)

        os.environ["DATABASE_PATH"] = self.db_path

        self.app = create_app()
        self.client = self.app.test_client()
        init_db()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.environ.pop("DATABASE_PATH", None)

    def create_test_account(self):
        return self.client.post(
            "/accounts",
            json={"name": "Asha", "email": "asha@example.com"},
        )

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_create_account(self):
        response = self.create_test_account()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Asha")

    def test_list_accounts(self):
        self.create_test_account()
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_read_account(self):
        created = self.create_test_account()
        account_id = created.get_json()["id"]

        response = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 200)

    def test_update_account(self):
        created = self.create_test_account()
        account_id = created.get_json()["id"]

        response = self.client.put(
            f"/accounts/{account_id}",
            json={"name": "Asha Updated", "email": "asha2@example.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Asha Updated")

    def test_delete_account(self):
        created = self.create_test_account()
        account_id = created.get_json()["id"]

        response = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
