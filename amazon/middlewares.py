from selenium import webdriver
from scrapy.http import HtmlResponse

from selenium.webdriver.chrome.options import Options

class Amazon_selenium_middleware(object):
    def __init__(self):
        # 有界面
        # self.driver = webdriver.Chrome()
        # 无界面
        option = Options()
        option.set_headless()
        self.driver = webdriver.Chrome(options=option)

    def process_request(self,spider,request):
        # 首页提取分类url才使用selenium
        if 'cn' in request.url[-2:]:
            #等待页面加载完成
            self.driver.implicitly_wait(5)
            self.driver.get(request.url)

            html = self.driver.page_source
            return HtmlResponse(url=self.driver.current_url,
                                body=html.encode("utf-8"),
                                encoding='utf-8',
                                request=request)

    def __del__(self):
        self.driver.quit()
