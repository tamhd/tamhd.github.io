#!/usr/bin/env python3

"""
This program attempts to break cipher from public/private key. Instead of going after
the underlying principle, this program toys with the idea to create a mapping from
the cipher to the plain characters. 

It follows the Expectation Maximization (EM) algorithm to generate word alignment. 
The algorithm was useful to handle more ambiguous situation with machine 
translation, but "hey, as long as it works" :-)
pseudocode: http://www.inf.ed.ac.uk/teaching/courses/emnlp/slides/emnlp15.pdf

An example of a public/private key RSA that could be broken: http://www.pedrodiaz.com/cs/RSA.sh
Special shoutout to Pedro for writing the awesome toy encoder

This (poorly and hastily written) "source code" is public domain. Do whatever you want with it.
Send comments or suggestions to tamhd [DOT] nus (AT) gmail [DOT] com
Tam
"""

import argparse
import sys
from collections import defaultdict  # let's abuse this convenient library

parser = argparse.ArgumentParser(description="""Decode a public/private key character encoder!
    This program provides three steps: \n
            1. Collect the input and cipher text on line by line basis (much easier if the public key is known) \n
            2. Execute action "analyse" to generate a lexicon from the cipher text to plain text character \n
            3. Execute action "decode" to decipher an input file \n
    """)
parser.add_argument("action", type=str, help="analyse/decode - choose your action!")
parser.add_argument("-i", "--input", help="input file of plain text")
parser.add_argument("-c", "--cipher", help="input file of cipher text")
parser.add_argument("-d", "--decode", help="input file of lexicon dictionary")
parser.add_argument("-v", "--verbose", action="store_true")
try:
    options = parser.parse_args()
except:
    parser.print_help(sys.stderr)
    print(""" Step-by-step execution \n
    Step 1: <do separately> Put the available ciphertext in cipher.text and the plaintext in plain.text \n
    Step 2: ./em_decoder analyse -i plain.text -c cipher.text -d lexicon.text
    Step 3: <do separately> Put the mysterious cipher text in to_decode.text
    Step 4: ./em_decoder decode -d lexicon.text -c to_decode.text

    """, file=sys.stderr)

    sys.exit(0)


def emAnalyser(e_sentences, f_sentences, iterations=20):
    """ Given two arrays of matching sentences, return the mapping between input and output characters
    """
    print("Generate the lexicon", file=sys.stderr)
    # generate the dictionary
    e_set, f_set = set(), set()
    for e_s in e_sentences:
        for e in e_s:
            e_set.add(e)
    for f_s in f_sentences:
        for f in f_s:
            f_set.add(f)

    e_chars = sorted(e_set)
    f_chars = sorted(f_set)
    t = defaultdict(lambda: defaultdict(lambda: 1.0 / len(f_chars)))
    # expectation - maximization step 
    for iter in range(iterations):
        if not iter % 5:
            print("Iteration: %s" % (iter + 1), file=sys.stderr)

        # initialize uniformly
        count = defaultdict(lambda: defaultdict(lambda: 0))
        total = defaultdict(lambda: 0)
        for e_s, f_s in zip(e_sentences, f_sentences):
            total_s = defaultdict(lambda: 0)
            # re estimate the expectation
            for e in e_s:
                total_s[e] = 0
                for f in f_s:
                    total_s[e] += t[e][f]
            # maximize the probability
            for e in e_s:
                for f in f_s:
                    count[e][f] += 1.0 * t[e][f] / total_s[e]
                    total[f] = 1.0 * t[e][f] / total_s[e]
        for f in f_chars:
            for e in e_chars:
                t[e][f] = 1.0 * count[e][f] / total[f]
    
    # Keep the top results
    prob = defaultdict(lambda: ("?", 0))
    try:
        fopen = open(options.decode, "w")
    except:
        fopen = sys.stdout
    for f in f_chars:
        match_e, match_val = matchGetter(t, f)
        prob[f] = (match_e, match_val)
        print("%s ||| %s ||| %s" % (f, match_e, round(match_val, 2)), file=fopen)
    fopen.close()
    print("Finish the lexicon", file=sys.stderr)
    return prob


def matchGetter(prob, char):
    """ Given a two dimentional dictionary, find the key with the highest value
    """
    max_val = 0
    max_key = "?"
    for key in prob:
        if prob[key][char] > max_val:
            max_key, max_val = key, prob[key][char]
    return max_key, max_val

def analyse():
    """ Given a pair of encoded text, map out the potential code
    """
    input_lines , cipher_lines = [], []
    with open(options.input, 'r') as fopen:
        for line in fopen:
            input_lines.append(list(line.strip())) # split by char in plain text

    with open(options.cipher, 'r') as fopen:
        for line in fopen:
            cipher_lines.append(line.strip().split()) # split by splace in cipher text
    
    emAnalyser(input_lines, cipher_lines)

def decode():
    """ Given a decode file and a cipher file, generate the original text
    """
    # read the lexicon and store the map
    prob = defaultdict(lambda: ("?", 0))  # replace unk by question mark
    with open(options.decode, "r") as fopen:
        for line in fopen:
            f, e, p = line.strip().split(" ||| ")
            prob[f] = (e, float(p))

    # read the cipher text and print the input text
    with open(options.cipher, "r") as fopen:
        for line in fopen:
            res = []
            for f in line.strip().split():
                e, p = prob[f]
                res.append(e)
            print("".join(res), file=sys.stdout)
    return


# naively handle the action, there is no time to write a complete parser!!!
# doesn't work if the parameters are missing, please always provide all
if __name__ == '__main__':
    if options.action == "analyse":
        # input file and cipher file are required for training
        # if lexicon file is not specified, write to stdout instead
        analyse()
    elif options.action == "decode":
        # lexicon file and cipher file are required
        decode()
    else:
        analyse()
        decode()
