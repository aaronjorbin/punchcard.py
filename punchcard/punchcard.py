#!/usr/bin/env python
"""
Accept a stream of unix timestamps and output a punchcard graph.
Copyright (c) 2013 Aaron Jorbin <aaron@jorb.in> http://aaron.jorb.in

Largly Copied from https://github.com/askedrelic/bash-history-punchcard 
which is Copyright (C) 2009  Matt Behrens <askedrelic@gmail.com> http://asktherelic.com

Requires

-pygooglechart
http://pygooglechart.slowchop.com/

Ideas and most code from:
http://dustin.github.com/2009/01/11/timecard.html
http://github.com/dustin/bindir/blob/master/gitaggregates.py
http://https://github.com/bitly/data_hacks

The MIT License (MIT)
Copyright (c) 2013 Aaron Jorbin 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.


"""

import time
import sys
import os
import subprocess
from optparse import OptionParser
from collections import defaultdict

class TimeHistory(object):

    def __init__(self, options):
        self.h = defaultdict(lambda: 0)
        self.options = options

    def add_logs(self):
        timestamps  = sys.stdin 

        for line in timestamps:
            #Blunt method for ignoring lines that aren't timestamps
            try: 
                self.h[time.strftime("%w %H", time.localtime(float(line.strip())))] += 1
            except:
                pass

    def dump(self):
        for h in range(24):
            for d in range(7):
                sys.stderr.write("%02d %d - %s\n"
                                 % (h, d, self.h["%d %02d" % (d, h)]))

    def to_gchart(self):
        from pygooglechart import ScatterChart
        chart = ScatterChart(800, 300, x_range=(-1, 24), y_range=(-1, 7))

        chart.add_data([(h % 24) for h in range(24 * 8)])

        d=[]
        for i in range(8):
            d.extend([i] * 24)
        chart.add_data(d)

        day_names = "Sun Mon Tue Wed Thu Fri Sat".split(" ")
        days = (0, 6, 5, 4, 3, 2, 1)

        sizes=[]
        for d in days:
            sizes.extend([self.h["%d %02d" % (d, h)] for h in range(24)])
        sizes.extend([0] * 24)
        chart.add_data(sizes)

        #Easier to manually set the x label for the 12am/12pm labels 
        chart.set_axis_labels('x', ['|12am|1|2|3|4|5|6|7|8|9|10|11|12pm|1|2|3|4|5|6|7|8|9|10|11|'])
        chart.set_axis_labels('y', [''] + [day_names[n] for n in days] + [''])

        chart.add_marker(1, 1.0, 'o', '333333', 25)
        
        chart.download(self.options.filename)
        return chart.get_url()

if __name__ == '__main__':
    parser = OptionParser()
    parser.usage = "cat data | %prog [options]"
    parser.add_option("-f", "--file", dest="filename",
                      help="minimum value for graph", default='punchcard.png')
    
    (options, args) = parser.parse_args()
    if sys.stdin.isatty():
        # if isatty() that means it's run without anything piped into it
        parser.print_usage()
        print "for more help use --help"
        sys.exit(1)
    th = TimeHistory(options)
    th.add_logs()
    #th.dump()
    th.to_gchart()
