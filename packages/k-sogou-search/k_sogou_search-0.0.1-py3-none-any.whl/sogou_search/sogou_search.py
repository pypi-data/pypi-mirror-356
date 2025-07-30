import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import random
import math

def get_random_user_agent():
    platforms = [
        "(Windows NT 10.0; Win64; x64)",
        "(Macintosh; Intel Mac OS X 10_15_7)",
        "(X11; Linux x86_64)",
    ]
    platform = random.choice(platforms)
    # 随机生成 Chrome 浏览器版本号
    random_version = random.randint(100, 120)
    return f"Mozilla/5.0 {platform} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random_version}.0.0.0 Safari/537.36"


def sogou_search(query: str, num_results: int = 10, delay: float = 1) -> List[Dict[str, str]]:
    """
    逆向实现搜狗搜索API，返回包含title、url、description的list。
    :param query: 搜索关键词
    :param num_results: 需要返回的结果数量
    :param delay: 请求之间的延迟（秒）
    :return: List[{'title': ..., 'url': ..., 'description': ...}]
    """
    all_results = []
    page = 1
    while len(all_results) < num_results:
        headers = {
            'User-Agent': get_random_user_agent(),
        }
        params = {
            'query': query,
            'page': page,
        }
        url = 'https://www.sogou.com/web'
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            break

        soup = BeautifulSoup(resp.text, 'html.parser')
        
        found_results_on_page = 0
        for item in soup.select('div.vrwrap, div.rb'):  # 搜狗搜索结果的常见容器
            title_tag = item.select_one('h3 a')
            desc_tag = item.select_one('div.str-text-info, div.ft, div.abstract, div.attribute-centent, div.fz-mid.space-txt, p.txt-info, p.star-wiki, a.star-wiki, div[class*="img-text"]')
            if title_tag:
                title = title_tag.get_text(strip=True)
                url = title_tag.get('href')
                description = desc_tag.get_text(strip=True) if desc_tag else ''
                all_results.append({
                    'title': title,
                    'url': url,
                    'description': description
                })
                found_results_on_page += 1

        if found_results_on_page == 0:
            break

        if len(all_results) < num_results:
            sleep_time = random.uniform(delay, delay + 1.0)
            time.sleep(sleep_time)
            page += 1
        
    return all_results[:num_results]

if __name__ == '__main__':
    # 示例用法
    data = sogou_search('人工智能', num_results=15, delay=1)
    print(f"成功获取 {len(data)} 条结果:")
    for i, d in enumerate(data, 1):
        print(f"--- 结果 {i} ---")
        print(d)
