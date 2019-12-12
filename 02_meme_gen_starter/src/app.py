import random
import os
import sys
import requests
from flask import Flask, render_template, abort, request
from PIL import Image
from app_exceptions import FilePathInvalid
from app_exceptions import InvalidFile
from app_exceptions import ImageSmall

# @TODO Import your Ingestor and MemeEngine classes
from meme_generator import MemeEngine
import quote_engine.QuoteModel as quotemodel
import quote_engine.Ingestor as ingestor
app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    try:
        for f in quote_files:
            quotes.extend(ingestor.Ingestor.parse(f))
    except (FilePathInvalid,InvalidFile) as e:
        return render_template('error.html', error=e.show)

    

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = None
    for root, _, files in os.walk(images_path):
        imgs = [os.path.join(root, file) for file in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    try:
        path = meme.make_meme(img, quote.body, quote.author)
    except (FilePathInvalid, InvalidFile,ImageSmall)  as e:
        return render_template('error.html', error= e.show)

    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    # Get form inputs
    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']

    # Get image from url with requests
    try:
        img = Image.open(requests.get(image_url, stream = True).raw)
    except IOError as er:
            print(er, file=sys.stderr)
            error_msg = "Error! cannot identify image file :\""+image_url+"\". Please check that image path is correct"
            return render_template('error.html', error=error_msg)
            
    
    
     # Save image in temp file `temp`
    req_img_path = './tmp'
    img_path = os.path.join(req_img_path, os.path.basename(image_url))
    img.save(img_path)
   
    # Use meme object to generate a meme using the temp file, body and author
    try:
        path = meme.make_meme(img_path, body, author)
    except (FilePathInvalid, InvalidFile,ImageSmall)  as e:
        return render_template('error.html', error= e.show)

    # Remove the temporary saved image
    # Removing the temporary save image may not be reached if an exception is thrown from `meme.make_meme` above.
    if os.path.exists(img_path):
        os.remove(img_path) 

    if os.path.exists(path):
        return render_template('meme.html', path=path)
    else:
        return render_template('error.html', error=path)
  


if __name__ == "__main__":
    app.run()
