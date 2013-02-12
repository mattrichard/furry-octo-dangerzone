#!/usr/bin/env python3

import sys
import re
# from operator import itemgetter

def open_file( file_name, mode ):
    f = None
    try:
        f = open( file_name, mode )
    except IOError:
        print( "Failed to open file: {0}".format( file_name ) )
    return f


def write_to_csv_file( file_name, word_count, distinct_words ):
    fout = open_file( file_name + '.csv', 'w' )
    if fout == None:
        return False
    fout.write( "Zipf's Law: rank * freq = const\n" )
    fout.write( "File:           {0}.txt\n".format( file_name ) )
    fout.write( "Total words:    {0}\n".format( word_count ) )
    fout.write( "Distinct words: {0}\n".format( distinct_words ) )
    fout.write( "\n" )
    fout.write( "rank,      freq,       r*f\n" )

    fout.close( )
    return True


def main( argv ):
    words_dict = { }
    freq_dict = { }
    word_count = 0

    if len( argv ) < 2:
        file_name = input( "Enter a file name: " )
    else:
        file_name = argv

    # Open input file and check for error
    fin = open_file( file_name, 'r' )
    if fin == None:
        return False

    base_file_name = file_name.rsplit( '.', 1 )[0]

    # Open output file and check for error
    fout = open_file( base_file_name + '.wrd', 'w' )
    if fout == None:
        fin.close( )
        return False

    #pat = "\s*\A[A-Za-z][A-Za-z']\Z[A-Za-z]\s*"
    pat = "[^A-Za-z]*[^A-Za-z']+[^A-Za-z]*"
    p = re.compile( pat )

    for line in fin:
        print( "line: ", line )
        #if p.match( line ):
        #print( 'words: ', p.findall( line ) )
        print( 'words: ', p.split( line ) )
        line_words = line.split( )
        for word in line_words:
            word = word.lower( )
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1
            word_count += 1

    for word in words_dict:
        freq = words_dict[word]
        if freq in freq_dict:
            freq_dict[freq].append( word )
        else:
            freq_dict[freq] = [word]

    fout.write( "Zipf's Law: word concordance\n" )
    fout.write( "----------------------------\n" )
    fout.write( "File:           {0}\n".format( file_name ) )
    fout.write( "Total words:    {0}\n".format( word_count ) )
    fout.write( "Distinct words: {0}\n".format( len( words_dict ) ) )

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

    if not write_to_csv_file( base_file_name, word_count, len( words_dict ) ):
        print( "Failed to create scv file" )

    fin.close( )
    fout.close( )
    return True


if __name__ == '__main__':
    if not main( sys.argv ):
        sys.exit( 1 )
