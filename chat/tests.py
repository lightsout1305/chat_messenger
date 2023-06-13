"""
Модульные тесты приложения chat
"""
import typing
import requests
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from requests import Response
from environ import environ
from .models import GroupMessages, Messages, GroupChat, UserImage


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


class TestGroupMessagesDatabase(TestCase):
    """
    Тестирование таблицы GroupMessages
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
        self.groupmessage = GroupMessages.objects.create(
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
        self.assertTrue(self.groupmessage)

    def test_message_data_is_correct(self) -> None:
        """
        Тест-кейс, проверяющий, все ли данные сохранились
        """
        self.data_for_tests()
        self.assertEqual(self.groupmessage.message, self.text)
        self.assertEqual(self.groupmessage.author, self.author)
        self.assertEqual(self.groupmessage.group_chat, self.group_chat)

    def test_message_data_type_is_correct(self) -> None:
        """
        Тест-кейс, проверяющий, правильные ли типы данных у сообщения
        """
        self.data_for_tests()
        self.assertIsInstance(self.groupmessage.message, str)
        self.assertIsInstance(self.groupmessage.created, timezone.datetime)
        self.assertIsInstance(self.groupmessage.modified, timezone.datetime)
        self.assertIsInstance(self.groupmessage.author, self.user)
        self.assertIsInstance(self.groupmessage.group_chat, GroupChat)


class TestMessageDatabase(TestCase):
    """
    Тестирование таблицы Messages
    """
    text: str
    user: typing.Type[get_user_model]
    author: typing.Type[get_user_model]
    created: timezone.timezone
    modified: timezone.timezone
    recipient: typing.Type[get_user_model]
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
        self.recipient = self.user.objects.create_user(
            username='test_user2',
            email='testuser2@example.com',
            password='Test123!'
        )
        self.message = Messages.objects.create(
            message=self.text,
            author=self.author,
            created=self.created,
            modified=self.modified,
            recipient=self.recipient
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
        self.assertEqual(self.message.author, self.author)
        self.assertEqual(self.message.recipient, self.recipient)

    def test_message_data_type_is_correct(self) -> None:
        """
        Тест-кейс, проверяющий, правильные ли типы данных у сообщения
        """
        self.data_for_tests()
        self.assertIsInstance(self.message.message, str)
        self.assertIsInstance(self.message.created, timezone.datetime)
        self.assertIsInstance(self.message.modified, timezone.datetime)
        self.assertIsInstance(self.message.author, self.user)
        self.assertIsInstance(self.message.recipient, self.user)


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


class TestGetMessagesAPI(TestCase):
    """
    Тестирование метода GetMessages
    """
    env = environ.Env()
    env.read_env()
    credentials: tuple = (env.str("LOGIN"), env.str("PASSWORD"))
    unauthorized_api: Response = requests.get("http://127.0.0.1:8000/api/messages")
    authorized_api: Response = requests.get("http://127.0.0.1:8000/api/messages", auth=credentials)
    api_with_author: Response = requests.get("http://127.0.0.1:8000/api/messages?author=lightsout",
                                             auth=credentials)
    api_with_nonexistent_author: Response = requests.get("http://127.0.0.1:8000/api/messages?author=zorro",
                                                         auth=credentials)
    api_with_recipient: Response = requests.get("http://127.0.0.1:8000/api/messages?recipient=raymond",
                                                auth=credentials)
    api_with_nonexistent_recipient: Response = requests.get("http://127.0.0.1:8000/api/messages?recipient=lol",
                                                            auth=credentials)
    api_with_both_author_and_recipient: Response = requests.get("http://127.0.0.1:8000/api/messages?author=lightsout"
                                                                "&recipient=raymond", auth=credentials)
    api_with_at_least_one_nonexistent_person: Response = requests.get("http://127.0.0.1:8000/api/messages?author"
                                                                      "=lightsout&recipient=kek", auth=credentials)

    def test_messages_return_200_if_authorized(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_messages_return_403_if_unauthorized(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_return_messages_with_author(self) -> None:
        """
        Тестирование, что метод возвращает все сообщения определенного автора
        """
        author: Response = self.api_with_author.json()[0]['author']
        self.assertEqual(author, 1)

    def test_return_messages_with_nonexistent_author(self) -> None:
        """
        Тестирование, что метод возвращает пустое тело ответа, если несуществующий автор
        """
        author: Response = self.api_with_nonexistent_author.json()
        self.assertFalse(author)

    def test_return_messages_with_recipient(self) -> None:
        """
        Тестирование, что метод возвращает все сообщения определенного адресата
        """
        recipient: Response = self.api_with_recipient.json()[0]['recipient']
        self.assertEqual(recipient, 5)

    def test_return_messages_with_nonexistent_recipient(self) -> None:
        """
        Тестирование, что метод возвращает пустое тело ответа, если несуществующий адресат
        """
        recipient: Response = self.api_with_nonexistent_recipient.json()
        self.assertFalse(recipient)

    def test_return_message_with_one_nonexistent_person(self) -> None:
        """
        Тестирование, что метод возвращает пустое тело ответа, если хотя бы одного человека не существует
        """
        one_person_absent: Response = self.api_with_at_least_one_nonexistent_person.json()
        self.assertFalse(one_person_absent)

    def test_return_message_with_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все обязательные поля
        """
        message_id: int = self.authorized_api.json()[0]['id']
        message: str = self.authorized_api.json()[0]['message']
        author: id = self.authorized_api.json()[0]['author']
        recipient: id = self.authorized_api.json()[0]['recipient']
        created: str = self.authorized_api.json()[0]['created']
        modified: str = self.authorized_api.json()[0]['modified']
        self.assertTrue(message_id)
        self.assertTrue(message)
        self.assertTrue(author)
        self.assertTrue(recipient)
        self.assertTrue(created)
        self.assertTrue(modified)


class TestCreateMessageAPI(TestCase):
    """
    Тестирование API CreateMessage
    """
    env = environ.Env()
    env.read_env()
    credentials: tuple = (env.str("LOGIN"), env.str("PASSWORD"))
    message: str = "Hello from tests"
    author: int = 5
    recipient: int = 1
    data: dict = {
        "message": message,
        "author": author,
        "recipient": recipient
    }
    bad_data: dict = {
        "message": message,
    }
    unauthorized_api: Response = requests.post("http://127.0.0.1:8000/api/messages/create/")
    authorized_api: Response = requests.post("http://127.0.0.1:8000/api/messages/create/", auth=credentials,
                                             data=data)
    unsuccessful_api: Response = requests.post("http://127.0.0.1:8000/api/messages/create/", auth=credentials,
                                               data=bad_data)

    def test_create_message_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 и сообщение успешно создается
        """
        content = self.authorized_api.json()
        self.assertEqual(self.authorized_api.status_code, 201)
        self.assertEqual(content["message"], self.message)
        self.assertEqual(content["author"], self.author)
        self.assertEqual(content["recipient"], self.recipient)

    def test_create_message_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_create_message_returns_400(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)


class TestGetGroupMessagesAPI(TestCase):
    """
    Тестирование API GetGroupMessages
    """
    env = environ.Env()
    env.read_env()
    credentials: tuple = (env.str("LOGIN"), env.str("PASSWORD"))
    unauthorized_api: Response = requests.get('http://127.0.0.1:8000/api/groupmessages')
    authorized_api: Response = requests.get('http://127.0.0.1:8000/api/groupmessages', auth=credentials)
    api_with_group_chat: Response = requests.get('http://127.0.0.1:8000/api/groupmessages?group-chat=french-group',
                                                 auth=credentials)
    api_with_nonexistent_group_chat: Response = requests.get('http://127.0.0.1:8000/api/groupmessages?group-chat=lel',
                                                             auth=credentials)

    def test_group_messages_return_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_group_messages_have_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все обязательные поля
        """
        message_id: int = self.authorized_api.json()[0]['id']
        message: str = self.authorized_api.json()[0]['message']
        author: id = self.authorized_api.json()[0]['author']
        group_chat: id = self.authorized_api.json()[0]['group_chat']
        created: str = self.authorized_api.json()[0]['created']
        modified: str = self.authorized_api.json()[0]['modified']
        self.assertTrue(message_id)
        self.assertTrue(message)
        self.assertTrue(author)
        self.assertTrue(group_chat)
        self.assertTrue(created)
        self.assertTrue(modified)

    def test_group_messages_return_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_group_messages_with_group_chat_returns_200_and_body(self) -> None:
        """
        Тестирование, что метод с фильтрацией по групповому чату возвращает непустое тело
        ответа со всеми обязательными полями
        """
        message_id: int = self.api_with_group_chat.json()[0]['id']
        message: str = self.api_with_group_chat.json()[0]['message']
        author: id = self.api_with_group_chat.json()[0]['author']
        group_chat: id = self.api_with_group_chat.json()[0]['group_chat']
        created: str = self.api_with_group_chat.json()[0]['created']
        modified: str = self.api_with_group_chat.json()[0]['modified']
        self.assertTrue(message_id)
        self.assertTrue(message)
        self.assertTrue(author)
        self.assertTrue(group_chat)
        self.assertTrue(created)
        self.assertTrue(modified)

    def test_group_messages_with_nonexistent_group_chat_returns_200(self) -> None:
        """
        Тестирование, что метод с фильтрацией по несуществующему групповому чату
        возвращает 200 с пустым телом ответа
        """
        self.assertEqual(self.api_with_nonexistent_group_chat.status_code, 200)
        self.assertFalse(self.api_with_nonexistent_group_chat.json())


