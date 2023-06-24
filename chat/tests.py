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


class TestUserImageDatabase(TestCase):
    """
    Тестирование таблицы UserImage
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
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    unauthorized_api: Response = requests.get("http://127.0.0.1:8000/api/messages",
                                              timeout=5)
    authorized_api: Response = requests.get("http://127.0.0.1:8000/api/messages",
                                            auth=credentials,
                                            timeout=5)
    api_with_author: Response = \
        requests.get("http://127.0.0.1:8000/api/messages?author=lightsout",
                     auth=credentials,
                     timeout=5)
    api_with_nonexistent_author: Response = \
        requests.get("http://127.0.0.1:8000/api/messages?author=zorro",
                     auth=credentials,
                     timeout=5)
    api_with_recipient: Response = \
        requests.get("http://127.0.0.1:8000/api/messages?recipient=raymond",
                     auth=credentials,
                     timeout=5)
    api_with_nonexistent_recipient: Response = \
        requests.get("http://127.0.0.1:8000/api/messages?recipient=lol",
                     auth=credentials,
                     timeout=5)
    api_with_both_author_and_recipient: Response = \
        requests.get("http://127.0.0.1:8000/api/messages?author=lightsout"
                     "&recipient=raymond", auth=credentials,
                     timeout=5)
    api_with_at_least_one_nonexistent_person: Response = \
        requests.get("http://127.0.0.1:8000/api/messages?author"
                     "=lightsout&recipient=kek", auth=credentials,
                     timeout=5)
    message_id: int = 1
    message: str = "Salut!"
    author: typing.Callable = env.int("USER_ID")
    recipient: typing.Callable = env.int("RECIPIENT_ID")
    created: str = '2023-06-11T20:33:03.462882Z'
    modified: str = '2023-06-11T20:33:03.462882Z'
    count_model: int = Messages.objects.count()

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
        Тестирование, что метод возвращает пустое тело ответа,
        если несуществующий автор
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
        Тестирование, что метод возвращает пустое тело ответа,
        если несуществующий адресат
        """
        recipient: Response = self.api_with_nonexistent_recipient.json()
        self.assertFalse(recipient)

    def test_return_message_with_one_nonexistent_person(self) -> None:
        """
        Тестирование, что метод возвращает пустое тело ответа,
        если хотя бы одного человека не существует
        """
        one_person_absent: Response = \
            self.api_with_at_least_one_nonexistent_person.json()
        self.assertFalse(one_person_absent)

    def test_return_message_with_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все обязательные поля
        """
        content: dict = self.authorized_api.json()
        self.assertTrue(content[0]["id"], self.message_id)
        self.assertTrue(content[0]["message"], self.message)
        self.assertTrue(content[0]["author"], self.author)
        self.assertTrue(content[0]["recipient"], self.recipient)
        self.assertTrue(content[0]["created"], self.created)
        self.assertTrue(content[0]["modified"], self.modified)

    def test_get_messages_have_all_records(self) -> None:
        """
        Тестирование, что метод возвращает все сообщения
        """
        count: int = 0

        for _ in self.authorized_api.json():
            count += 1
        self.assertEqual(self.count_model, count)


class TestCreateMessageAPI(TestCase):
    """
    Тестирование API CreateMessage
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    message: str = "Hello from tests"
    author: int = 5
    recipient: int = 1
    good_data: dict = {
        "message": message,
        "author": author,
        "recipient": recipient
    }
    bad_data: dict = {
        "message": message,
    }
    unauthorized_api: Response = requests.post("http://127.0.0.1:8000/api/messages/create/",
                                               timeout=5)
    authorized_api: Response = requests.post("http://127.0.0.1:8000/api/messages/create/",
                                             auth=credentials,
                                             json=good_data,
                                             timeout=5)
    unsuccessful_api: Response = requests.post("http://127.0.0.1:8000/api/messages/create/",
                                               auth=credentials,
                                               json=bad_data,
                                               timeout=5)

    def test_create_message_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 и сообщение успешно создается
        """
        content: dict = self.authorized_api.json()
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
    env: environ.Env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    unauthorized_api: Response = requests.get('http://127.0.0.1:8000/api/groupmessages',
                                              timeout=5)
    authorized_api: Response = requests.get('http://127.0.0.1:8000/api/groupmessages',
                                            auth=credentials,
                                            timeout=5)
    api_with_group_chat: Response = \
        requests.get('http://127.0.0.1:8000/api/groupmessages?group-chat=french-group',
                     auth=credentials,
                     timeout=5)
    api_with_nonexistent_group_chat: Response = \
        requests.get('http://127.0.0.1:8000/api/groupmessages?group-chat=lel',
                     auth=credentials,
                     timeout=5)
    message_id: int = 1
    message: str = "Test"
    author: typing.Callable = env.int("USER_ID")
    group_chat: int = 1
    created: str = '2023-06-11T20:31:39.163859Z'
    modified: str = '2023-06-11T20:31:39.163859Z'
    count_model: int = GroupMessages.objects.count()

    def test_group_messages_return_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_group_messages_have_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все обязательные поля
        """
        self.assertTrue(self.message_id)
        self.assertTrue(self.message)
        self.assertTrue(self.author)
        self.assertTrue(self.group_chat)
        self.assertTrue(self.created)
        self.assertTrue(self.modified)

    def test_group_messages_have_required_data_type(self) -> None:
        """
        Тестирование, что у полей метода запланированные типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content[0]["message"], str)
        self.assertIsInstance(content[0]["author"], int)
        self.assertIsInstance(content[0]["group_chat"], int)
        self.assertIsInstance(content[0]["created"], str)
        self.assertIsInstance(content[0]["modified"], str)

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
        author: int = self.api_with_group_chat.json()[0]['author']
        group_chat: int = self.api_with_group_chat.json()[0]['group_chat']
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

    def test_group_messages_return_all_records(self) -> None:
        """
        Тестирование, что метод возвращает все групповые сообщения
        """
        count: int = 0

        for _ in self.authorized_api.json():
            count += 1
        self.assertEqual(self.count_model, count)


class TestCreateGroupMessagesAPI(TestCase):
    """
    Тестирование метода CreateGroupMessages
    """
    env: environ.Env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    message: str = "Hello from tests"
    author: int = 5
    group: int = 1
    good_data: dict = {
        "message": message,
        "author": author,
        "group_chat": group
    }
    bad_data: dict = {
        "message": message,
    }
    unauthorized_api: Response = \
        requests.post("http://127.0.0.1:8000/api/groupmessages/create/", timeout=5)
    authorized_api: Response = \
        requests.post("http://127.0.0.1:8000/api/groupmessages/create/",
                      auth=credentials,
                      json=good_data,
                      timeout=5)
    unsuccessful_api: Response = \
        requests.post("http://127.0.0.1:8000/api/groupmessages/create/",
                      auth=credentials,
                      json=bad_data,
                      timeout=5)

    def test_create_group_messages_returns_201(self) -> None:
        """
        Тестирование, что метод возвращает 200 и создается групповое сообщение
        """
        content = self.authorized_api.json()
        self.assertEqual(self.authorized_api.status_code, 201)
        self.assertEqual(content["message"], self.message)
        self.assertEqual(content["author"], self.author)
        self.assertEqual(content["group_chat"], self.group)

    def test_create_group_messages_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_create_group_messages_returns_400(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)


class TestGetUsersAPI(TestCase):
    """
    Тестирование метода GetUsers
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    authorized_api: Response = requests.get('http://127.0.0.1:8000/api/users/',
                                            auth=credentials,
                                            timeout=5)
    unauthorized_api: Response = requests.get('http://127.0.0.1:8000/api/users/',
                                              timeout=5)
    user_id: int = env.int("USER_ID")
    username: str = env.str("LOGIN")
    first_name: str = env.str("FIRST_NAME")
    last_name: str = env.str("LAST_NAME")
    count_model: int = get_user_model().objects.count()

    def test_get_users_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 с непустым телом ответа
        """
        self.assertEqual(self.authorized_api.status_code, 200)
        self.assertTrue(self.authorized_api.json())

    def test_get_users_have_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content[0]["id"], self.user_id)
        self.assertEqual(content[0]["username"], self.username)
        self.assertEqual(content[0]["first_name"], self.first_name)
        self.assertEqual(content[0]["last_name"], self.last_name)

    def test_get_users_returns_all_users(self) -> None:
        """
        Тестирование, что метод возвращает всех пользователей
        """
        count: int = 0
        for _ in self.authorized_api.json():
            count += 1
        self.assertEqual(self.count_model, count)

    def test_get_users_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestGetUserInfoAPI(TestCase):
    """
    Тестирование метода GetUserInfo
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    authorized_api: Response = requests.get('http://127.0.0.1:8000/api/users/1/',
                                            auth=credentials,
                                            timeout=5)
    unauthorized_api: Response = requests.get('http://127.0.0.1:8000/api/users/1/',
                                              timeout=5)
    unsuccessful_api: Response = requests.get('http://127.0.0.1:8000/api/users/2/',
                                              auth=credentials,
                                              timeout=5)
    user_id: int = env.int("USER_ID")
    username: str = env.str("LOGIN")
    first_name: str = env.str("FIRST_NAME")
    last_name: str = env.str("LAST_NAME")

    def test_get_user_info_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_get_user_info_returns_necessary_fields(self) -> None:
        """
        Тестирование, что метод возвращает необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["id"], self.user_id)
        self.assertEqual(content["username"], self.username)
        self.assertEqual(content["first_name"], self.first_name)
        self.assertEqual(content["last_name"], self.last_name)

    def test_get_user_info_returns_correct_data_type(self) -> None:
        """
        Тестирование, что метод возвращает правильные типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["id"], int)
        self.assertIsInstance(content["username"], str)
        self.assertIsInstance(content["first_name"], str)
        self.assertIsInstance(content["last_name"], str)

    def test_get_user_info_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_get_user_info_returns_404(self) -> None:
        """
        Тестирование, что метод возвращает 404
        """
        self.assertEqual(self.unsuccessful_api.status_code, 404)


class TestUpdateUserInfoAPI(TestCase):
    """
    Тестирование метода UpdateUserInfo
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN_2"), env.str("PASSWORD"))
    user_id: int = env.int("RECIPIENT_ID")
    username: str = env.str("LOGIN_2")
    first_name: str = "Raymond"
    last_name: str = "Grant"
    good_data: dict = {
        "id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name
    }
    bad_data: dict = {
        "first_name": first_name
    }
    authorized_api: Response = requests.put('http://127.0.0.1:8000/api/users/5/update/',
                                            auth=credentials,
                                            json=good_data,
                                            timeout=5)
    unauthorized_api: Response = requests.put('http://127.0.0.1:8000/api/users/5/update/',
                                              json=good_data,
                                              timeout=5)
    forbidden_api: Response = requests.put('http://127.0.0.1:8000/api/users/1/update/',
                                           auth=credentials,
                                           json=good_data,
                                           timeout=5)
    unsuccessful_api: Response = requests.put('http://127.0.0.1:8000/api/users/5/update/',
                                              auth=credentials,
                                              json=bad_data,
                                              timeout=5)

    def test_update_user_info_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_update_user_info_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает необходимые поля
        """
        self.assertEqual(self.authorized_api.json()["id"], self.user_id)
        self.assertEqual(self.authorized_api.json()["username"], self.username)
        self.assertEqual(self.authorized_api.json()["first_name"], self.first_name)
        self.assertEqual(self.authorized_api.json()["last_name"], self.last_name)

    def test_update_user_info_has_correct_data_type(self) -> None:
        """
        Тестирование, что метод возвращает запланированные типы данных
        """
        self.assertIsInstance(self.authorized_api.json()["id"], int)
        self.assertIsInstance(self.authorized_api.json()["username"], str)
        self.assertIsInstance(self.authorized_api.json()["first_name"], str)
        self.assertIsInstance(self.authorized_api.json()["last_name"], str)

    def test_update_user_info_returns_403_if_unauthorized(self) -> None:
        """
        Тестирование, что метод возвращает 403, если пользователь не авторизован
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_update_user_info_returns_403_if_different_user(self) -> None:
        """
        Тестирование, что метод возвращает 403, если пользователь не владелец профиля
        и не администратор
        """
        self.assertEqual(self.forbidden_api.status_code, 403)

    def test_update_user_info_returns_400(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)


class TestGetGroupChatAPI(TestCase):
    """
    Тестирование метода GetGroupChats
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    group_id: int = 1
    title: str = "Test group chat"
    slug: str = "test-group-chat"
    count_model: int = GroupChat.objects.filter(deleted=None).count()
    authorized_api: Response = requests.get('http://127.0.0.1:8000/api/groupchats/',
                                            auth=credentials,
                                            timeout=5)
    unauthorized_api: Response = requests.get('http://127.0.0.1:8000/api/groupchats/',
                                              timeout=5)

    def test_get_group_chats_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_get_group_chats_have_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content[0]["id"], self.group_id)
        self.assertEqual(content[0]["title"], self.title)
        self.assertEqual(content[0]["slug"], self.slug)

    def test_get_group_chats_have_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content[0]["id"], int)
        self.assertIsInstance(content[0]["title"], str)
        self.assertIsInstance(content[0]["slug"], str)

    def test_get_group_chats_return_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)

    def test_get_group_chats_return_all_records(self) -> None:
        """
        Тестирование, что метод возвращает все записи
        """
        count: int = 0
        for _ in self.authorized_api.json():
            count += 1
        self.assertEqual(count, self.count_model)


class TestCreateGroupChat(TestCase):
    """
    Тестирование метода CreateGroupChat
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    title: str = "Hello from tests"
    slug: str = "hello-from-tests"
    good_data: dict = {
        "title": title,
        "slug": slug
    }
    bad_data: dict = {
        "slug": slug
    }
    authorized_api: Response = requests.post("http://127.0.0.1:8000/api/groupchats/create/",
                                             auth=credentials,
                                             json=good_data,
                                             timeout=5)
    unauthorized_api: Response = requests.post("http://127.0.0.1:8000/api/groupchats/create/",
                                               json=good_data,
                                               timeout=5)
    unsuccessful_api: Response = requests.post("http://127.0.0.1:8000/api/groupchats/create/",
                                               auth=credentials,
                                               json=bad_data,
                                               timeout=5)

    def test_create_group_chat_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 и создает групповой чат
        """
        self.assertEqual(self.authorized_api.status_code, 201)

    def test_create_group_chat_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["title"], self.title)
        self.assertEqual(content["slug"], self.slug)

    def test_create_group_chat_has_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["title"], str)
        self.assertIsInstance(content["slug"], str)

    def test_create_group_chat_returns_400(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)

    def test_create_group_chat_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestUpdateGroupChat(TestCase):
    """
    Тестирование метода UpdateGroupChat
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    group_id: int = 3
    title: str = "Hello from tests modified"
    slug: str = "hello-from-tests-modified"
    data: dict = {
        "id": group_id,
        "title": title,
        "slug": slug
    }
    bad_data: dict = {
        "id": group_id,
        "slug": slug
    }
    authorized_api: Response = requests.put(
        f"http://127.0.0.1:8000/api/groupchats/{group_id}/update/",
        auth=credentials,
        json=data,
        timeout=5)
    unauthorized_api: Response = requests.put(
        f"http://127.0.0.1:8000/api/groupchats/{group_id}/update/",
        json=data,
        timeout=5)
    unsuccessful_api: Response = requests.put(
        f"http://127.0.0.1:8000/api/groupchats/{group_id}/update/",
        auth=credentials,
        json=bad_data,
        timeout=5)

    def test_update_group_chat_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_update_group_chat_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["id"], self.group_id)
        self.assertEqual(content["title"], self.title)
        self.assertEqual(content["slug"], self.slug)

    def test_update_group_chat_has_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["id"], int)
        self.assertIsInstance(content["title"], str)
        self.assertIsInstance(content["slug"], str)

    def test_update_group_chat_returns_400(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)

    def test_update_group_chat_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestDeleteGroupChat(TestCase):
    """
    Тестирование метода DeleteGroupChat
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    group_id: int = int(input("Введите id группы для удаления:\n"))
    good_data: dict = {
        "id": group_id
    }
    bad_data: dict = {
        "id": 4
    }
    authorized_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/groupchats/{group_id}/delete/",
        auth=credentials,
        json=good_data,
        timeout=5)
    unauthorized_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/groupchats/{group_id}/delete/",
        json=good_data,
        timeout=5)
    unsuccessful_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/groupchats/{group_id}/delete/",
        auth=credentials,
        data=bad_data,
        timeout=5)

    def test_delete_group_chat_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_delete_group_chat_returns_400(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)

    def test_delete_group_chat_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestGetGroupChatInfo(TestCase):
    """
    Тестирование метода GetGroupChatInfo
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN"), env.str("PASSWORD"))
    group_id: int = 2
    title: str = "French group"
    slug: str = "french-group"
    authorized_api: Response = requests.get(f"http://127.0.0.1:8000/api/groupchats/{group_id}/",
                                            auth=credentials,
                                            timeout=5)
    unauthorized_api: Response = requests.get(f"http://127.0.0.1:8000/api/groupchats/{group_id}/",
                                              timeout=5)
    unsuccessful_api: Response = requests.get("http://127.0.0.1:8000/api/groupchats/4/",
                                              auth=credentials,
                                              timeout=5)

    def test_get_group_chat_info_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_get_group_chat_info_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["id"], self.group_id)
        self.assertEqual(content["title"], self.title)
        self.assertEqual(content["slug"], self.slug)

    def test_get_group_chat_info_has_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["id"], int)
        self.assertIsInstance(content["title"], str)
        self.assertIsInstance(content["slug"], str)

    def test_get_group_chat_info_returns_404(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 404)

    def test_get_group_chat_info_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestGetUserImage(TestCase):
    """
    Тестирование метода GetUserImage
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN_3"), env.str("PASSWORD"))
    user_id: int = 6
    image_id: int = 5
    image: str = "/media/she.png"
    authorized_api: Response = requests.get(f"http://127.0.0.1:8000/api/users/{user_id}/images/",
                                            auth=credentials,
                                            timeout=5)
    unauthorized_api: Response = requests.get(f"http://127.0.0.1:8000/api/users/{user_id}/images/",
                                              timeout=5)
    unsuccessful_api: Response = requests.get("http://127.0.0.1:8000/api/users/2/images/",
                                              auth=credentials,
                                              timeout=5)

    def test_get_user_image_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_get_user_image_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["id"], self.image_id)
        self.assertEqual(content["user"], self.user_id)
        self.assertEqual(content["image"], self.image)

    def test_get_user_image_has_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["id"], int)
        self.assertIsInstance(content["user"], int)
        self.assertIsInstance(content["image"], str)

    def test_get_user_image_returns_404(self) -> None:
        """
        Тестирование, что метод возвращает 404
        """
        self.assertEqual(self.unsuccessful_api.status_code, 404)

    def test_get_user_image_returns_403(self) -> None:
        """
        Тестирование, что метод возвращает 403
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestCreateUserImage(TestCase):
    """
    Тестирование метода CreateUserImage
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN_2"), env.str("PASSWORD"))
    user_id: int = 5
    image: str = "test_1.png"
    good_data: dict = {
        "user": user_id,
        "image": image
    }
    bad_data: dict = {
        "image": None,
        "user": user_id
    }
    authorized_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/create/",
        auth=credentials,
        json=good_data,
        timeout=5)
    authorized_api_again: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/create/",
        auth=credentials,
        json=good_data,
        timeout=5)
    unauthorized_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/create/",
        json=good_data,
        timeout=5)
    unsuccessful_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/create/",
        auth=credentials,
        json=bad_data,
        timeout=5)
    forbidden_api: Response = requests.post(
        "http://127.0.0.1:8000/api/users/1/images/create/",
        auth=credentials,
        json=good_data,
        timeout=5)

    def test_create_user_image_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 и создает изображение
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_create_user_image_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает необходимыe поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["user"], self.user_id)
        self.assertEqual(content["image"], f"/media/{self.image}")

    def test_create_user_image_returns_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["user"], int)
        self.assertIsInstance(content["image"], str)

    def test_create_user_image_returns_400_if_bad_data(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)

    def test_create_user_image_returns_400_if_image_exists(self) -> None:
        """
        Тестирование, что метод возвращает 400, если изображение уже существует
        """
        self.assertEqual(self.authorized_api_again.status_code, 400)

    def test_create_user_image_returns_403_if_different_user(self) -> None:
        """
        Тестирование, что метод возвращает 403, если не владелец профиля
        """
        self.assertEqual(self.forbidden_api.status_code, 403)

    def test_create_user_image_returns_403_if_unauthorized(self) -> None:
        """
        Тестирование, что метод возвращает 403, если пользователь не авторизован
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestUpdateUserImage(TestCase):
    """
    Тестирование метода UpdateUserImage
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN_2"), env.str("PASSWORD"))
    user_id: int = 5
    image: str = "test_updated.png"
    good_data: dict = {
        "user": user_id,
        "image": image
    }
    bad_data: dict = {
        "user": user_id,
        "image": None
    }
    authorized_api: Response = requests.put(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/update/",
        auth=credentials,
        json=good_data,
        timeout=5)
    unauthorized_api: Response = requests.put(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/update/",
        json=good_data,
        timeout=5)
    unsuccessful_api: Response = requests.put(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/update/",
        auth=credentials,
        json=bad_data,
        timeout=5)
    forbidden_api: Response = requests.put(
        "http://127.0.0.1:8000/api/users/6/images/update/",
        auth=credentials,
        json=good_data,
        timeout=5)

    def test_update_user_image_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 и обновляет изображение
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_update_user_image_has_required_fields(self) -> None:
        """
        Тестирование, что метод возвращает все необходимые поля
        """
        content: dict = self.authorized_api.json()
        self.assertEqual(content["user"], self.user_id)
        self.assertEqual(content["image"], f"/media/{self.image}")

    def test_update_user_image_has_required_data_type(self) -> None:
        """
        Тестирование, что метод возвращает необходимые типы данных
        """
        content: dict = self.authorized_api.json()
        self.assertIsInstance(content["id"], int)
        self.assertIsInstance(content["user"], int)
        self.assertIsInstance(content["image"], str)

    def test_update_user_image_returns_400_if_bad_data(self) -> None:
        """
        Тестирование, что метод возвращает 400
        """
        self.assertEqual(self.unsuccessful_api.status_code, 400)

    def test_update_user_image_returns_400_if_image_is_deleted(self) -> None:
        """
        Тестирование, что метод возвращает 400, если изображение удалено
        """
        requests.post(f"http://127.0.0.1:8000/api/users/{self.user_id}/images/delete/",
                      auth=self.credentials,
                      json=self.good_data,
                      timeout=5)
        api: Response = requests.put(
            f"http://127.0.0.1:8000/api/users/{self.user_id}/images/update/",
            auth=self.credentials,
            json=self.good_data,
            timeout=5)
        self.assertEqual(api.status_code, 400)

    def test_update_user_image_returns_403_if_different_user(self) -> None:
        """
        Тестирование, что метод возвращает 403, если не владелец профиля
        """
        self.assertEqual(self.forbidden_api.status_code, 403)

    def test_update_user_image_returns_403_if_unauthorized(self) -> None:
        """
        Тестирование, что метод возвращает 403, если не авторизован
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)


class TestDeleteUserImage(TestCase):
    """
    Тестирование метода DeleteUserImage
    """
    env = environ.Env()
    env.read_env()
    credentials: typing.Tuple[str, str] = (env.str("LOGIN_2"), env.str("PASSWORD"))
    user_id: int = 5
    forbidden_user_id: int = 6
    deletion_data: dict = {
        "user": user_id,
    }
    authorized_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/delete/",
        auth=credentials,
        json=deletion_data,
        timeout=5)
    unauthorized_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/images/delete/",
        json=deletion_data,
        timeout=5)
    forbidden_api: Response = requests.post(
        f"http://127.0.0.1:8000/api/users/{forbidden_user_id}/images/delete/",
        auth=credentials,
        json=deletion_data,
        timeout=5)

    def test_delete_user_image_returns_200(self) -> None:
        """
        Тестирование, что метод возвращает 200 и удаляет изображение
        """
        self.assertEqual(self.authorized_api.status_code, 200)

    def test_delete_user_image_returns_403_if_different_user(self) -> None:
        """
        Тестирование, что метод возвращает 403, если не владелец профиля
        """
        self.assertEqual(self.forbidden_api.status_code, 403)

    def test_delete_user_image_returns_403_if_unauthorized(self) -> None:
        """
        Тестирование, что метод возвращает 403, если не авторизован
        """
        self.assertEqual(self.unauthorized_api.status_code, 403)
