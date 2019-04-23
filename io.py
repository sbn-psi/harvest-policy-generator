'''
Contains utility methods to make it a little more convenient to work with
file IO
'''
import os.path


def make_parent(filename):
    '''
    Creates the parent directories of a given file.
    '''
    dirname = os.path.dirname(filename)
    if not(os.path.exists(dirname)):
        os.makedirs(dirname)


def open_writeable(filename):
    '''
    Opens a file for writing, creating the parent directories
    if necessary
    '''
    make_parent(filename)
    return open(filename, 'w')


def writefile(filename, output):
    '''
    Writes the given string to a outfile.
    '''
    outfile = open_writeable(filename)
    try:
        outfile.write(output)
    finally:
        outfile.close()


def readfile(filename):
    '''
    Reads the given infile into a string.
    '''
    infile = open(filename)
    try:
        return infile.read()
    finally:
        infile.close()


def readpartial(filename, length):
    '''
    Reads the given infile into a string.
    '''
    infile = open(filename)
    try:
        return infile.read(length)
    finally:
        infile.close()


def pad_lines(document, width=78):
    '''
    Adjusts the width of each line in a document to the specified width.
    '''
    src_lines = document.split("\n")
    out_lines = [line.ljust(width) + "\r\n" for line in src_lines]
    return "".join(out_lines)


def get_file_width(filename):
    '''
    Determines the width of a fixed width text file.
    '''
    infile = open(filename)
    try:
        return len(infile.readline())
    finally:
        infile.close()
