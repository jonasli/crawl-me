from pyquery import PyQuery as pq

from pageBasedHandler import *
from ..common.utils import *


class FfftHandler(PageBasedHandler):

    def getPageUrl(self, opener, paraConf):
        syslog('getPageUrl started')
        urlList = list()
        secondLevelUrlList = {}

        for page in range(paraConf["beginPage"], paraConf["endPage"] + 1):
            if page == 1:
                crawlUrl = paraConf["url"]
            else:
                crawlUrl = paraConf["url"][0: paraConf["url"].index('.html')] + "/" + str(page) + ".html"
            urlList.append(crawlUrl)

        for i in range(0,len(urlList)):

            htmlContent = urlReadWithRetry(self.opener, urlList[i])
            if htmlContent == None:
                syslog("parse 1st level url fail at url=" + urlList[i], LOG_ERROR)
            q = pq(htmlContent)

            divs = q('.img')
            for i in range(0, divs.size()):
                title = divs.eq(i).find('a').attr('title')
                url = divs.eq(i).find('a').attr('href')
                if url== None:
                    continue

                syslog(title)
                syslog(url)
                secondLevelUrlList[url] = title

                for p in range(paraConf["beginPage"]+1, paraConf["endPage"]+1):
                    try:
                        pageUrl = url[0: url.index('.html')] + "_" + str(p) + ".html"
                        secondLevelUrlList[pageUrl]=title
                    except:
                        print('Error happened for url :' + url)


        #syslog(secondLevelUrlList.items)
        assert (len(secondLevelUrlList) > 0)
        return secondLevelUrlList
    #
    # # def getPageUrl(self, baseUrl, opener, beginPage, endPage):
    # def getPageUrlBackup(self, opener, paraConf):
    #     urlList = list()
    #     for page in range(paraConf["beginPage"], paraConf["endPage"] + 1):
    #         if page == 1:
    #             crawlUrl = paraConf["url"]
    #         else:
    #             crawlUrl = paraConf["url"][0: paraConf["url"].index('.html')] + "_" + str(page) + ".html"
    #         urlList.append(crawlUrl)
    #     return urlList

    def getPictureUrl(self, pageUrl, opener, savePath):
        urlList = {}
        htmlContent = urlReadWithRetry(opener, pageUrl)
        if htmlContent == None:
            syslog("FfftPicIterator init fail at url=" + pageUrl, LOG_ERROR)
        q = pq(htmlContent)
        imgP = q('p')
        
        for i in range(0, imgP.size()):
            syslog("p.id: %s" % imgP.eq(i).attr('id'))
            if (imgP.eq(i).attr('id')=='contents'):
       
                syslog('find a')
                links=imgP.eq(i).find('a')
                syslog("how many links: %s" % (links.size()))
                for j in range(0,links.size()):
                    try:
                        #check if the sub element has a href attribute
                        image=links.eq(j).find('img')
                        href = image.attr('src')
                        alt=image.attr('alt')
                        syslog(alt)
                        if (href == None):
                            continue


                        #check postfix 
                        imgUrl = href#.split('?')[1]
                        urlList[imgUrl]=savePath
                        syslog("imgurl find, url=%s" % (imgUrl))
                        #syslog(alt)
                    except Exception, e:
                        syslog("Exception:" + str(Exception) + ", " + str(e), LOG_ERROR)
                        continue

        return urlList

    def initOpener(self, conf):
        self.opener = urllib2.build_opener()
        return self.opener

    def initPara(self, parser):
        parser.add_argument('url', help='your url to crawl')
        parser.add_argument('savePath', help='the path where the imgs ars saved')
        parser.add_argument('beginPage', help='the page where we start crawling', type=int)
        parser.add_argument('endPage', help='the page where we end crawling', type=int)
        args = parser.parse_args()
        return {
            "url": args.url,
            "savePath": args.savePath,
            "beginPage": args.beginPage,
            "endPage": args.endPage
        }





         
