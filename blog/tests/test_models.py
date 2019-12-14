import datetime

from unittest.mock import patch

from blog.models import Link, Category, Tag, Post


def mock_now():
    return datetime.datetime(2016, 1, 1, 0, 0, 0, 0)


class TestLink:
    def test_str(self):
        link = Link(title="foo", url="http://foo.com")
        assert str(link) == "foo"


class TestCategory:
    def test_str(self):
        category = Category(name="foo")
        assert str(category) == "foo"


class TestTag:
    def test_str(self):
        tag = Tag(name="foo")
        assert str(tag) == "foo"


class TestPost:
    def test_str(self):
        post = Post(title="foo", slug="bar", body="the body",)

        assert str(post) == "foo"

    @patch("blog.models.datetime")
    def test_get_now(self, mock_datetime):
        expected = mock_now()
        mock_datetime.now.return_value = expected
        assert Post.get_now() == expected

    @patch("blog.models.Post.get_now", side_effect=mock_now)
    def test_published_when_published(self, now):
        go_live_date = mock_now()

        post = Post(title="foo", slug="bar", body="the body", go_live_date=go_live_date)

        assert post.published()

    @patch("blog.models.Post.get_now", side_effect=mock_now)
    def test_published_when_not_published(self, now):
        go_live_date = mock_now() + datetime.timedelta(days=1)

        post = Post(title="foo", slug="bar", body="the body", go_live_date=go_live_date)

        assert not post.published()
