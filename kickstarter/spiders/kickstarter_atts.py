import scrapy, json, re
import pandas as pd


class KickstarterSpider(scrapy.Spider):
    name = "kickstarter_atts"

    def start_requests(self):

        urls = []
        whole_atts = pd.read_csv("Kickstarter_2016-01-28T09_15_08_781Z/Kickstarter031.csv")
        camp_len = whole_atts.shape[0]
        print(camp_len)
        for i in range(int(camp_len)):
            json_urls = json.loads(whole_atts['urls'][i])
            urls.append(json_urls["web"]['rewards'])
        
        for url in urls:
            yield scrapy.Request(url=url, meta= {'whole_atts': whole_atts}, callback=self.parse)

    def parse(self, response):
        whole_atts = response.meta['whole_atts']
        camp_id = whole_atts['id']
        camp_name = whole_atts['name']
        blurb = whole_atts['blurb']
        goal = whole_atts['goal']
        pledged = whole_atts['pledged']
        status = whole_atts['state']
        slug = whole_atts['slug']
        disable_communication = whole_atts['disable_communication']
        country = whole_atts['country']
        currency = whole_atts['currency']
        deadline = 
        rewards = len(response.css("ol li").extract())
        try:
           FAQ = int(response.xpath("//div[@class='project-nav__links']/a[3]/span/text()").extract()[0])
        except IndexError:
           FAQ = 0
        try:
           updates = int(response.xpath("//div[@class='project-nav__links']/a[4]/span/text()").extract()[0])
        except IndexError:
           updates = "Not Found"
        try:
           comments = response.xpath("//div[@class='project-nav__links']/a[5]/span/data/text()").extract()[0]
           com = re.search(r",", comments, re.M|re.I)
           if com:
               comments = comments.replace(",", "")
        except IndexError:
           comments = "Not Found"
          
        try:
           video_url = response.xpath("//video/source/@src").extract()[0]
        except IndexError:
           video_url = "No Video"
        with open("Kickstarter031.csv", "a") as kick:
           kick.write(str(camp_id)+ ";" + str(camp_name) + ";" +str(rewards) + ";" + str(FAQ) + ";" + str(comments) + ";" + str(updates) + ";" + str(video_url) + "\n")