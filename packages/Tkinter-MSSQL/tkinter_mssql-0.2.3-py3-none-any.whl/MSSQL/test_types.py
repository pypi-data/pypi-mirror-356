import unittest
from unittest.mock import patch, MagicMock
import MSSQL.main as main

class TestGetColumns(unittest.TestCase):
    def test_get_columns(self):
        """Проверка, что get_columns возвращает список колонок"""
        with patch('MSSQL.main.get_connection') as mock_conn:  # Мокаем соединение
            mock_cursor = MagicMock()
            mock_cursor.cursor.return_value.fetchall.return_value = [('id',), ('name',)]
            mock_conn.return_value.__enter__.return_value = mock_cursor
            result = main.get_columns('SomeTable')  # Вызываем функцию
            self.assertEqual(result, ['id', 'name'])  # Проверяем результат

if __name__ == '__main__':
    unittest.main() 