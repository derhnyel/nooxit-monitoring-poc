FROM victoriametrics/victoria-metrics:latest
COPY prom-scrape-conf.yaml /etc/victoria-metrics-scraper-config.yaml
ENTRYPOINT ["/victoria-metrics-prod","--httpListenAddr=:8428","--storageDataPath=/var/victoria-metrics","--retentionPeriod=30d","--promscrape.config=/etc/victoria-metrics-scraper-config.yaml","--promscrape.config.strictParse=false","--promscrape.suppressScrapeErrors=true"]
