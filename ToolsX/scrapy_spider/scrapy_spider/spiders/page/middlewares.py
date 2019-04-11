import os
import re

from scrapy_spider.spiders.page import page_utils


class PageMiddleware(object):
    def process_response(self, request, response, spider):
        return response.replace(body=self.process_response_text(response))

    def process_response_text(self, response):
        """处理文本"""
        url = response.url
        text = response.text

        text = self.replace_to_real_link(url, text)
        text = self.replace_to_relative_link(url, text)
        return text

    @staticmethod
    def replace_to_real_link(url: str, text: str) -> str:
        """处理为实际链接
        ../ 替换为实际链接
        // 拼接上 scheme

        >>> PageMiddleware().replace_to_real_link('https://a/b/c','src="../../d/e"')
        'src="https://a/d/e"'
        """

        def _replace_relative_link(match):
            """相对链接替换为实际链接"""
            path = match.group(1)
            path = os.path.normpath(os.path.join(url, path))
            path = path.replace('\\', '/')
            path = path.replace(':/', '://')
            return path

        # 替换相对链接
        text = re.sub(r'(?<=")(\.{2}.*)(?=")', _replace_relative_link, text)
        # 加上 scheme
        scheme = url[:url.find(':')]
        text = re.sub(r'(?<=")(//.*)(?=")', f'{scheme}:\\1', text)
        return text

    @staticmethod
    def replace_to_relative_link(url, text):
        """同一文件替换为相对链接

        如果以后要处理，可以将已下载的文都替换为相对链接
        """
        url = page_utils.add_file_extension(url)
        return text.replace(url + '#', '#')


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
