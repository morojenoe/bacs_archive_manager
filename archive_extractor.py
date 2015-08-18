import logging
import path
import tarfile
import zipfile


class ArchiveExtractor:
    def extract(self, path_to_file, path_to_extraction_dir):
        path_to_file = path.Path(path_to_file)
        if tarfile.is_tarfile(path_to_file):
            self._extract_tar(path_to_file, path_to_extraction_dir)
        else:
            self._extract_zip(path_to_file, path_to_extraction_dir)

    @staticmethod
    def is_archive(path_to_file):
        return (tarfile.is_tarfile(path_to_file)) or (
            zipfile.is_zipfile(path_to_file))

    @staticmethod
    def _extract_tar(path_to_file, path_to_extraction_dir):
        try:
            with tarfile.open(path_to_file) as tar_file:
                tar_file.extractall(path_to_extraction_dir)
        except tarfile.TarError as error:
            logging.error('Cannot extract files from an archive ({0})'.format(
                path_to_file))
            logging.exception(error)

    @staticmethod
    def _extract_zip(path_to_file, path_to_extraction_dir):
        try:
            with zipfile.ZipFile(path_to_file) as zip_file:
                zip_file.extractall(path_to_extraction_dir)
        except tarfile.TarError as error:
            logging.error('Cannot extract files from an archive ({0})'.format(
                path_to_file))
            logging.exception(error)
