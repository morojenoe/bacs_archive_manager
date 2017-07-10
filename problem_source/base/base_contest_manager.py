from abc import ABCMeta, abstractmethod

import pathlib

from tools import archive_extractor


class BaseContestManager(metaclass=ABCMeta):
    def __init__(self, link_maker, problems_extractor, downloader,
                 package_manager, path_to_directory):
        self.link_maker = link_maker
        self.problems_extractor = problems_extractor
        self.downloader = downloader
        self.package_manager = package_manager
        self.path_to_directory = path_to_directory

    def download_contest(self, contest_description):
        tmp_directory = pathlib.Path(self.path_to_directory).joinpath('TEMP')
        links = self.link_maker.get_links(contest_description)
        self.downloader.download_data(tmp_directory, links)
        links = self.link_maker.get_additional_links(contest_description)
        self.downloader.download_additional_data(tmp_directory, links,
                                                 contest_description)
        self.extract_archives(tmp_directory)
        problems = self.problems_extractor.extract(tmp_directory,
                                                   contest_description)
        self.package_manager.build_packages(problems, self.path_to_directory)

    @staticmethod
    def extract_archives(tmp_directory):
        extractor = archive_extractor.ArchiveExtractor()
        tmp_directory = pathlib.Path(tmp_directory)
        for file in tmp_directory.iterdir():
            if file.is_file() and extractor.is_archive(file):
                arch_dir = tmp_directory.joinpath(file.stem)
                arch_dir.mkdir(exist_ok=True)
                extractor.extract(file, arch_dir)

    @property
    @abstractmethod
    def short_name(self):
        pass

    @property
    @abstractmethod
    def long_name(self):
        pass

    @property
    @abstractmethod
    def main_link(self):
        pass
