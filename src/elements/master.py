"""Module"""
import typing

import datasets


class Master(typing.NamedTuple):
    """
    The data type class ⇾ Master

    id2label : dict
        The codes & names of the fine grain labels of the FEW NERD (Few-Shot Named Entity Recognition Dataset) dataset
    label2id : dict
        The inverse of the above
    data: datasets.DatasetDict
        The FEW NERD (Few-Shot Named Entity Recognition Dataset) dataset
    """

    id2label: dict
    label2id: dict
    data: datasets.DatasetDict
