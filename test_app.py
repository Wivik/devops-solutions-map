import os
import unittest
from app import app, freezer

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['FREEZER_MODE'] = True
        self.frozen = freezer.freeze()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DevOps Solutions Map', response.data)

    def test_links(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<a href="/about.html">About</a>', response.data)

    def test_tools(self):
        response = self.app.get('/tool/VSCode.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Visual Studio Code, also commonly referred to as VS Code', response.data)

    def test_usecases(self):
        response = self.app.get('/side/dev/step/plan/usecase/Project%20management.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project management is the process of leading the work', response.data)

    def test_static_files_exist(self):
        """
        Test that the static files have been generated correctly.
        """
        # Check that the index.html file exists.
        self.assertTrue(os.path.exists(os.path.join(app.config['FREEZER_DESTINATION'], 'index.html')))

        # Check that the static directory exists.
        self.assertTrue(os.path.exists(os.path.join(app.config['FREEZER_DESTINATION'], 'static')))

        # Check that the CSS file exists.
        self.assertTrue(os.path.exists(os.path.join(app.config['FREEZER_DESTINATION'], 'static', 'css', 'style.css')))

        # Check that the VSCode page exists
        self.assertTrue(os.path.exists(os.path.join(app.config['FREEZER_DESTINATION'], 'tool', 'VSCode.html')))

        # Check that the Project Management use case exists.
        self.assertTrue(os.path.exists(os.path.join(app.config['FREEZER_DESTINATION'], 'side', 'dev', 'step', 'plan', 'usecase', 'Project management.html')))


if __name__ == '__main__':
    unittest.main()

