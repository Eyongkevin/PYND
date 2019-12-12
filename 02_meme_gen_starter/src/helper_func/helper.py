import app_exceptions.FileExceptions as file_excep
import quote_engine.QuoteModel as quotemodel
import os
import functools

extensions = ['.jpg','.png']

class Helper:
        """Helper class which contain both decorators and functions that may lead to repeatation. 
        This function enforces the idea of DRY(Don't Repeat Yourself)
        """

        @classmethod
        def process_text(cls, txt:str, output_list:list)->None:
                """Process text by removing extra quotation marks(") and also split the text at '-' which 
                separates the body from the author. 

                @params:
                        txt: str
                                text to process
                        output_list: list
                                list to contain the processed text. The list is modified inplace since it is mutable.

                """

                txt = [i.replace('"','').strip() for i in txt.split('-')]
                if len(txt) == 2:
                        output_list.append(quotemodel.QuoteModel(*txt))

        @classmethod
        def get_resizedHeight_from_width(cls, width, img_width, img_height)->float:
                """Given the width, we generate a resized height while conserving ratio

                @params:
                        width: float
                                width to resize the image to
                        img_width: float
                                width of the image to resize
                        img_height: float
                                height of the image to resize
                @return
                        hsize: float
                                The resized height generated
                """
                        
                wpercent = (width/float(img_width))
                hsize = int((float(img_height)*float(wpercent)))
                return hsize


        ###############################
        # Decorators to help do some check before or after the function processes the data.
        # We use 'functools.wraps for debugging purposes. 
        ################################

        # Decorators
        @classmethod
        def check_path(cls, func):
                """make sure the given path exists. If not exist, raise a File Path Invalid exception
                """
                @functools.wraps(func)
                def wrapper(*arg):
                        path = arg[-1]
                        if not os.path.exists(path):
                                raise file_excep.FilePathInvalid(path)     
                        res = func(*arg)
                        return res
                return wrapper

        @classmethod
        def check_extension(cls, func):
                """Make sure the given file has a valid extension. If not, raise an Invalid File extension.
                """
                @functools.wraps(func)
                def wrapper(*arg):
                        path = arg[-1]
                        if not os.path.splitext(path)[1].lower() in extensions:
                                raise file_excep.InvalidFile(os.path.splitext(path)[1].lower())      
                        res = func(*arg)
                        return res
                return wrapper

