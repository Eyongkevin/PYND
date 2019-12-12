import os
import random
import argparse

# @TODO Import your Ingestor and MemeEngine classes
from meme_generator import MemeEngine
from quote_engine import Ingestor
import quote_engine.QuoteModel as quoteModel
import  quote_engine.Ingestor as ingestor 

def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, _, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
       
    else:
        img = path
    
    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(ingestor.Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = quoteModel.QuoteModel(body, author)

    meme = MemeEngine('./tmp')

    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--path', type=str, default=None, help='Path to image file')
    parser.add_argument('--body', type=str, default=None, help='Quote body to add to the image')
    parser.add_argument('--author', type=str, default=None, help='Quote author to add to the image')
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
