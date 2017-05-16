from lxml import html
import requests

url = 'http://www.kcfortunecookiefactory.com/fortunes'

tree_from_url = lambda url, params=None : html.fromstring(requests.get(url, params).content)
fetch_fortunes = lambda page_number : tree_from_url(url, {'page': page_number})
    .xpath('//div[@class=\"item-list\"]/ul/li/span/text()')

fortunes = []

count = int(tree_from_url(url)
    .xpath('//div[@class=\"item-list"]/ul[@class=\"pager\"]/li[@class=\"pager-current\"]/text()')[0].split(' ')[2])



for i in range(count):
    results = fetch_fortunes(i)
    for result in results:
        fortunes.append(result)
        print(result)


fortune_file = open('fortunes.txt', 'w')
for fortune in fortunes:
    fortune_file.write(fortune + '\n')
fortune_file.close()
