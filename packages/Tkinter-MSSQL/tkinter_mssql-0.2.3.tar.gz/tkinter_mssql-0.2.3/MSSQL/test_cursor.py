import unittest
from unittest.mock import patch, MagicMock
import MSSQL.main as main

class TestFetchAll(unittest.TestCase):
    def test_fetch_all_returns_data(self):
        """Проверка, что fetch_all возвращает данные"""
        with patch('MSSQL.main.get_connection') as mock_conn:  # Мокаем соединение
            mock_cursor = MagicMock()
            mock_cursor.cursor.return_value.fetchall.return_value = [(1, 'test')]
            mock_conn.return_value.__enter__.return_value = mock_cursor
            result = main.fetch_all('SomeTable')  # Вызываем функцию
            self.assertEqual(result, [(1, 'test')])  # Проверяем результат

if __name__ == '__main__':
    unittest.main() 