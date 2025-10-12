from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('blog:register')
        self.login_url = reverse('blog:login')
        self.profile_url = reverse('blog:profile')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }

    def test_register_creates_user_and_redirects(self):
        resp = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(resp.status_code, 302)  # redirect to profile
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_profile_requires_login(self):
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, 302)  # redirect to login
        # login then access
        User.objects.create_user(username='u', email='u@test.com', password='p')
        self.client.login(username='u', password='p')
        resp2 = self.client.get(self.profile_url)
        self.assertEqual(resp2.status_code, 200)


class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass123')
        self.other = User.objects.create_user(username='other', password='pass123')
        self.post = Post.objects.create(title='First', content='Hello world', author=self.user)

    def test_list_view_accessible(self):
        url = reverse('blog:post-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)

    def test_detail_view(self):
        url = reverse('blog:post-detail', kwargs={'pk': self.post.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.content)

    def test_create_requires_login(self):
        url = reverse('blog:post-create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # redirect to login

        self.client.login(username='author', password='pass123')
        resp2 = self.client.post(url, {'title': 'New', 'content': 'content'})
        # after successful creation, CreateView redirects to detail page (default)
        self.assertEqual(resp2.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New').exists())

    def test_update_only_author(self):
        url = reverse('blog:post-update', kwargs={'pk': self.post.pk})
        # other user cannot access update
        self.client.login(username='other', password='pass123')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)  # UserPassesTestMixin returns 403 by default

        # author can access and update
        self.client.login(username='author', password='pass123')
        resp2 = self.client.post(url, {'title': 'Updated', 'content': 'new'})
        self.assertEqual(resp2.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated')

    def test_delete_only_author(self):
        url = reverse('blog:post-delete', kwargs={'pk': self.post.pk})
        self.client.login(username='other', password='pass123')
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)
        self.client.login(username='author', password='pass123')
        resp2 = self.client.post(url)
        self.assertEqual(resp2.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

class CommentTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.post = Post.objects.create(title='T', content='C', author=self.author)
        self.comment = Comment.objects.create(post=self.post, author=self.author, content='First comment')

    def test_create_comment_requires_login(self):
        url = reverse('blog:comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Hi'})
        self.assertEqual(resp.status_code, 302)  # redirect to login

        self.client.login(username='other', password='pass')
        resp2 = self.client.post(url, {'content': 'Hi'})
        self.assertEqual(resp2.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='Hi', author=self.other).exists())

    def test_edit_only_author(self):
        url = reverse('blog:comment-update', kwargs={'pk': self.comment.pk})
        self.client.login(username='other', password='pass')
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (302, 403))  # redirect or forbidden
        self.client.login(username='author', password='pass')
        resp2 = self.client.post(url, {'content': 'Edited'})
        self.assertEqual(resp2.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Edited')

    def test_delete_only_author(self):
        url = reverse('blog:comment-delete', kwargs={'pk': self.comment.pk})
        self.client.login(username='other', password='pass')
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 403))
        self.client.login(username='author', password='pass')
        resp2 = self.client.post(url)
        self.assertEqual(resp2.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())


class TagAndSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.post1 = Post.objects.create(title='Django tips', content='Search me', author=self.user)
        self.post2 = Post.objects.create(title='Python tricks', content='Useful content', author=self.user)
        tag = Tag.objects.create(name='django')
        self.post1.tags.add(tag)

    def test_posts_by_tag(self):
        url = reverse('blog:posts-by-tag', kwargs={'tag_name': 'django'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django tips')
        self.assertNotContains(resp, 'Python tricks')

    def test_search_by_title_content_tag(self):
        url = reverse('blog:search') + '?q=Search'
        resp = self.client.get(url)
        self.assertContains(resp, 'Django tips')

        url2 = reverse('blog:search') + '?q=django'
        resp2 = self.client.get(url2)
        self.assertContains(resp2, 'Django tips')