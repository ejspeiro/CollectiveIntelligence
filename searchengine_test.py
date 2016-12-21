import searchengine

if __name__ == "__main__":
    pages = ['https://en.wikipedia.org/wiki/Finite_difference']

    crawler = searchengine.crawler('searchengine.db')
    crawler.createindextables()
    crawler.crawl(pages)
    print "Added %d pages" % (crawler.totallinks())
