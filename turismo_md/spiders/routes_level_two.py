import scrapy
import mysql.connector
import os
from dotenv import load_dotenv
from utils import get_map_links, get_stages_links

class RouteStage(scrapy.Spider):
    name = "TurismoMadrid2"
    
    custom_settings = {
        'DOWNLOAD_DELAY': 4, 
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
        url = 'https://turismomadrid.es/es/rutas/nivel2/3.html?etapa=1'

        yield scrapy.Request(url=url, callback=self.parse,  method='GET', dont_filter=True)

    def parse(self, response):
        data = []
        
        title_stage = response.css('h1.nivel2-titulo::text').get()

        image_stage_url = response.css('div.uk-panel.uk-flex.uk-flex-middle.uk-flex-center::attr(style)').re_first(r"url\('(.*)'\)")

        stage_description = response.css("div.descripcion-etapa p::text").get()

        # Maps GPX & KMZ
        map_gpx, map_kmz = get_map_links(response)
        
        # Stages
        stages_links = get_stages_links(response)
        
        db = self.crawlerDb.cursor(dictionary=True)
        query_insert = "INSERT IGNORE INTO `route_stages` (`title_stage`, `image_stage_url`, `stage_description`, `map_gpx`, `map_kmz`,`stages_links`) VALUES(%s, %s, %s, %s, %s, %s)"
        query_params = (
            title_stage,
            image_stage_url,
            stage_description,
            map_gpx,
            map_kmz,
            stages_links
        )
        db.execute(query_insert, query_params)
        self.crawlerDb.commit()
        data.extend([title_stage, image_stage_url, stage_description, map_gpx, map_kmz, stages_links])
        print(data)