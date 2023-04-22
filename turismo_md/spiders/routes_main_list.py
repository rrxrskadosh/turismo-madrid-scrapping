import scrapy
import mysql.connector
import os
from dotenv import load_dotenv

class RoutesList(scrapy.Spider):
    name = "TurismoMadrid"
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,     
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_dotenv()
            
        self.crawlerDb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        
    def start_requests(self):
        url = "https://turismomadrid.es/es/rutas.html"

        yield scrapy.Request(url=url, callback=self.parse, method='GET', dont_filter=True)

    def parse(self, response):
                                
        data = []
        grid_stack = response.css('a.enlace-ruta')
        for elem in grid_stack:
            url_details_route = elem.css('::attr(href)').get()
            url_details_route = f'https://turismomadrid.es{url_details_route}'

            titles_routes = elem.css("div.descripcion-ruta > h2.uk-margin::text").get()
            titles_routes = titles_routes.replace("\xa0", "")

            description = elem.css("div.descripcion-ruta > p::text").get()

            distance = elem.css("div.uk-width-1-2 p:nth-child(2)::text").get()

            duration = elem.css('div.uk-width-1-2 p:contains("Duración:") + p.dato-ruta::text').get()
            
            db = self.crawlerDb.cursor(dictionary=True)
            query_insert = "INSERT INTO `routes_list` (`titles_routes`,  `url_details_route`, `description`, `distance`, `duration`) VALUES(%s, %s, %s, %s, %s)"
            query_params = (
                titles_routes,
                url_details_route,
                description,
                distance,
                duration
            )
            db.execute(query_insert, query_params)
            self.crawlerDb.commit()

            data.extend([titles_routes, url_details_route, description, distance, duration])
        print(data) 

  


 
            
