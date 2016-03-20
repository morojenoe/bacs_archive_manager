import urllib.request

import lxml.html
import path
from lxml.html.builder import HTML, BODY, PRE

from problem_source.base import data_downloader


class UsacoDownloader(data_downloader.BaseDownloader):
    def download_additional_data(self, dir_path, links, contest_description):
        for link in links:
            page = urllib.request.urlopen(link[0]).read()
            page = str(page, encoding='utf-8')
            page = page.replace(' <= ', ' &lt;= ')
            page = page.replace(' < ', ' &lt; ')
            page = lxml.html.fromstring(page)
            file_name = self.get_file_name_from_link(link[1])
            file_name = path.Path(file_name).splitext()[0] + ".html"
            statement = page.xpath("//div[@class='problem-text']")[0]

            year = contest_description["year"]
            month = contest_description["month"]
            if (year < 2015) or (year == 2015 and month == "jan"):
                statement = HTML(BODY(PRE(statement)))
            else:
                statement = HTML(BODY(statement))

            with open(dir_path.joinpath(file_name), 'w') as statement_file:
                statement_file.write(
                    str(lxml.html.etree.tostring(statement), encoding='utf-8'))
