import datetime

from unittest import TestCase
from unittest.mock import patch

from blog.models import Link, Category, Tag, Post


def mock_now():
    return datetime.datetime(2016, 1, 1, 0, 0, 0, 0)


class LinkTestCase(TestCase):

    def test_str(self):
        link = Link(title='foo', url='http://foo.com')
        self.assertEqual('foo', str(link))


class CategoryTestCase(TestCase):

    def test_str(self):
        category = Category(name='foo')
        self.assertEqual('foo', str(category))


class TagTestCase(TestCase):

    def test_str(self):
        tag = Tag(name='foo')
        self.assertEqual('foo', str(tag))


class PostTestCase(TestCase):

    def test_str(self):
        post = Post(
            title='foo',
            slug='bar',
            body='the body',
        )

        self.assertEqual('foo', str(post))

    @patch('blog.models.datetime')
    def test_get_now(self, mock_datetime):
        expected = mock_datetime.datetime(2016, 1, 1, 0, 0, 0, 0)
        mock_datetime.now.return_value = expected
        self.assertEqual(expected, Post.get_now())

    @patch('blog.models.Post.get_now', side_effect=mock_now)
    def test_published_when_published(self, now):
        go_live_date = mock_now()

        post = Post(
            title='foo',
            slug='bar',
            body='the body',
            go_live_date=go_live_date
        )

        self.assertTrue(post.published())

    @patch('blog.models.Post.get_now', side_effect=mock_now)
    def test_published_when_not_published(self, now):
        go_live_date = mock_now() + datetime.timedelta(days=1)

        post = Post(
            title='foo',
            slug='bar',
            body='the body',
            go_live_date=go_live_date
        )

        self.assertFalse(post.published())
