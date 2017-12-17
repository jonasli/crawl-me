from baseHandler import *
from ..common.utils import *
from ..third_party.abc import abstractmethod


class PictureUrlThread(threading.Thread):
    def __init__(self, threadName, pageUrl, savePath, handler):
        threading.Thread.__init__(self, name=threadName)
        self.pageUrl = pageUrl
        self.savePath= savePath
        self.handler = handler
        self.pictureUrlList={}

    def run(self):
        syslog("getting page url=%s" % (self.pageUrl), LOG_INFO)
        self.pictureUrlList = self.handler.getPictureUrl(self.pageUrl, copy.copy(self.handler.opener),self.savePath)

    def getPictureUrlList(self):
        return self.pictureUrlList


# abstruct base class
class PageBasedHandler(BaseHandler):
    def getUrlList(self, conf):
        syslog('getUrlList started')
        pageUrlList = self.getPageUrl(copy.copy(self.opener), conf)

        pageNum = len(pageUrlList)
        threadList = list()
        index=0
        for key,value  in pageUrlList.items():
            index=index+1
            th = PictureUrlThread("pictureUrlThread:%s" % (index), key,value, self)
            threadList.append(th)
            th.start()

        pictureUrlList = {}
        for th in threadList:
            th.join()
            #pictureUrlList.update(th.getPictureUrlList())

            pictureUrlList=dict(pictureUrlList,**th.getPictureUrlList())

        return pictureUrlList


    @abstractmethod
    def getPageUrl(self, opener, paraConf):
        pass

    @abstractmethod
    def getPictureUrl(self, pageUrl, opener,savePath):
        pass
