#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from scrapy import cmdline

# command = "scrapy crawl csdn -a search=python"
# os.system(command)

cmdline.execute('scrapy crawl csdn -a search=python+分布式'.split())