import unittest
from unittest.mock import patch
import MSSQL.main as main

class TestConnection(unittest.TestCase):
    def test_get_connection(self):
        """Проверка, что соединение с БД создаётся"""
        with patch('pyodbc.connect') as mock_connect:  # Мокаем pyodbc.connect
            conn = main.get_connection()  # Вызываем функцию
            mock_connect.assert_called_once()  # Проверяем, что connect был вызван

if __name__ == '__main__':
    unittest.main() 