import unittest
import requests


class TestDict(unittest.TestCase):
    def test_auth_check(self):
        res = requests.get('http://127.0.0.1:5000/api/v1/check/', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

        res = requests.get('http://127.0.0.1:5000/api/v1/check/', cookies={
            'session': 'happy new year'
        }, verify=False)
        self.assertEqual(res.status_code, 401)

    def test_user(self):
        res = requests.get('http://127.0.0.1:5000/api/v1/users/3/info/', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

        res = requests.get('http://127.0.0.1:5000/api/v1/users/my/info/', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)


        res = requests.put('http://127.0.0.1:5000/api/v1/users/my/info/', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, json={'qq': '985811440', 'show_stdnum': False, 'show_qq': False}, verify=False)
        self.assertEqual(res.status_code, 200)

    def test_rank(self):
        res = requests.get('http://127.0.0.1:5000/api/v1/rank/lib', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

        res = requests.get('http://127.0.0.1:5000/api/v1/rank/step/person', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

        res = requests.get('http://127.0.0.1:5000/api/v1/rank/step/dept/week', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

        res = requests.get('http://127.0.0.1:5000/api/v1/rank/step/dept/month', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

    def test_werun(self):
        res = requests.get('http://127.0.0.1:5000/api/v1/werun/', cookies={
            'session': 'eyJpZCI6IjMifQ.XJSYlg.X8x9KwTOB6dpamiKVQ70Ya2VhsI'
        }, verify=False)
        self.assertEqual(res.status_code, 200)

    def test_like(self):
        pass


if __name__ == '__main__':
    unittest.main()
