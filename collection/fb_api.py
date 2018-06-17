from urllib.parse import urlencode
from collection import json_request as jr

BASE_URL_FB_API = 'https://graph.facebook.com/v3.0'
ACCESS_TOKEN = 'EAACEdEose0cBAJ2K86ZC1ayVNY2DVdWVu6iqTwQZAdLLdpLZBp21dSMdrGp4IcZBzoqT1X6kBUuWvjDr1hBOLoC4zSuTcrOenryfZA9gowGqudKUOzoqBZBKZCeoCSDS7vMZBWyAaXxAHLPxXJmMG2aUkhE6xFbNeBeD4ZCzV7h0dKOG89j9Y5Kir33edFypHdIYm1qZCi6ZCYqnZAzUcFtzWWSwbmqy0fMPy8MZD'


# 여러 파라미터에 대하여, url을 생성
def fb_generate_url(base = BASE_URL_FB_API, node = '', **param):
    return '%s/%s/?%s' % (base, node, urlencode(param))


# API를 사용할 때 'JTBC 뉴스' 라는 페이지 이름이 아닌, 페이지의 id가 필요하다.
# 여기서 매개변수 pagename은 JTBC 뉴스 페이지 URL( https://www.facebook.com/jtbcnews/?ref=br_rs )에 붙은 것을 의미한다.
def fb_name_to_id(pagename):
    url = fb_generate_url(node = pagename, access_token = ACCESS_TOKEN)
    # print(url)
    json_result = jr.json_request(url)
    # print(json_result)                # {'name': 'JTBC 뉴스', 'id': '240263402699918'}
    return json_result.get('id')


# 게시글 가져오기 - 크롤러는 최종적으로 이 함수를 사용한다.
# 인자로 페이스북 페이지명과 게시글 일자 기간을 넘겨준다.
def fb_fetch_post(pagename, since, until):
    url = fb_generate_url(
        node = fb_name_to_id( pagename ) + '/posts',
        fields = 'id, message, link, name, type, shares, created_time,\
                  reactions.limit(0).summary(true),\
                  comments.limit(0).summary(true)',
        since = since,  # 시작 날짜
        until = until,  # 끝 날짜
        limit = 30,     # 개수
        access_token = ACCESS_TOKEN
    )

    isnext = True
    while isnext is True:
        json_result = jr.json_request(url)

        paging = None if json_result is None else json_result.get('paging')
        url = None if paging is None else paging.get('next')
        isnext = url is not None

        posts = None if json_result is None else json_result.get('data')
        # generator를 사용해서 fb_fetch_post(...) 함수를 for 푸르안에서 사용 가능하도록 수정한다.
        yield posts

for posts in fb_fetch_post('jtbcnews', '2018-05-01', '2018-05-30'):
    print(posts)