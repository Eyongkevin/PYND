import sys
class ImageExceptions(Exception):
    """Custom exception that will handle any error that will occur in the cause of processing the image
    """
    def __init__(self, img_path, msg=None):
        if msg is None:
            msg = "Error with the file"
        self.img_path = img_path
        self.msg = msg

    @property
    def show(self):
        """Display error message in a readable way
        @return:
            full_msg: str:
                full message formated in a readable format
        """

        full_msg = self.msg +": "+ self.img_path
        print(full_msg, file=sys.stderr)
        return full_msg
      

class ImageSmall(ImageExceptions):
    """Class takes care of exception for images that are smaller than the required size
    """
    def __init__(self, path, msg="Image size is small"):
        super(ImageSmall, self).__init__(path, msg)