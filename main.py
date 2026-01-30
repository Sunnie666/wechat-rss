import feedgen.feed
import requests
from config import WECHAT_BIZ_LIST
from datetime import datetime


def get_wechat_articles(biz):
    """抓取公众号最新文章"""
    url = f"https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={biz}&f=json&offset=0&count=10"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        # 解析微信返回的内容（简化版，只取标题、链接、时间）
        data = resp.json()
        articles = []
        for msg in data.get("general_msg_list", {}).get("list", []):
            if "app_msg_ext_info" in msg:
                info = msg["app_msg_ext_info"]
                articles.append({
                    "title": info["title"],
                    "link": info["content_url"],
                    "pub_date": datetime.fromtimestamp(info["update_time"])
                })
        return articles
    except Exception as e:
        print(f"抓取失败: {e}")
        return []


def generate_rss():
    """生成RSS文件"""
    fg = feedgen.feed.FeedGenerator()
    fg.title("我的微信公众号RSS")
    # 已替换为你的GitHub用户名 Sunnie666
    fg.link(href="https://github.com/Sunnie666/wechat-rss", rel="self")
    fg.description("自动抓取的微信公众号文章")

    # 遍历所有公众号抓取文章
    for name, biz in WECHAT_BIZ_LIST:
        articles = get_wechat_articles(biz)
        for art in articles:
            fe = fg.add_entry()
            fe.title(f"[{name}] {art['title']}")
            fe.link(href=art["link"])
            fe.pubDate(art["pub_date"])

    # 保存为feed.xml
    fg.rss_file("feed.xml", pretty=True)


if __name__ == "__main__":
    generate_rss()
  
