
# Getting Maps GPX and KMZ
def get_map_links(response):
    map_gpx = map_kmz = None
    container_maps= response.css("div.uk-child-width-auto")
    map_links = container_maps.css('a')
    for link in map_links:
        if 'GPX' in link.css('::text').get():
            map_gpx = link.css('::attr(href)').get()
            map_gpx = f'https://turismomadrid.es{map_gpx}'
        elif 'KMZ' in link.css('::text').get():
            map_kmz = link.css('::attr(href)').get()
            map_kmz = f'https://turismomadrid.es{map_kmz}'

    return map_gpx, map_kmz

# Getting Links stages
def get_stages_links(response):
    list_stages_links = response.css('a[href*=etapa]')
    hrefs = []
    for link in list_stages_links:
        href = link.css('::attr(href)').get()
        hrefs.append(href)

    return ', '.join(hrefs)