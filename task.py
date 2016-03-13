
import os
from sys import argv
import shutil
import requests
import logging
import argparse


logger = logging.getLogger('task')
hdlr = logging.FileHandler('logTask.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def arguments(argv):
    '''
    Returns the files to be downloaded and the folder in which to download.
    :param argv: Command line argument(s) that are to be processed.
    :return: argumentparser object
    '''

    def getFileName():#function to run if input filename not given in command line
        if len(argv) == 1:
            print "Enter the filename with filepath."
            fileName = raw_input()
            return inputFileLoader(fileName)

    def inputFileLoader(fileName):#function to get the urls
        try:
            if os.access(fileName, os.R_OK):
                with open(fileName) as r:
                    x = r.read().splitlines()
                    return x
        except Exception as e: logger.exception( 'File not found. Error %s', e)


    def outputDir(string):#function to get directory name to save the files to be downloaded
        if not os.path.exists(string):
            os.makedirs(string)
        return string


    parser = argparse.ArgumentParser(description='Script to download and store images.')
    parser.add_argument('infile', nargs='?', type=inputFileLoader, default = getFileName(),help = 'Filename where urls are present.')
    parser.add_argument('outpath', nargs='?', type=outputDir, default=os.getcwd(), help = 'Directory name to save the files downloaded.')
    return parser.parse_args()



def getInput(url, outfile):
    '''
    Returns successfully if all files are downloaded.
    :param url:    website url of the image.
    :param outfile: directory where the file is to be saved.
    :return:        File successfully downloaded   1
                    Otherwise                      0
    '''
    name = os.path.join(outfile, url.split('/')[-1])
    try:
        response = requests.get(url, stream=True)
        if response.ok:
            with open(name, 'wb') as img:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, img)
            logger.info('%s Download finished',name)
            return 1
        else:
            logger.exception('Error in downloading. Error status %s', response.status_code)
            return 0
    except Exception as e:
        logger.exception('Error in downloading. Error status %s', e)
        return 0


def main():
    '''
    Main function
    :return: all files successfully downloaded  1
            otherwise                           0
    '''
    args = arguments(argv)
    return 1 if[getInput(url, args.outpath) for url in args.infile] else 0


if __name__ == '__main__':
    exit(main())
