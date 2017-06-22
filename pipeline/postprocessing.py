"""Used for processing a first-pass transcript that contains a bunch of
paragraphs separated by alternating speakers and a variable number of newlines
during manual paragraph separation.

Very quickly written.
"""

import sys


if __name__ == '__main__':
    fn_a = sys.argv[1]
    fn_b = sys.argv[2]
    interviewer = sys.argv[3]
    interviewee = sys.argv[4]
    i = 0

    with open(fn_a, 'r') as rhandle:
        with open(fn_b, 'w') as whandle:
            for line in rhandle.readlines():
                if line.strip() != '':
                    if i % 2 == 0:
                        whandle.write('{}: {}\n'.format(interviewer, line))
                        i += 1
                    else:
                        whandle.write('{}: {}\n'.format(interviewee, line))
                        i += 1
