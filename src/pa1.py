#!/usr/bin/env python

###############################################################################
# Programming Assignment #1 - Zipf’s Law in Python
#
# Author:     Matt Richard
# Date:       Wed Feb 20, 2013
# Professor:  Dr. John Weiss
# Course:     CSC 461
# Locations:  McLaury 313
#
# Description: 
#
# Zipf's Law is a curious observation about the statistical distribution of
# words in text: the frequency of any word is inversely proportional to its
# rank in the frequency table. Word frequency is the number of times a given
# word appears in the text. When words are ranked according to frequency, the
# most frequent word is given rank 1, the next-most-frequent word is given rank
# 2, etc. Ties are handled by assigning the middle value in a range of ranks.
# For example, in a two-way tie for most frequent word, each word is given the
# rank of 1.5.
#
# Write a Python program to investigate the validity of Zipf’s Law. Read in
# words from a text file, counting their frequency of occurrence. Print out the
# words sorted by frequency (highest frequency first). Within each frequency
# group, sort the words alphabetically. Then print a table that lists word rank
# and frequency, and plot log(rank) vs. log(frequency). If Zipf’s Law holds for
# that particular text file, you should get a straight line with slope of -1.
#
# Implementation Details
# Read the input words from a text file, whose filename may be given as a
# command-line argument. If no filename is supplied on the command line, prompt
# the user to enter the filename. Print an error message if the usage is
# incorrect or the text file cannot be opened.
#
# The input text file consists of a stream of ASCII characters that you must
# parse into words. For this assignment, restrict words to strings of letters,
# possibly containing embedded single quotes (contractions). Words are
# separated from the surrounding text by anything that is not a letter. The
# word concordance should be case-insensitive, so convert all words to lower
# case prior to insertion in the frequency table. Use regular expressions to
# help extract words from the text file.
#
# Store the words and their frequencies of occurrence in a Python dictionary
# (aka hash table). As you may recall from your data structures course, hash
# table performance is O(1) average for find, insert and delete operations.
# Using a dictionary, you should be able to insert new words and increment word
# frequencies very efficiently.
#
# The output of your program should include the following:
#
# 1. Print the word frequencies to a file with the same name as the input file,
#    but with the extension .wrd. For example, given an input text file
#    file.txt, write the output to file.wrd. File header info should include
#    the input filename, total number of words processed, and number of
#    distinct words found.
#
#    Print words in frequency groups, sorted alphabetically within each group.
#    Do not print empty frequency groups. Print multiple words per line, left
#    justified within columns. For formatting purposes, you may assume that
#    words will not exceed 15 characters in length.
#
# 2. Print rank and frequency information to a CSV (comma separated value)
#    file, suitable for importing into an Excel spreadsheet. This file should
#    have the same name as the input text file, with a .csv extension. Include
#    the same file header info as in the .wrd file.
#
# 3. Print timing results to the console. This will give an indication of how
#    efficiently your program executes.
#
# Usage: $ python3 zipf.py FILENAME
#
# Bugs:  None
###############################################################################


import re
import sys
import time


def open_file( file_name, mode ):
    """Opens a file in the given mode, catching any errors that may occur.

    Given a path to a file and mode, this will attempt to open the file
    in that mode. If an error occurs while openning the file, a description
    of the error will be printed. If the file was successfully open, the file
    handle will be returned; otherwise, None will be returned.
    """
    f = None
    # Open file file_name in the given mode and catch any errors that occur
    try:
        f = open( file_name, mode )
    except IOError:
        print( "Failed to open file: {0}".format( file_name ) )
    except:
        print( "Unknown error occured while opening file: {0}".format(
            file_name) )
    return f


def write_file_header_info( f, input_file_name, total_words, distinct_words ):
    """Writes file header info related to Zipf's Law to the given file.

    Given an output file handle, an input file name, the total number of words
    in the input file, and the total number of distinct words in the file,
    this function will format and write the given information to the output
    file. This function is used with the create_wrd_file and create_csv_file
    functions, as both these file have the same file header info. If any
    errors occur while writing to the output file, an error will be printed
    and the function will return False. Otherwise, if no errors occured, the
    function will return True.
    """
    result = False
    try:
        f.write( "Zipf's Law: rank * freq = const\n" )
        f.write( "-------------------------------\n" )
        f.write( "File:           {0}\n".format( input_file_name ) )
        f.write( "Total words:    {0}\n".format( total_words ) )
        f.write( "Distinct words: {0}\n".format( distinct_words ) )
        result = True
    except AttributeError:
        print( "Error while writing file header info. " \
            "The given file handle is not valid, or is opened for read only." )
    except:
        print( "Unknown error occured while writing file header info." )
    return result


def create_wrd_file( base_file_name, word_count, distinct_words, freq_dict ):
    # Open the output file with .wrd extension and check for failure
    fout = open_file( base_file_name + '.wrd', 'w' )
    if fout == None:
        return False

    # Write header info the to wrd file, and verify it was successful
    if not write_file_header_info( fout, base_file_name + '.txt', word_count,
        distinct_words ):
        fout.close( )
        return False

    for freq in sorted( list( freq_dict.keys( ) ), reverse=True ):
        fout.write( "\n" )
        fout.write( "Words occurring {0}:\n".format(
            "once" if freq == 1 else "{0} times".format( freq ) ) )

        count = 1
        for word in sorted( freq_dict[freq] ):
            fout.write( '{0:<16}'.format( word ) )
            if count % 5 == 0:
                fout.write( '\n' )
            count += 1
        fout.write( "\n" )

    fout.close( )
    return True


def create_csv_file( base_file_name, word_count, distinct_words, freq_dict ):
    # Open the output file with .csv extension and check for failure
    fout = open_file( base_file_name + '.csv', 'w' )
    if fout == None:
        return False

    # Write header info the to csv file, and verify it was successful
    if not write_file_header_info( fout, base_file_name + '.txt', word_count,
        distinct_words ):
        fout.close( )
        return false

    fout.write( "\n" )
    fout.write( "{0:>4},{1:>10},{2:10}\n".format( "rank", "freq", "r*f" ) )

    words = 1
    for freq in sorted( freq_dict.keys( ), reverse=True ):
        # Calculate rank
        count = sum( x for x in range( words, words + len( freq_dict[freq] ) ) )
        rank = count / len( freq_dict[freq] )

        # Write rank, frequency, and rank * frequency to the csv file, formatted
        fout.write( "{0:>4},{1:>10},{2:>10}\n".format( rank, freq, rank * freq ) )

        words += len( freq_dict[freq] )

    fout.close( )
    return True


def main( argv ):
    words_dict = dict( )
    freq_dict = dict( )
    word_count = 0
    p = re.compile( "[a-z]+[a-z']*[a-z]*" )

    # Verify the user provided a file as an argument.
    # If they didn't, prompt for a file name.
    if len( argv ) < 2:
        file_name = input( "Enter a file name: " )
    else:
        file_name = argv[1]

    # Open input file and check for error
    fin = open_file( file_name, 'r' )
    if fin == None:
        return False

    # Read the input file line-by-line, parse words from each line,
    # and put the word into the words dictionary.
    for line in fin:
        for word in p.findall( line.lower( ) ):
            # The regular expression can return words that have a ' at the
            # end of the word, so strip any single quotes from the end of
            # the word.
            word = word.strip( "'" )
            if word != '':
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1
                word_count += 1

    # Input file is not needed anymore, so close it
    fin.close( )

    # Using the words dictionary, create a dictionary based of off the
    # frequencies of words in the words dict. This frequency dictionary
    # stores the words associated with each frequency in a list.
    for word in words_dict:
        freq = words_dict[word]
        if freq in freq_dict:
            freq_dict[freq].append( word )
        else:
            freq_dict[freq] = [word]

    # Remove any directories given in the path to the file
    base_file_name = file_name.rsplit( '/', 1 )[-1]

    # remove file extension
    base_file_name = base_file_name.rsplit( '.', 1 )[0]

    if not create_wrd_file( base_file_name, word_count, len( words_dict ), freq_dict ):
        print( "Failed to create wrd file" )
        return False

    if not create_csv_file( base_file_name, word_count, len( words_dict ), freq_dict ):
        print( "Failed to create csv file" )
        return False

    return True


if __name__ == '__main__':
    start_time = time.time( )

    if not main( sys.argv ):
        sys.exit( 1 )

    end_time = 1000.0 * ( time.time( ) - start_time )
    print( "Elapsed time = {0} msec".format( end_time ) )
