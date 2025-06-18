import requests
from parsel import Selector


def extract_repo(html):
    """提取仓库信息"""
    selector = Selector(text=html)
    repos = selector.xpath('//h2/a/text()').getall()
    return [repo.strip() for repo in repos]


def main(context):
    url = 'https://github.com/trending'
    headers = {'User-Agent': 'Mozilla/5.0'}
    context.log(f'[Trending] 开始抓取数据，目标地址: {url}')
    try:
        ret_html = requests.get(url, headers=headers, timeout=10)
        ret_html.raise_for_status()
    except requests.RequestException as e:
        context.log(f'[Trending] 请求失败: {e}')
        return context.res.error('无法获取GitHub Trending页面')
    context.log(f'[Trending] 获取HTML成功，长度: {len(ret_html.text)}')
    repos = extract_repo(ret_html.text)
    context.log(f'[Trending] 提取仓库成功，数量: {len(repos)}')

    return context.res.success(data=repos)
