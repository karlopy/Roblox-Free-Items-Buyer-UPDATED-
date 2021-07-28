import json,requests,time


cookie = input('Enter your cookie: ')

def scrape(cursor):
    if cursor == None:
        r = requests.get(f'https://catalog.roblox.com/v1/search/items?category=All&creatorTargetId=1&limit=60&maxPrice=0&minPrice=0').json()
    else:
        r = requests.get(f'https://catalog.roblox.com/v1/search/items?category=All&creatorTargetId=1&cursor={cursor}&limit=60&maxPrice=0&minPrice=0').json()
    nextCursor = r['nextPageCursor']
    for data in r['data']:
        try:
            id = data['id']
            if data['itemType'] == 'Asset':
                r = requests.get(f'https://api.roblox.com/Marketplace/ProductInfo?assetId={id}').json()
                save = open('ids.txt','a')
                save.write(f"{r['ProductId']}\n")
                print(f"Scraped: {r['Name']}")
            else:
                r = requests.get(f'https://catalog.roblox.com/v1/bundles/{id}/details').json()
                save = open('ids.txt','a')
                save.write(f"{r['product']['id']}\n")
                print(f"Sraped: {r['name']}")
        except:
            pass
    if nextCursor != None: 
        scrape(nextCursor)

req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
print('')
scrape(None)
print('')
try:
    ids = open("ids.txt", 'r').read().split('\n')
    xcrsftoken = req.headers['X-CSRF-TOKEN'] = req.post("https://economy.roblox.com/v1/developer-exchange/submit").headers['X-CSRF-TOKEN']
    try:
        for id in ids:
            r = req.post(f"https://economy.roblox.com/v1/purchases/products/{id}", data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1} ,headers={"X-CSRF-TOKEN": xcrsftoken})
            if 'TooManyRequests' in r.text:
                print('Rate Limited! Trying again in a minute..')
                time.sleep(60)
                r = req.post(f"https://economy.roblox.com/v1/purchases/products/{id}", data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1} ,headers={"X-CSRF-TOKEN": xcrsftoken})
            else:
                print('Bought item!')
                
    except Exception as er:
        print(er)

except Exception as e:
    print(e)

