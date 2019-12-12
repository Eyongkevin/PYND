"""
Encapsulation:::
    It is a fundamental concept in OOP. It describes the idea of wrapping data and methods
    that work on data within a single unit. This restrict accessing and accidental modification
    or change of data

Interfacing::
    Interface of an object is what the object can do to play its role in a system.
    In OOP, interface of an object are publicly accessible methods that other part of the system can use to interact
    with the object.
    It is strickly enforced in OOP languages like Java, but Python doesn't. We need to trick it to work.

    In python we use ABCs(Abstract Base Classes) which defines abstract objects with abstract methods and every
    object that derives from it is then forced to implement these abstract methods. 
"""
import abc
import pandas as pd
import docx
from typing import List
import pdftotext
import subprocess
import os 

import app_exceptions.FileExceptions as file_excep
import quote_engine.QuoteModel as quotemodel
import helper_func.helper as helper_


class IngestorInterface(abc.ABC):

    @classmethod
    def can_ingest(cls, path) ->bool:
        """ Extract extension and check if it is equal to the ingestor
        @param:
            path: str
                Path to the file
        @return:
            bool
        """

        ext = path.split('.')[-1]
        return (ext == cls.extension)

    @classmethod
    @abc.abstractmethod
    def parse(cls, path: str) -> List[quotemodel.QuoteModel]:
        """This is an abstract method, so no need to implement it here
        @param:
            path : str
                path to the file 
        @return:
            return list of types QuoteModel
        """
        pass

class IngestCSV(IngestorInterface):
    """Ingestor for CSV. Ingest CSV files and process the content.
    The CSV file has text which is arrange as body and author. 
        """
    extension = 'csv'

    @classmethod
    def parse(cls, path: str) -> List[quotemodel.QuoteModel]:
        """Get CSV file path and extract the content.
        @param:
            path : str
                path to the csv file 
        @return:
            return list of types QuoteModel
        """
        body_author_list = []
        read = pd.read_csv(path)
        for item in read.values:
            body_author_list.append(quotemodel.QuoteModel(*item))
        return body_author_list

        

class IngestPDF(IngestorInterface):
    """Ingestor for PDF. Ingest PDF files and process the content.
    The PDF file has text which is arrange as body and author. 

    We use pdftotext library to open the pdf file in a subprocess. 
    This converts the pdf into a txt file, then we extract the information 
    and then delete the temporary created txt file.
        """
    extension = 'pdf'
    
    @classmethod
    def parse(cls, path: str) -> List[quotemodel.QuoteModel]:
        """Get PDF file path and extract the content.
        @param:
            path : str
                path to the PDF file 
        @return:
            return list of types QuoteModel
        """
        cmd = ['pdftotext','-layout', path]
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = run.communicate()
        #display errors if they occur
        if err:
            print(err)
            return None
        else:
            fileastextfile = os.path.splitext(path)[0]+'.txt'
            QuoteModel_obj = IngestTXT.parse(fileastextfile)
            
            # Delete temporary file
            if os.path.exists(fileastextfile):
                os.remove(fileastextfile)
            else:
                print("Can not delete the file as it doesn't exists")
                
            return QuoteModel_obj

# encode with `utf-8-sig` to remove the BOM u'\ufeff'
class IngestTXT(IngestorInterface):
    """Ingestor for TXT. Ingest TXT files and process the content.
    The TXT file has text which is arrange as body and author. 
        """
    
    extension = 'txt'

    @classmethod
    def parse(cls, path: str) -> List[quotemodel.QuoteModel]:
        """Get TXT file path and extract the content.
        @param:
            path : str
                path to the TXT file 
        @return:
            return list of types QuoteModel
        """
        body_author_list = []
        with open(path, 'r', encoding='utf-8-sig') as f:
            for note in f:
                helper_.Helper.process_text(note, body_author_list)
        return body_author_list
                

class IngestDOCX(IngestorInterface):
    """Ingestor for DOCX. Ingest DOCX files and process the content.
    The DOCX file has text which is arrange as body and author. 

    We use the docx library to extract the docx file content 
    for processing.
        """
    extension = 'docx'
    
    @classmethod
    def parse(cls, path: str) -> List[quotemodel.QuoteModel]:
        """Get DOCX file path and extract the content.
        @param:
            path : str
                path to the DOCX file 
        @return:
            return list of types QuoteModel
        """
        body_author_list = []
        doc = docx.Document(path)
        for note in doc.paragraphs:
            helper_.Helper.process_text(note.text, body_author_list)
        return body_author_list


class Ingestor(IngestorInterface):
    """The main Ingestor. We make sure we assign the various ingestors the appropriate files
    for processing. 

    Raise an invalid file exception if fail doesn't match any of the ingestors.
    """
        
    @classmethod
    @helper_.Helper.check_path
    def parse(cls, path: str)->List[quotemodel.QuoteModel]:
        """Control the ingestion process. It determine which ingest object should be called to process
        a file base on the file's extension.

        @param:
            path: str
                path to the file to process
        @return:
            A list of quotemodel object containing the processed text and author
        """
  
        if IngestTXT.can_ingest(path):
            return IngestTXT.parse(path)
        if IngestPDF.can_ingest(path):
            return IngestPDF.parse(path)
        if IngestDOCX.can_ingest(path):
            return IngestDOCX.parse(path)
        if IngestCSV.can_ingest(path):
            return IngestCSV.parse(path)

        raise file_excep.InvalidFile(path)

        
        
        
      