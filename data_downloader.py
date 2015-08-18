import urllib.error
import urllib.request
import urllib.parse
import shutil
import path
import logging


class BaseDownloader:
    def download_data(self, path_to_problem_dir, links):
        path_to_problem_dir = path.Path(path_to_problem_dir)
        path_to_problem_dir.makedirs_p()
        for link in links:
            file_name = self.get_file_name_from_link(link)
            path_to_file = path_to_problem_dir.joinpath(file_name)
            try:
                with urllib.request.urlopen(link) as response, \
                        open(path_to_file, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            except urllib.error.URLError as error:
                logging.error('Cannot download a link: {0}'.format(link))
                logging.exception(error)
            except IOError as error:
                logging.error('Cannot open a file: {0}'.format(path_to_file))
                logging.exception(error)

    @staticmethod
    def get_file_name_from_link(link):
        link = urllib.parse.urlparse(link).path
        return path.Path(link).name

    def download_additional_data(self, path_to_problem_dir):
        pass
