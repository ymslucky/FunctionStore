import os

import requests
from appwrite.id import ID
from parsel import Selector

from appwrite.client import Client
from appwrite.services.databases import Databases

client = Client()
(client
 .set_endpoint(os.environ['ENDPOINT'])
 .set_project(os.environ['PROJECT_ID'])
 .set_key(os.environ['API_KEY'])
 )
databases = Databases(client)


def extract_repo(html):
    """提取仓库信息"""
    selector = Selector(text=html)
    repos = selector.xpath('//article').getall()
    rows = []
    for i in range(len(repos)):
        href = selector.xpath(f'//article[{i + 1}]/h2/a/@href').get().strip()
        rows.append({
            'name': href,
            'language': selector.xpath(f'//article[{i + 1}]/div[2]/span[1]/span[2]/text()').get().strip(),
            'star': int(selector.xpath(f'//article[{i + 1}]/div[2]/a[1]/text()').get().strip().replace(",", "")),
            'description': selector.xpath(f'//article[{i + 1}]/p/text()').get().strip(),
            'link': f'https://github.com{selector.xpath(f'//article[{i + 1}]/h2/a/@href').get().strip()}'
        })
    return rows


def save_to_appwrite(repos, context):
    """保存数据至Appwrite"""
    for row in repos:
        result = databases.create_document(os.environ['DATABASE_ID'], os.environ['COLLECTION_ID'], ID.unique(), row)
        context.log(f'[Trending] 保存数据成功: {result}')


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

    # 向Appwrite数据库写入 数据
    save_to_appwrite(repos, context)

    return context.res.success(data=repos)
