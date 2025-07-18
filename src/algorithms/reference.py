"""Module reference.py"""
import logging

import pandas as pd


class Reference:
    """
    Returns a data frame that includes the fine named entity
    recognition (NER) codes and their names.
    """

    def __init__(self, id2label: dict):
        """

        :param id2label: A dictionary of named entity recognition (NER) labels and their codes
        """

        self.__id2label = id2label

    def __get_frame(self) -> pd.DataFrame:
        """

        :return:
        """

        frame = pd.DataFrame.from_dict(self.__id2label, orient='index')
        frame.reset_index(drop=False, inplace=True)
        frame.rename(columns={'index': 'code', 0: 'name'}, inplace=True)

        return frame

    def __call__(self) -> pd.DataFrame:
        """

        :return: A data frame that has the fields<br>
            code: Identification code.
            name: name = `parent` + `-` + `branch`
            parent: cf. coarse entity.  Equivalent.
            branch: The children of a coarse entity.
        """

        # Get the data frame of Fine NER Tags, i.e., the contents of self.__id2label as a data frame.
        frame = self.__get_frame()

        # The data frame `frame` has 2 columns, `code` & `name`.  Each name is a concatenation
        # of a Coarse NER Tag and a branch of the coarse tag.
        splits = frame['name'].str.split(pat='-', n=1, expand=True)
        splits.rename(columns={0: 'parent', 1: 'branch'}, inplace=True)

        frame = frame.copy().join(splits, how='left')
        logging.info(frame)

        return frame
