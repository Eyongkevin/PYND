class QuoteModel:
    """Encapsulate the body and author
    We use @property decorator to make body and author to be available as a property or accessed as variables.

    @Param:
        body: str
            The quote to process
        author: str
            The author's name
    """
    def __init__(self, body:str, author:str):
        self._body = body
        self._author = author

    @property
    def body(self)->str:
        return self._body
    @property
    def author(self)->str:
        return self._author