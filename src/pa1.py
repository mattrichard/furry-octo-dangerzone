#!/usr/bin/env python3

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
    try:
        f = open( file_name, mode )
    except IOError:
        print( "Failed to open file: {0}".format( file_name ) )
    except:
        print( "Unknown error occured while opening file: {0}".format(
            file_name) )
    return f


def write_file_header_info( f, input_file_name, total_words, distinct_words ):
    f.write( "Zipf's Law: rank * freq = const\n" )
    f.write( "-------------------------------\n" )
    f.write( "File:           {0}\n".format( input_file_name ) )
    f.write( "Total words:    {0}\n".format( total_words ) )
    f.write( "Distinct words: {0}\n".format( distinct_words ) )


def create_wrd_file( base_file_name, word_count, distinct_words, freq_dict ):
    # Open the output file with .wrd extension and check for failure
    fout = open_file( base_file_name + '.wrd', 'w' )
    if fout == None:
        return False

    write_file_header_info( fout, base_file_name + '.txt', word_count, distinct_words )

    for freq in sorted( list( freq_dict.keys( ) ), reverse=True ):
        fout.write( "\n" )
        fout.write( "Words occurring {0}:\n".format( "once" if freq == 1 else "{0} times".format( freq ) ) )
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

    write_file_header_info( fout, base_file_name + '.txt', word_count, distinct_words )

    fout.write( "\n" )
    fout.write( "rank,      freq,       r*f\n" )

    words = 1
    for freq in sorted( freq_dict.keys( ), reverse=True ):
        count = sum( x for x in range( words, words + len( freq_dict[freq] ) ) )
        rank = count / len( freq_dict[freq] )

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

    fin.close( )

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
