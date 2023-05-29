"""
Тесты для базовых проверок функционала
"""
import unittest
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class RunServerTests(TestCase):
    """
    Класс, проверяющий запуск сервера разработки
    """
    def setUp(self) -> None:
        """
        Конфигурация тест-кейса
        """
        self.browser: WebDriver = webdriver.Chrome()

    def test_server_is_working(self) -> None:
        """
        Тест-кейс, проверяющий, что тестовый сервер работает
        """
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn("Congratulations", self.browser.title)

    def tearDown(self) -> None:
        """
        Завершение сессии браузера
        """
        self.browser.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
