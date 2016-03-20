from abc import abstractmethod, ABCMeta


class BaseLinkMaker(metaclass=ABCMeta):
    @abstractmethod
    def get_links(self, contest_description):
        pass

    def get_additional_links(self, contest_description):
        pass
