from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from .models import Post

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
})
class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a small dummy image
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.cover_image = SimpleUploadedFile('test.gif', small_gif, content_type='image/gif')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            body='This is a test post body.',
            published=True,
            cover_image=self.cover_image
        )

    def test_post_list_page(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_page(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post body.')

    @patch('boto3.client')
    def test_presigned_view_requires_auth_or_public(self, mock_boto):
        # Mock the presigned URL generation
        mock_s3 = mock_boto.return_value
        mock_s3.generate_presigned_url.return_value = 'https://rustfs.dsreed.net/api/blog-media/media/posts/test.gif?signed=true'
        
        url = reverse('blog:post_cover_redirect', kwargs={'post_id': self.post.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue('rustfs.dsreed.net' in response.url)
        mock_s3.generate_presigned_url.assert_called_once()

    def test_presigned_view_denies_private_post_for_anonymous(self):
        private_post = Post.objects.create(
            title='Private Post',
            slug='private-post',
            body='Secret content',
            published=False
        )
        url = reverse('blog:post_cover_redirect', kwargs={'post_id': private_post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
