from abc import ABCMeta, abstractproperty
import path
import archive_extractor


class BaseContestManager(metaclass=ABCMeta):
    def __init__(self, link_maker, problems_extractor, downloader,
                 package_manager, path_to_directory):
        self.link_maker = link_maker
        self.problems_extractor = problems_extractor
        self.downloader = downloader
        self.package_manager = package_manager
        self.path_to_directory = path_to_directory

    def download_contest(self, contest_description):
        tmp_directory = path.Path(self.path_to_directory).joinpath('TEMP')
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
        tmp_directory = path.Path(tmp_directory)
        for file in tmp_directory.files():
            if extractor.is_archive(file):
                arch_dir = tmp_directory.joinpath(file.name.splitext()[0])
                arch_dir.makedirs_p()
                extractor.extract(file, arch_dir)

    @abstractproperty
    def short_name(self):
        pass

    @abstractproperty
    def long_name(self):
        pass

    @abstractproperty
    def main_link(self):
        pass
