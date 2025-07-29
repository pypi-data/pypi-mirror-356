import unittest
from unittest.mock import patch, MagicMock
import MSSQL.main as main

class TestDeleteRow(unittest.TestCase):
    def test_delete_row(self):
        """Проверка, что delete_row вызывает execute с правильным SQL"""
        with patch('MSSQL.main.get_connection') as mock_conn:  # Мокаем соединение
            mock_cursor = MagicMock()
            mock_conn.return_value.__enter__.return_value = mock_cursor
            main.delete_row('SomeTable', 'id', 1)  # Вызываем функцию
            mock_cursor.cursor.return_value.execute.assert_called_with(
                'DELETE FROM SomeTable WHERE [id]=?', (1,)
            )  # Проверяем вызов execute

if __name__ == '__main__':
    unittest.main() 