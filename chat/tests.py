"""
Модульные тесты приложения chat
"""
import typing
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Messages, GroupChat, UserImage


class TestGroupChatDatabase(TestCase):
    """
    Тестирование таблицы GroupChat
    """
    title: str
    group: typing.Type[GroupChat]

    def data_for_tests(self) -> None:
        """
        Дженерик с тестовыми данными
        """
        self.title = 'Тестовая группа'
        self.group = GroupChat.objects.create(
            title=self.title
        )

    def test_group_chat_is_created(self) -> None:
        """
        Тестирование, что группа создана
        """
        self.data_for_tests()
        self.assertTrue(self.group)

    def test_group_data_is_valid(self) -> None:
        """
        Тестирование, что данные группового чата правильные
        """
        self.data_for_tests()
        self.assertEqual(self.group.title, self.title)

    def test_group_data_type_is_valid(self) -> None:
        """
        Тестирование, что типы данных группового чата правильные
        """
        self.data_for_tests()
        self.assertIsInstance(self.group.title, str)


class TestMessagesDatabase(TestCase):
    """
    Тестирование таблицы MessageHistory
    """
    text: str
    user: typing.Type[get_user_model]
    author: typing.Type[get_user_model]
    created: timezone.timezone
    modified: timezone.timezone
    group_chat: typing.Type[GroupChat]
    message: typing.Type[Messages]

    def data_for_tests(self) -> None:
        """
        Дженерик создания тестовых данных
        """
        self.text = 'Тест'
        self.user = get_user_model()
        self.author = self.user.objects.create_user(
            username='test_user1',
            email='testuser@example.com',
            password='Test123!'
        )
        self.group_chat = GroupChat.objects.create(
            title=self.text
        )
        self.created = timezone.now()
        self.modified = timezone.now()
        self.message = Messages.objects.create(
            message=self.text,
            author=self.author,
            created=self.created,
            modified=self.modified,
            group_chat=self.group_chat
        )

    def test_message_is_created(self) -> None:
        """
        Тест-кейс, проверяющий, создано ли сообщение
        """
        self.data_for_tests()
        self.assertTrue(self.message)

    def test_message_data_is_correct(self) -> None:
        """
        Тест-кейс, проверяющий, все ли данные сохранились
        """
        self.data_for_tests()
        self.assertEqual(self.message.message, self.text)
        self.assertEqual(self.message.created, self.created)
        self.assertEqual(self.message.modified, self.modified)
        self.assertEqual(self.message.author, self.author)
        self.assertEqual(self.message.group_chat, self.group_chat)

    def test_message_data_type_is_correct(self) -> None:
        """
        Тест-кейс, проверяющий, правильные ли типы данных у сообщения
        """
        self.data_for_tests()
        self.assertIsInstance(self.message.message, str)
        self.assertIsInstance(self.message.created, timezone.datetime)
        self.assertIsInstance(self.message.modified, timezone.datetime)
        self.assertIsInstance(self.message.author, self.user)
        self.assertIsInstance(self.message.group_chat, GroupChat)


class TestUserImage(TestCase):
    """
    Тестирование UserImage
    """
    user: typing.Type[get_user_model]
    image: str
    author: typing.Type[get_user_model]
    user_image: typing.Type[UserImage]

    def test_image_is_created(self) -> None:
        """
        Тестирование, что запись в UserImage создана
        """
        self.user = get_user_model()
        self.user = self.user.objects.create_user(
            username='test_user',
            password='test123!',
            email='test1@example.com'
        )
        self.image = 'test.png'
        self.user_image = UserImage.objects.create(
            user=self.user,
            image=self.image
        )
        self.assertTrue(self.user_image)

    def test_user_image_data_is_correct(self) -> None:
        """
        Тестирование, что у записи в UserImage сохранились все данные
        """
        self.user = get_user_model()
        self.author = self.user.objects.create_user(
            username='test_user',
            password='test123!',
            email='test1@example.com'
        )
        self.image = 'test.png'
        self.user_image = UserImage.objects.create(
            user=self.author,
            image=self.image
        )
        self.assertEqual(self.user_image.user, self.author)
        self.assertEqual(self.user_image.image, self.image)

    def test_user_image_data_type_is_correct(self) -> None:
        """
        Тестирование, что типы данных в UserImage правильные
        """
        self.user = get_user_model()
        self.author = self.user.objects.create_user(
            username='test_user',
            password='test123!',
            email='test1@example.com'
        )
        self.image = 'test.png'
        self.user_image = UserImage.objects.create(
            user=self.author,
            image=self.image
        )
        self.assertIsInstance(self.user_image, UserImage)
        self.assertIsInstance(self.user_image.user, self.user)
