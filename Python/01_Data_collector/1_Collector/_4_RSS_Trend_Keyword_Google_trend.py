# pip install feedparser

import datetime
import sys
import os
import feedparser

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_trend(national):
    feed = feedparser.parse('https://trends.google.com/trending/rss?geo=' + national)
    indexs = ['title', 'ht_approx_traffic', 'ht_news_item_title', 'published']
    head_message = f'[Google Trend - {national}]\n'

    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today_day_of_week = today.strftime("%a")
    today_day = today.strftime("%d")
    yesterday_day_of_week = yesterday.strftime("%a")
    yesterday_day = yesterday.strftime("%d")
    message = ''

    for item in feed.entries:
        try:
            for index in indexs:
                print(f'{index}: {getattr(item, index)}')
        except:
            continue
        tmp = str(item.published).replace(",", "")
        tmp_time = tmp.split(" ")

        if (len(item.ht_approx_traffic) > 6) and ((today_day_of_week == tmp_time[0] and today_day == tmp_time[1]) or (
                yesterday_day_of_week == tmp_time[0] and yesterday_day == tmp_time[1])):
            message += f"  {item.title} ({item.ht_approx_traffic}) - {str(item.ht_news_item_title).replace('&#39;', '').replace('&quot;', '')}\n"
        else:
            continue
    return str(head_message + message)


if __name__ == "__main__":
    #print("Google Trend plugin Create!")
    nationals = ['KR', 'US', 'GB', 'JP', 'HK', 'IN', 'TW']

    for national in nationals:
        print(f"Google Trend {national} data get")
        print(get_trend(national))
