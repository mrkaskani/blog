from freezegun import freeze_time

from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .models import Post
from .views import About


class AboutMePageViewTest(TestCase):
    def setUp(self):
        url = reverse('about_me')
        self.response = self.client.get(url)

    def test_about_me_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_me_template(self):
        self.assertTemplateUsed(self.response, 'blog/about.html')

    def test_about_me_contains_correct_html(self):
        self.assertContains(self.response, 'Tell About Yourself')

    def test_about_me_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_about_me(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, About.as_view().__name__)


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()

        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class TodoPostTestModel(TestCase):

    @classmethod
    @freeze_time("2022-02-02 02:02:02")
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            username='username',
            email='email@mail.com',
            password='testpass123'
        )
        Post.objects.create(
            author_id=user.id,
            title='a title',
            slug='a_slug',
            body='a body here',
            image='post_test/test.jpg',
            created_at='',
            updated_at='',
            published_at='',
            publish=True
        )

    def test_author_id_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.author_id
        self.assertEquals(expected_object_name, 3)

    def test_title_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEquals(expected_object_name, 'a title')

    def test_slug_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.slug}'
        self.assertEquals(expected_object_name, 'a_slug')

    def test_body_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.body}'
        self.assertEquals(expected_object_name, 'a body here')

    def test_created_at_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.created_at}'
        self.assertEquals(expected_object_name, '2022-02-02 02:02:02+00:00')

    def test_update_at_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.updated_at}'
        self.assertEquals(expected_object_name, '2022-02-02 02:02:02+00:00')

    def test_published_at_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.published_at}'
        self.assertEquals(expected_object_name, '2022-02-02 02:02:02+00:00')

    def test_publish_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.publish
        self.assertEquals(expected_object_name, True)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'a body here')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get('/posts/a_slug/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'a body here')
        self.assertTemplateUsed(response, 'blog/post_detail.html')
