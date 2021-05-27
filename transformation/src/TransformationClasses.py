# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from pathlib import Path
import logging
import pandas as pd
from abc import ABC, abstractmethod

class File(ABC):
  """A class used to serve as an interface, it defines methods for child classes
  to extend and implement on their own.
  """
  def __init__(self, file_path:Path):
    self.file_path = file_path
    self.df = None

  def __repr__(self):
    return f"AbstractClass('{self.file_path}')"

  def __del__(self):
    logging.info('Object Terminated')

  @abstractmethod
  def load_dataframe(self) -> None:
    """This method must be implemented in a child class
    """
    pass

  @abstractmethod
  def clean_dataframe(self) -> None:
    """This method must be implemented in a child class
    """
    pass

  def clean_str_columns(self, list_of_str_columns:list) -> None:
    """This is a generic method that uses the self.df (pandas dataframe) to clean all the columns that are string type.

    Args:
    list_of_str_columns (list): [List of str columns in dataframe]
    """
    for column in list_of_str_columns:
      self.df[column].fillna("", inplace=True)
      self.df[column] = self.df[column].astype(str).str.strip()

  def clean_int_columns(self, list_of_int_columns:list) -> None:
    """This is a generic method that uses the self.df (pandas dataframe) to clean all the columns that are int type.

    Args:
    list_of_int_columns (list): [List of int columns in dataframe]
    """
    pass

  def clean_date_columns(self, list_of_date_columns:list) -> None:
    """This is a generic method that uses the self.df (pandas dataframe) to clean all the columns that are date type.

    Args:
    list_of_date_columns (list): [List of date columns in dataframe]
    """
    pass

class Allegis(File):

  __original_columns = ['VENDOR_CODE', 'SITE_CODE2', 'AMOUNT', 'INVOICE_NUMBER',
                        'INVOICE_DATE', 'ENTITY', 'LOB', 'CC', 'ACCOUNT',
                        'CUSTOMER_PARTY_NUMBER', 'PRODUCT', 'AFFILATE', 'FUTURE_1',
                        'FUTURE_2', 'MEMO', 'STAT_DATE', 'STAT_NAME', 'STAT_VALUE',
                        'INV_CURRENCY', 'INVOICE_TYPE', 'PO_NUMBER', 'HDR_DESCRIPTION',
                        'PO_LINE_NUMBER', 'QUANTITY', 'GROUP_ID', 'PROJECT',
                        'TASK', 'EXPENDITURE_TYPE', 'EXPENDITURE_ORG', 'EXPENDITURE_DATE',
                        'PA_QUANTITY', 'XXX', 'RATE_COMPONENT']

  __original_suffix = '.csv'

  def __init__(self, file_path:Path):
    super(Allegis, self).__init__(file_path=file_path)
    self.df = self.load_dataframe()

  def __repr__(self):
    return f"Allegis('{self.file_path}')"

  def load_dataframe(self) -> None:
    """ Loading data effectively from a .csv to a DataFrame object.

    Returns:
      None: This operation is inplace.
    """
    tmp_df = pd.read_csv(open(self.file_path, 'rb'), nrows = 1)

    if self.file_path.suffix != Allegis.__original_suffix:
      raise ValueError("File type not supported")
    if Allegis.__original_columns != tmp_df.columns.to_list():
      raise ValueError("Columns do not match with the original format in their position or number!")

    return pd.read_csv(open(self.file_path, 'rb'))

  def clean_dataframe(self) -> None:
    """Cleans columns that are set to be string in the DataFrame.

    Returns:
      None: This operation is inplace.
    """
    str_columns = ['VENDOR_CODE','INVOICE_NUMBER','LOB','MEMO','STAT_NAME','INV_CURRENCY',
                   'INVOICE_TYPE','HDR_DESCRIPTION','GROUP_ID','PROJECT']

    self.clean_str_columns(str_columns)

class FileFactory:

  def __init__(self, file_path:Path):
    self.file_path = file_path

  @property
  def file_path(self):
    # Getter
    return self._file_path

  @file_path.setter
  def file_path(self, value:Path):
    # Setter
    if not value.exists():
      raise ValueError("File does not exists!")
    self._file_path = value

  def creates(self) -> File:
    """Creates an object of File type

    Returns:
      File: Returns an obj of class File
    """
    file_name: str = self.file_path.name.lower()

    if 'allegis' in file_name:
      file_object = Allegis(self.file_path)
    else:
      file_object = None

    if isinstance(file_object, File):
      return file_object
    else:
      raise ValueError("This file is not supported!")
