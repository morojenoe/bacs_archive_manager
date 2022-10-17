import logging
import pathlib
import tarfile
import zipfile


class ArchiveExtractor:
    def extract(self, path_to_file, path_to_extraction_dir):
        path_to_file = str(path_to_file)
        path_to_extraction_dir = str(path_to_extraction_dir)
        if tarfile.is_tarfile(path_to_file):
            self._extract_tar(path_to_file, path_to_extraction_dir)
        else:
            self._extract_zip(path_to_file, path_to_extraction_dir)

    @staticmethod
    def is_archive(path_to_file):
        path_to_file = str(path_to_file)
        return (tarfile.is_tarfile(path_to_file)) or (
            zipfile.is_zipfile(path_to_file))

    @staticmethod
    def _extract_tar(path_to_file, path_to_extraction_dir):
        try:
            with tarfile.open(path_to_file) as tar_file:
                
                import os
                
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar_file, path_to_extraction_dir)
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
