"""Module source.py"""
import logging

import datasets

import config
import src.elements.service as sr
import src.elements.s3_parameters as s3p
import src.data.initial


class Interface:
    """
    A class for data preparation.
    """

    def __init__(self, service: sr.Service,  s3_parameters: s3p):
        """

        :param service: A suite of services for interacting with Amazon Web Services.<br>
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

        # The Data
        self.__dataset: datasets.DatasetDict = datasets.load_dataset(
            "DFKI-SLT/few-nerd", "supervised")

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)


    def exc(self):
        """

        :return:
        """

        # The data segments
        self.__logger.info('The data segments:\n%s', self.__dataset.keys())
        self.__logger.info('The training set: %s\n%s',
                           type(self.__dataset['train']), self.__dataset['train'].shape)
        self.__logger.info('The validation set: %s\n%s',
                           type(self.__dataset['validation']), self.__dataset['validation'].shape)
        self.__logger.info('The test set: %s\n%s',
                           type(self.__dataset['test']), self.__dataset['test'].shape)

        # Delete data sets within the storage area
        src.data.initial.Initial(service=self.__service, s3_parameters=self.__s3_parameters).exc()

        # Persist
        dataset_dict_path = 's3://' + self.__s3_parameters.internal + '/' + self.__configurations.prefix
        self.__logger.info(dataset_dict_path)
        self.__dataset.save_to_disk(dataset_dict_path=dataset_dict_path)
