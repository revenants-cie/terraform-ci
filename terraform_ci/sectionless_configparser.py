"""
Module for SectionLessConfigParser - a config parser for ini files
without section.
"""
from configparser import RawConfigParser


class SectionLessConfigParser(RawConfigParser):  # pylint: disable=too-many-ancestors
    """
    Class reads ini file without sections.
    """

    def read(self, filenames, encoding=None):
        with open(filenames) as fdesc:
            file_content = "[dummy_section]\n" + fdesc.read()

        self.read_string(file_content)

    def get(self, *args, **kwargs):  # pylint: disable=arguments-differ
        super_args = ("dummy_section",) + args
        return super().get(*super_args, **kwargs).strip("\"'")
