import scrapy
import mysql.connector
import os
from dotenv import load_dotenv
from utils import get_map_links, get_stages_links

class RouteDetails(scrapy.Spider):
    name = "TurismoMadrid1"
    
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
        url = "https://turismomadrid.es/es/rutas/nivel1/2.html"

        yield scrapy.Request(url=url, callback=self.parse, method='GET', dont_filter=True)

    def parse(self, response):
        data = []

        image_detail_url = response.css('div.uk-panel.uk-flex.uk-flex-middle.uk-flex-center::attr(style)').re_first(r"url\('(.*)'\)")

        short_description = response.css("div.descripcion-etapa p::text").get()

        # Maps GPX & KMZ
        map_gpx, map_kmz = get_map_links(response)
        
        # Stages
        stages_links = get_stages_links(response)

        db = self.crawlerDb.cursor(dictionary=True)
        query_insert = "INSERT IGNORE INTO `route_details` (`image_detail_url`, `short_description`, `map_gpx`, `map_kmz`,`stages_links`) VALUES(%s, %s, %s, %s, %s)"
        query_params = (
            image_detail_url,
            short_description,
            map_gpx,
            map_kmz,
            stages_links
        )
        db.execute(query_insert, query_params)
        self.crawlerDb.commit()
        data.extend([image_detail_url, short_description, map_gpx, map_kmz, stages_links])
        print(data)
            
           
            