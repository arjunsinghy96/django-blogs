import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blogs.models import Post, Upvote

class UpvoteTestCase(TestCase):

    def setUp(self):
        self.post1 = Post.objects.create(
            uuid=uuid.uuid4(),
            author='authoruser',
            heading='Post1 Heading',
            content='Post1 Content',
            slug='post1-heading-abcd',
            is_published=True,
        )
        self.post2 = Post.objects.create(
            uuid=uuid.uuid4(),
            author='authoruser',
            heading='Post2 Heading',
            content='Post2 Content',
            slug='post2-heading-abcd',
            is_published=False,
        )
        self.url1 = reverse("blogs:upvote", kwargs={'uuid': self.post1.uuid})
        self.url2 = reverse("blogs:upvote", kwargs={'uuid': self.post2.uuid})

        self.upvote1 = Upvote.objects.create(
            post=self.post1,
            fingerprint="uniquefingerprint"
        )
    
    def test_new_upvote_created_on_get_for_post(self):
        """
        Tests that a new upvote is created.
        """
        data = {
            'fingerprint': 'newuniquefingerprint1',
        }
        response = self.client.get(self.url1, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post1.upvote_set.count(), 2)
        self.assertEqual(self.post2.upvote_set.count(), 0)
    
    def test_200_on_get_with_false(self):
        """
        Tests that when the fingerprint has not upvoted, get
        returns 200 with is_updated False.
        """
        data = {
            'fingerprint': 'newuniquefingerprint2',
        }
        response = self.client.get(self.url2, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['is_upvoted'])
    
    def test_200_on_get_with_true(self):
        """
        Tests that when the fingerprint has upvoted, get
        returns 200 with is_updated True
        """
        data = {
            'fingerprint': 'newuniquefingerprint3',
        }
        response = self.client.post(self.url2, data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.url2, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_upvoted'])
    
    def test_400_bad_request_without_fingerprint(self):
        """
        Tests that the fingerprint is mandatory in GET and POST
        """
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, 400)
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 400)
    
    def test_post_toggles_upvote_status(self):
        """
        Tests that each POST request toggles the is_upvoted attribute.
        """
        data = {
            'fingerprint': 'uniquefingerprint',
        }
        response = self.client.post(self.url1, data=data)
        self.assertEqual(response.status_code, 200)
        upvote = Upvote.objects.get(pk=self.upvote1.id)
        self.assertTrue(upvote.is_upvoted)
        response = self.client.post(self.url1, data=data)
        self.assertEqual(response.status_code, 200)
        upvote = Upvote.objects.get(pk=self.upvote1.id)
        self.assertFalse(upvote.is_upvoted)