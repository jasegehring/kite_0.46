from collections import OrderedDict
from Bio import SeqIO
import os


def make_mismatch_map(filename):
    """
    This function returns all sample tags and and their single base mismatches
    (hamming distance 1). It returns a dictionary 4*tag_length*number_of_tags
    the size of the original tag)
    e.g. tags AA and TT  result in 4*2*2 = 16 tags
    """

    odict = OrderedDict()
    print('Read the following tags:')
    for record in SeqIO.parse(filename, "fasta"):
        if len(record)%2 == 0:
            print('Length of tag is even! kallisto needs odd k-mers. \n'
                  'Truncate the tag by one bp or increate it by one')
            return: None
        counter = 0
        print(record.seq)
        odict[record.name] = str(record.seq)[:sample_tag_length]
        for pos in range(sample_tag_length):
            letter = str(record.seq)[pos]
            barcode = list(str(record.seq)[:+sample_tag_length])
            if letter == 'A':
                barcode[pos] = 'T'
                odict[record.name + '+-+' + str(pos) + '-1'] = "".join(barcode)
                barcode[pos] = 'G'
                odict[record.name + '+-+' + str(pos) + '-2'] = "".join(barcode)
                barcode[pos] = 'C'
                odict[record.name + '+-+' + str(pos) + '-3'] = "".join(barcode)
            elif letter == 'G':
                barcode[pos] = 'T'
                odict[record.name + '+-+' + str(pos) + '-1'] = "".join(barcode)
                barcode[pos] = 'A'
                odict[record.name + '+-+' + str(pos) + '-2'] = "".join(barcode)
                barcode[pos] = 'C'
                odict[record.name + '+-+' + str(pos) + '-3'] = "".join(barcode)
            elif letter == 'C':
                barcode[pos] = 'T'
                odict[record.name + '+-+' + str(pos) + '-1'] = "".join(barcode)
                barcode[pos] = 'G'
                odict[record.name + '+-+' + str(pos) + '-2'] = "".join(barcode)
                barcode[pos] = 'A'
                odict[record.name + '+-+' + str(pos) + '-3'] = "".join(barcode)
            else:
                barcode[pos] = 'A'
                odict[record.name + '+-+' + str(pos) + '-1'] = "".join(barcode)
                barcode[pos] = 'G'
                odict[record.name + '+-+' + str(pos) + '-2'] = "".join(barcode)
                barcode[pos] = 'C'
                odict[record.name + '+-+' + str(pos) + '-3'] = "".join(barcode)

    return odict