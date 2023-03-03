import unittest
from app import app

class AppTest(unittest.TestCase):
    def test_home(self):
         self.client = app.test_client()
         response = self.client.get("/")
         self.assertEquals(response.status_code, 200)


if __name__ == "__main__":
   unittest.main()  
