import base_link_maker
import lxml.html


class UsacoLinkMaker(base_link_maker.BaseLinkMaker):
    def get_links(self, contest_description):
        for links in self._extract_links(contest_description):
            yield links[1]

    def _extract_links(self, contest_description):
        links = self._get_links_to_problem_data(contest_description["year"],
                                                contest_description["month"],
                                                contest_description["lang"])
        if contest_description["division"] is not None:
            for link in links[contest_description["division"]]:
                yield link
        else:
            for div, links in links.items():
                for link in links:
                    yield link

    @staticmethod
    def _get_links_to_problem_data(year, month, lang):
        year %= 100
        result = {"gold": [], "silver": [], "bronze": []}
        base_url = "http://usaco.org/"
        url = (base_url + "index.php?page={}{}problems").format(month, year)
        page = lxml.html.parse(url)
        if len(page.xpath(".//div[@class='panel historypanel']")) == 0:
            page = lxml.html.parse(url.replace("problems", "results"))

        division = ["gold", "silver", "bronze"]
        current_division = -1

        for node in page.xpath(".//div[@class='panel historypanel']"):
            number = int(node.xpath("div[1]/h1[1]")[0].text_content())
            if number == 1:
                current_division += 1
            link2text = base_url + node.xpath("div[2]/a[1]")[0].get("href")
            link2text += "&lang={}".format(lang)
            link2data = base_url + node.xpath("div[2]/a[2]")[0].get("href")
            result[division[current_division]].append((link2text, link2data))
        return result

    def get_additional_links(self, contest_description):
        return self._extract_links(contest_description)
