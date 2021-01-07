import unittest
import cli
from habitica import HabiticaAPI
from unittest.mock import patch, Mock
from io import StringIO
import json
from textwrap import dedent

class TestCLI(unittest.TestCase):


    def setUp(self):
        self.parser = cli.setup_parser()
        self.hbt_api = HabiticaAPI(cli.get_auth())

    def test_find_matching_tasks(self):
        test_tasks = [{'text':'test1'}, {'text':'test2'}]
        match_test_all = cli.find_matching_tasks('test', test_tasks)
        match_test_one = cli.find_matching_tasks('test1', test_tasks)
        match_test_none = cli.find_matching_tasks('none', test_tasks)

        self.assertEqual(match_test_all, test_tasks)
        self.assertEqual([test_tasks[0]], match_test_one)
        self.assertEqual([], match_test_none)

    @patch('habitica.requests.get')
    def test_status(self, mock_status):
        args = self.parser.parse_args(["status"])
        self.mock_get_request(args, mock_status,
            'mock_data/status.json',
            'mock_data/expected_output/status.txt')

    @patch('habitica.requests.get')
    def test_list_all_tasks(self, mock_tasks):
        args = self.parser.parse_args(["list"])
        self.mock_get_request(args, mock_tasks, 
            'mock_data/tasks_all.json',
            'mock_data/expected_output/tasks_all.txt')

    @patch('habitica.requests.get')
    def test_list_habit_tasks(self, mock_tasks):
        args = self.parser.parse_args(["list", "habits"])
        self.mock_get_request(args, mock_tasks, 'mock_data/tasks_habits.json',
            'mock_data/expected_output/tasks_habits.txt')

    def mock_get_request(self, args, mock_api, mock_data_path, expected_output_path):
        mock_api.return_value.status_code = 200

        with open(mock_data_path) as f:
            data = json.load(f)

        with open(expected_output_path) as f:
            expected_output = f.read()

        mock_api.return_value.json.return_value = data

        with patch('sys.stdout', new=StringIO()) as mock_out:
            cli.run_command(args, self.hbt_api)
            self.assertEqual(mock_out.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()