import unittest
import cli
from habitica import HabiticaAPI
from unittest.mock import patch, Mock
from io import StringIO
from textwrap import dedent

class TestCLI(unittest.TestCase):


    def setUp(self):
        self.parser = cli.setup_parser()
        self.hbt_api = HabiticaAPI(cli.get_auth())


    @patch('habitica.requests.get')
    def test_status(self, mock_status):

        status = {'profile': {'name':'test user'},
        'stats': {
            'lvl' : 1,
            'class' : "Warrior",
            'hp' : 10,
            'maxHealth' : 100,
            'exp' : 100,
            'toNextLevel' : 1000,
            'mp' : 10,
            'maxMP' : 50 
        }}

        expected_output = """\
        test user
        --------------------
        Level 1 Warrior
        --------------------
        HP: 10/100
        XP: 100/1000
        MP: 10/50
        """

        expected_output = dedent(expected_output)

        mock_status.return_value.status_code = 200
        mock_status.return_value.json.return_value = {'data': status}
        args = self.parser.parse_args(["status"])

        with patch('sys.stdout', new=StringIO()) as mock_out:
            cli.run_command(args, self.hbt_api)
            self.assertEqual(mock_out.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()