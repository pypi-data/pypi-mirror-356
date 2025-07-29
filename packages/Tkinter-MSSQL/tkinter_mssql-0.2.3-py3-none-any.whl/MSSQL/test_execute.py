import unittest
from unittest.mock import patch, MagicMock
import MSSQL.main as main

class TestInsertRow(unittest.TestCase):
    def test_insert_row(self):
        """Проверка, что insert_row вызывает execute с правильными параметрами"""
        with patch('MSSQL.main.get_connection') as mock_conn, \
             patch('MSSQL.main.get_columns', return_value=['id', 'name']):  # Мокаем get_columns
            mock_cursor = MagicMock()
            mock_conn.return_value.__enter__.return_value = mock_cursor
            main.insert_row('SomeTable', [1, 'test'])  # Вызываем функцию
            mock_cursor.cursor.return_value.execute.assert_called_with(
                'INSERT INTO SomeTable VALUES (?,?)', [1, 'test']
            )  # Проверяем вызов execute

if __name__ == '__main__':
    unittest.main() 