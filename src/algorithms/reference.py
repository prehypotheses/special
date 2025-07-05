
import pandas as pd


class Reference:

    def __init__(self, id2label: dict):

        self.__id2label = id2label

    def __get_frame(self):

        frame = pd.DataFrame.from_dict(self.__id2label, orient='index')
        frame.reset_index(drop=False, inplace=True)
        frame.rename(columns={'index': 'code', 0: 'name'}, inplace=True)

        return frame

    def __call__(self):
        """

        :return:
        """

        # Get the data frame of Fine NER Tags, i.e., the contents of self.__id2label as a data frame.
        frame = self.__get_frame()

        # The data frame `frame` has 2 columns, `code` & `name`.  Each name is a concatenation
        # of a Coarse NER Tag and a branch of the coarse tag.
        splits = frame['name'].str.split(pat='-', n=1, expand=True)
        splits.rename(columns={0: 'parent', 1: 'branch'}, inplace=True)


        return frame.copy().join(splits, how='left')
