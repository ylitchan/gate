import scrapy
import json
import os
from scrapy import Request

bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAAPEGjQEAAAAAkECGXEPb5OdKDxAvKPfKMpvapK8%3D75XuXphqMTjfL80Efbruq0T56U2wEkyKDH3EaSK8HAIIET3GMd")
# headers = {
#         'user-agent': (
#             f"Python/{python_version()} "
#             f"Requests/{requests.__version__} "
#             f"Tweepy/{tweepy.__version__}"
#         ),
#         'authorization': f"Bearer {bearer_token}"}
class AlphaSpider(scrapy.Spider):
    name = 'alpha'
    allowed_domains = ['api.twitter.com']
    # with open('alpha.json', 'r+') as alpha:
    #     alpha = json.load(alpha)
    start_urls = ["https://api.twitter.com/2/users/{}/following".format(user_id) for user_id in [4920186276]]
    self._make_request(
        "GET", f"/2/users/{id}/following", params=params,
        endpoint_parameters=(
            "expansions", "max_results", "pagination_token",
            "tweet.fields", "user.fields"
        ), data_type=User, user_auth=user_auth
    )
    def start_requests(self):
        for url in self.start_urls:
            yield Request("https://api.twitter.com/2/users/{}/following", dont_filter=True,callback=self.parse, headers=headers,meta={'proxy': 'http://127.0.0.1:10810'})


    def parse(self, response):
        print(response.text)
