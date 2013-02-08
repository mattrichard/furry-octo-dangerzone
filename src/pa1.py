#!/usr/bin/env python3

import sys
from operator import itemgetter

def open_file( file_name, mode ):
    f = None
    try:
        f = open( file_name, mode )
    except IOError:
        print( "Failed to open file: {0}".format( file_name ) )
    return f

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

    output_file_name = file_name.rsplit( '.', 1 )[0] + '.wrd'

    # Open output file and check for error
    fout = open_file( output_file_name, 'w' )
    if fout == None:
        fin.close( )
        return False

    for line in fin:
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

    fin.close( )
    fout.close( )
    return True


if __name__ == '__main__':
    if not main( sys.argv ):
        sys.exit( 1 )
