import json
from api.views import get_search_result
from api.models import Comment
import pytest
from mixer.backend.django import mixer


class Dumb_request:
    def __init__(self, GET):
        self.GET = GET


@pytest.mark.django_db
def test_get_search_result():
    request = Dumb_request({'request': 'comment'})

    comment1 = mixer.blend(Comment, content='1233comment123')
    comment2 = mixer.blend(Comment)

    res = get_search_result(request)

    res = res.content.decode('utf8')
    res = json.loads(res)
    res = res['search comments'][0]
    assert res['content'] == '1233comment123'
