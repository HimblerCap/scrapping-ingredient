import scrapy

class SpiderIngredient(scrapy.Spider):
    name = 'ingredient'
    start_urls = [
        'https://www.comeperuano.pe'
    ]
    custom_settings = {
        'FEED_URI': 'ingredient.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response): 
        links_dishes = response.xpath('//*/div/div/div/h3/a/@href').getall()
        for link in links_dishes:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})
    
    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        Principalingredients = response.xpath('//*/div/div/ul[1]/li/text()').getall()
        otherIngredients = response.xpath('//*/div/div/ul[1]/li[@style="font-weight: 400;"]/span/text()').getall()
        ingredients = []
        picture = response.xpath('//*/div/header/div[1]/img/@data-src').getall()
        
        for i in range(len(Principalingredients)):
            if(Principalingredients[i] == ''):
                ingredients.append(otherIngredients[i])
            else:
                ingredients.append(Principalingredients[i])

        yield {
            'Plato':  link[27:-1].replace('-', ' ').replace('receta', '').strip().capitalize().replace('De', '').strip(),
            'Ingrediente' : [ingredient.strip() for ingredient in ingredients ],
            'Imagen': picture,
        }
    