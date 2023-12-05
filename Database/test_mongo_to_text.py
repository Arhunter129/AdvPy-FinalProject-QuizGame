import unittest
from unittest.mock import patch, MagicMock
from mongo_to_txt import get_mongodb_data, format_data, write_to_file


class TestMongoToTxt(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_documents = [
            {'question': 'test question', 'options':
             ['opt1', 'opt2'], 'answer': 'opt1'}]

    @patch('mongo_to_txt.MongoClient')
    def test_get_mongodb_data(self, mock_mongo_client: MagicMock) -> None:
        # Setup mock
        mock_collection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = iter(self.mock_documents)
        mock_collection.find.return_value = mock_cursor
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_mongo_client.return_value.__getitem__.return_value = mock_db

        # Call the function
        documents = get_mongodb_data(
            'dummy_uri',
            'dummy_path',
            'dummy_db',
            'dummy_collection')

        # Convert cursor to list for comparison
        documents_list = list(documents)

        # Assertions
        self.assertEqual(documents_list, self.mock_documents)

    def test_format_data(self) -> None:
        # Call the function with a list (which is also an Iterable)
        formatted_data = format_data(iter(self.mock_documents))

        # Assertions
        expected_data = ['test question', 'opt1', 'opt2', 'opt1\n']
        self.assertEqual(formatted_data, expected_data)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write_to_file(self, mock_open: MagicMock) -> None:
        # Test data
        data = ['line1', 'line2', 'line3']

        # Call the function
        write_to_file(data, 'dummy_file.txt')

        # Assertions
        mock_open.assert_called_with('dummy_file.txt', 'w')
        handle = mock_open()
        handle.write.assert_called()
        self.assertEqual(handle.write.call_count, len(data))


if __name__ == '__main__':
    unittest.main()
