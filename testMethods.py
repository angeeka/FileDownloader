
import task
import os


def test_imageFile():
    url = "http://www.c2cis.com/uploads/2/1/4/6/21468406/1733734.png"
    outfile = os.getcwd()
    assert task.getInput(url, outfile) == 1

def test_textFile():
    url = "https://en.wikipedia.org/wiki/Computer"
    outfile = os.getcwd()
    assert task.getInput(url, outfile) == 1

def test_invalidFile():
    url = "hppt://en.wikipedia.org/wiki/Computer"
    outfile = os.getcwd()
    assert task.getInput(url, outfile) == 0

