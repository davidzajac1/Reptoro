from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
import time


class Scraper:

    def __init__(self):
        self.help = "This class has 3 scrapers, 'results_page_scraper', 'seller_scraper', 'animal_scraper'"

    def get_html(self, url, sessionid=None, retries=0):

        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': f"sessionid={sessionid}",
            'Referer': 'https://www.morphmarket.com/sw.js',
            'Upgrade-Insecure-Requests': '1',
            'Host':'www.morphmarket.com'
            }

        if sessionid == None: headers.pop('Cookie')

        for r in range(0, retries + 1):
            try:
                req = Request(url, headers=headers)
                html = urlopen(req)
            except Exception as e:
                if r == retries + 1:
                    print(e)
                else:
                    time.sleep(10)

        return BeautifulSoup(html.read(), 'html.parser')

    #Scrapes 1-50 results from a Morphmarket Search Results Page and returns them in a list
    def results_page_scraper(self, sessionid, min_price, max_price, page_num, retries=0):

        url = f"https://www.morphmarket.com/us/search?epoch=2&layout=list&sort=nfs&min_price={min_price}&max_price={max_price}&page={page_num}"

        soup = self.get_html(url, sessionid, retries)

        table = soup.find('tbody')
        rows = table.findAll('tr')

        animals = []
        for row in rows:

            animal = {}

            #Page URL
            url = str(row.get('data-href'))
            animal['url'] = url

            #Status
            status = row.get('class')
            if len(status) < 3:
                status = 'for sale'
            elif 'sold' in status[2]:
                status = 'sold'
            elif 'on-hold' in status[2]:
                status = 'on hold'
            elif 'expired' in status[2]:
                status = 'expired'
            animal['status'] = status

            #Price
            price = row.find('span', {'class': 'actual-price'})

            if price != None: price = price.text.strip()

            if (price == None) or ('nquire' in price) or (price == ''):

                animal['price'] = 0

            else:
                formatted_price = ''
                nums = ['0','1','2','3','4','5','6','7','8','9','.']

                for char in price:
                    if char in nums:
                        formatted_price = formatted_price + char

                formatted_price = round(float(formatted_price),2)

                animal['price'] = formatted_price

            animals.append(animal)

        return animals

    #Scrapes info from a Seller Page on MorphMarket
    def seller_scraper(self, url, scrape_date, retries=0):

        def find_value(text):
            try:
                soup.find('dt', text = text).next_sibling.next_sibling.text.replace("'",'').replace('"','').strip()
                return soup.find('dt', text = text).next_sibling.next_sibling.text.replace("'",'').replace('"','').strip()
            except:
                return None

        soup = self.get_html(url, retries=retries)

        owner = find_value(" Owner")
        location = find_value(" Location")
        website = find_value(" Website")
        facebook = find_value(" Facebook")
        instagram = find_value(" Instagram")
        twitter = find_value(" Twitter")
        phone = find_value(" Phone")
        youtube = find_value(" YouTube")
        email = find_value(" Email")

        #joined
        joined = datetime.strptime(find_value("Joined").split('\n')[0], '%b %d, %Y').strftime("%Y-%m-%d")


        #ratings
        ratings = find_value('\n                    Ratings').replace("(show ratings page)",'').strip()

        #responses
        try:
            responses = find_value('\n                    Responses\n                ').split('\n')
            if len(responses) > 1:
                responses = responses[0] + ' ' + responses[-1].strip()
            elif len(responses) == 1:
                responses = responses[0]
        except:
            responses = None

        #followers
        try:
            followers = int(find_value('\n                    Followers'))
        except:
            followers = 0

        #forum_url
        try:
            forum_url = soup.find('a', text = "Community Profile").get('href')
        except:
            forum_url = None

        #logo
        try:
            logo = soup.find('img', {'class': 'store-logo'}).get('src')
        except:
            logo = None

        #membership
        if soup.find('div', {'class': 'svgbadge xx-small shape5 blue membership-badge'}) != None:
            membership = 'basic'
        elif soup.find('div', {'class': 'svgbadge xx-small shape5 green membership-badge'}) != None:
            membership = 'standard'
        elif soup.find('div', {'class': 'svgbadge xx-small shape5 dark membership-badge'}) != None:
            membership = 'pro'
        elif soup.find('div', {'class': 'svgbadge xx-small shape5 orange membership-badge'}) != None:
            membership = 'premium'
        else:
            membership = 'free'

        #title
        title = soup.find('div', {'class': 'main-content fixed-width wide store-page'}).h3.text

        #delivery methods
        delivery_methods = []
        try:
            delivery = soup.find('dt', text = "Delivery").next_sibling.next_sibling.findAll('div')
            for method in delivery:
                delivery_methods.append(method.text.strip())
        except:
            delivery_methods = []

        #badge list
        badge_list = []
        try:
            badges = soup.find('div', {'class': 'store-details badges'}).findAll('h5')
            for badge in badges:
                badge_list.append(badge.text)
            badge_list = sorted(list(set(badge_list)))
        except:
            badge_list = []

        return {'breeder_url': url, 'title': title, 'owner': owner, 'location': location, 'email': email, 'phone': phone
               ,'website': website, 'facebook': facebook, 'instagram': instagram, 'twitter': twitter
               , 'youtube': youtube, 'forum_url': forum_url, 'joined': joined, 'followers': followers
               , 'membership': membership, 'delivery_methods': delivery_methods, 'logo': logo
               , 'badge_list': badge_list, 'ratings': ratings, 'responses': responses, 'date_scraped': scrape_date}

    #Scrapes all the info off an individual Animal Listing on MorphMarket
    def animal_scaper(self, url, sessionid, scrape_date, retries=0):

        soup = self.get_html(url, sessionid, retries)

        details = soup.find('dl', {'class': 'dl-horizontal'})

        #title
        title = soup.find('span', {'class': 'title'})

        if title != None:
            title = title.text.strip()

        #type
        type_ = soup.find('span', {'class': 'animal-type'})

        if type_ != None:
            type_ = type_.text.strip()

        #traits
        traits = details.find('dt', text = 'Traits: ')

        trait_list = []

        if traits != None:

            traits = traits.next_element.next_element.next_element.findAll('span')

            for trait in traits:
                trait_list.append(trait.text.strip())

            trait_list = list(set(trait_list))

        #quantity
        quantity = soup.find('div', {'class': 'quantity'})

        if quantity != None: quantity = quantity.text.strip().replace('(','').replace(' available)', '')

        #breeder_url
        breeder_url = details.find('dd', {'class': 'store-name-and-logo'}).a.get('href')\
            .split('/')[2]

        #store
        store = details.find('dd', {'class': 'store-name-and-logo'}).a\
            .text.strip().replace('"','').replace("'",'')

        if store == '':
            store = details.find('dd', {'class': 'store-name-and-logo'}).findAll('a')[1]\
                .text.strip().replace('"','').replace("'",'')


        #Description
        description = soup.find('div', {'class': 'desc'})

        if description != None: description = description.text.strip()\
            .replace('Description. ','').replace('"','').replace("'",'')

        #images
        image_list = []
        images = soup.find('div', {'class': 'image d-flex flex-column'})
        images = soup.findAll('div', {'class': 'image-wrapper'})

        for image in images:
            image_list.append(image.img.get('src'))

        #status
        status = soup.find('div', {'class': 'image d-flex flex-column'})

        if status.find('img', {'class': 'sold'}) != None:
            status = 'sold'
        elif status.find('img', {'class': 'on-hold'}) != None:
            status = 'on hold'
        elif status.find('img', {'class': 'expired'}) != None:
            status = 'expired'
        else:
            status = 'for sale'

        #proven_breeder
        proven_breeder = details.find('dt', text = 'Proven:')

        if proven_breeder != None:
            proven_breeder = proven_breeder.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

            if proven_breeder == 'Yes':
                proven_breeder = True
            else:
                proven_breeder = False
        else:
            proven_breeder = False

        #likes
        likes = soup.find('span', {'class': 'badge badge-secondary badge-pill num-likes'}).text
        if likes == '':
            likes = 0
        else:
            likes = int(likes)

        #maturity
        maturity = soup.find('div', {'class': 'maturity'})

        if maturity != None:

            maturity = maturity.text.strip()

            if 'Baby' in maturity:
                maturity = 'B'
            elif 'Subadult' in maturity:
                maturity = 'S'
            elif 'Adult' in maturity:
                maturity = 'A'

        #sex
        sex = details.find('dt', text = ' Sex:')

        try:
            if sex != None: sex = sex.next_element.next_element\
                .next_element.i.get('alt')
        except:
            sex = None

        #birthday
        birthday = details.find('dt', text = ' Birth: ')

        if birthday != None: birthday = birthday.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #weight
        weight = details.find('dt', text = 'Weight:')

        if weight != None: weight = weight.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #shipping
        shipping = details.find('dt', text = 'Shipping:')

        if shipping != None: shipping = shipping.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #trades
        trades = details.find('dt', text = 'Trades:')

        if trades != None:
            trades = trades.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #first_posted
        first_posted = details.find('dt', text = 'First Posted:')

        if first_posted != None:
            first_posted = first_posted.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

            first_posted = datetime.strptime(first_posted, '%m/%d/%y').strftime("%Y-%m-%d")

        #last_renewed
        last_renewed = details.find('dt', text = 'Last Renewed:')

        if last_renewed != None:
            last_renewed = last_renewed.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

            last_renewed = datetime.strptime(last_renewed, '%m/%d/%y').strftime("%Y-%m-%d")

        #last_updated
        last_updated = details.find('dt', text = 'Last Updated:')

        if last_updated != None:
            last_updated = last_updated.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

            last_updated = datetime.strptime(last_updated, '%m/%d/%y').strftime("%Y-%m-%d")

        #id_num
        id_num = details.find('dt', text = 'ID#:')

        if id_num != None: id_num = id_num.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #clutch
        clutch = details.find('dt', text = 'Clutch:')

        if clutch != None: clutch = clutch.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #diet
        diet = details.find('dt', text = 'Diet:')

        if diet != None: diet = diet.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #currency and price
        amount = details.find('dt', text = ' Price:')

        if amount != None: amount = amount.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        if (amount == None) or ('nquire' in amount) or (amount == ''):

            currency = 'Inquire'
            price = None

        else:
            currency = ''
            price = ''
            nums = ['0','1','2','3','4','5','6','7','8','9','.']

            for char in amount:
                if char not in nums:
                    currency = currency + char
                else:
                    price = price + char

            price = round(float(price),2)
            currency = currency.replace('US','').replace(',','')

        #offers
        offers = details.find('dt', text = 'Offers:')

        if offers != None: offers = offers.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        #origin
        origin = details.find('dt', text = 'Origin:')

        if origin != None: origin = origin.next_element\
            .next_element.next_element.text.strip().replace('"','').replace("'",'')

        animal = {'url': url.replace('https://www.morphmarket.com', ''), 'breeder_url': breeder_url, 'date_scraped': scrape_date
        , 'description': description, 'images': image_list, 'status': status, 'proven_breeder': proven_breeder, 'birthday': birthday
        , 'likes': likes, 'shipping': shipping, 'trades': trades, 'first_posted':first_posted, 'last_renewed': last_renewed, 'last_updated': last_updated, 'id_num': id_num, 'clutch': clutch
        , 'diet': diet, 'offers': offers, 'origin': origin, 'sex': sex, 'maturity': maturity, 'title': title, 'type': type_
        , 'weight': weight, 'currency': currency, 'price': price, 'store': store, 'quantity': quantity, 'traits': trait_list}

        return animal
