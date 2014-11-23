""" 
http://docs.python.org/2/library/difflib.html

Above is a link to the original script, which was transformed
into a Splunk search command.  

James Donn - Author
Chhean Saur - Contributor

jdonn@splunk.com
"""

import re
import csv
import sys
import splunk.Intersplunk
import string
import sys, os, time, difflib, optparse

### Enable logging to file
debug = 0

### open logfile
if debug:
    f = open('/tmp/workfile', 'a')
    f.write('\nStarting\n')
    f.write('argv length ' + str(len(sys.argv)) + '\n')
    for arg in sys.argv:
        f.write('we have argv of %r.\n' % arg)
    f.write('argv 0 - \"' + sys.argv[0] + '\"\n')

### Set the html dir
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../appserver/static/html/sdiff.html')
output = open(filename, 'w+')

### This and another isgetinfo statement below enable ARGV debugging
### Comand will then require __EXECUTE__ as the first arguement.
if debug:
    (isgetinfo, sys.argv) = splunk.Intersplunk.isGetInfo(sys.argv)

### Declare optional args
u    = ''
xpo  = ''
n    = 3
c    = False
w    = None
last = ''

### Expect arguments in any order, ignoring anything that doesn't belong, but in this format: 
### <search> | sdiff pos1=n* pos2=n* xpo=(line number to ignore) n=# c=True|False 
### * Are the only required fields
if len(sys.argv) < 2:
    splunk.Intersplunk.parseError("Invalid argument '%s'" % arg)
for arg in sys.argv:
    if re.search('^pos1\s?=\s?', arg, re.IGNORECASE):
        pos1 = re.sub(r'^pos1\s?=\s?', "", arg)
        if debug:
            f.write('pos1 = \"' + pos1 + '\"\n')
    if re.search('^pos2\s?=\s?', arg, re.IGNORECASE):
        pos2 = re.sub(r'^pos2\s?=\s?', "", arg)
        if debug:
            f.write('pos2 = \"' + pos2 + '\"\n')
    if re.search('^u\s?=\s?(t[rue]?|1)', arg, re.IGNORECASE):
        u = re.sub(r'^u\s?=\s?', "", arg)
        if debug:
            f.write('u = \"' + u + '\"\n')
    if re.search('^xpo=.*', arg, re.IGNORECASE):
        xpo = re.sub(r'^xpo=', "", arg)
        if debug:
            f.write('xpo = \"' + xpo + '\"\n')
    if re.search('^n=', arg, re.IGNORECASE):
        n = re.sub(r'^n=', "", arg)
        n = int(n)
        if debug:
            f.write('n = \"' + n + '\"\n')
    if re.search('^c=', arg, re.IGNORECASE):
        c = re.sub(r'^c=', "", arg)
        ### Boolean False is an empty string
        if c == "False":
            c = ''
        if debug:
            f.write('c = \"' + c + '\"\n')
    if re.search('^w=', arg, re.IGNORECASE):
        w = re.sub(r'^w=', "", arg)
        if re.search(r'\d+', arg):
            w = int(w)
        if debug:
            f.write('w = \"' + w + '\"\n')
    if re.search('^last=', arg, re.IGNORECASE):
        last = re.sub(r'^last=', "", arg)
        ### Boolean False is an empty string
        if last == "False":
            last = ''
        if debug:
            f.write('l = \"' + l + '\"\n')

    if debug:
        f.write('n = \"' + str(n) + '\"\n')
        f.write('c = \"' + str(c) + '\"\n')

### Validate required fields
if len(pos1) == 0 or len(pos2) == 0:
    splunk.Intersplunk.parseError("Invalid or empty field '%s'" % field)

### If a field exists, make sure it is the proper type.
### TO DO ^


### Now that you have stated all of argv for testing above, outputInfo
### outputInfo automatically calls sys.exit()
if debug:
    if isgetinfo:
        splunk.Intersplunk.outputInfo(False, False, True, False, None, True)

try:
    if debug:
        f.write('Getting results from Splunk\n')
    results = splunk.Intersplunk.readResults(None, None, True)

    if debug:
        f.write('Success\n')
        f.write('Size of resultset' + str(len(results)) + '\n')
        for res in results:
            if res['_raw']:
                f.write('date = ' + res['_time']+ ' Sourcetype = ' + res['sourcetype'] + ' RAW = \"' + res['_raw']  + '\"\n')

    ### We only care about _raw, lets remove everything else
    if debug:
        for res in results:
            if res['_raw']:
                f.write('We have %r' % res['_raw'])

    ### Prepare pos1 and pos2
    pos1 =  int(pos1)
    pos1 -= 1
    pos2 =  int(pos2)
    pos2 -= 1

    if debug:
        f.write("The pos1 element is:\n {0}\n".format(results[pos1]['_raw']))
        f.write("The pos2 element is:\n {0}\n".format(results[pos2]['_raw']))

    ### Extract the file names (command names) and time from the first line
    fromdate = results[pos1]['_time']
    todate   = results[pos2]['_time']
    fromfile = results[pos1]['sourcetype']
    tofile   = results[pos2]['sourcetype']

    if debug:
        f.write('fromdate=' + fromdate + '\n')
        f.write('todate=' + todate + '\n')
        f.write('fromfile=' + fromfile + '\n')
        f.write('tofile=' + tofile + '\n')

    ### Set fromlines and tolines
    fromlines = []
    tolines   = []
    fromlines = results[pos1]['_raw'].split('\n')
    tolines   = results[pos2]['_raw'].split('\n')
    
    ### Remove the xpo line
    if xpo:
        xpo=int(xpo)
        xpo -=1
        del fromlines[int(xpo)]
        del tolines[int(xpo)]

        if debug:
            f.write('we have XPO of %r.\n' % xpo)
            for line in fromlines:
                f.write('fromlines list is %r \n' % line)
            for line in tolines:
                f.write('tolines list is %r \n' % line)

    ### Pass doctored up pos1 and pos2 to the diff command and create the html
    diff = difflib.HtmlDiff(wrapcolumn=w).make_file(fromlines, tolines, fromfile, tofile, context=c, numlines=n)

    ### Change the auto refresh so we see updates right away! 
    diff = re.sub(r'<head>', '<head>\n<meta http-equiv=\"refresh\" content=\"4\"/> ', diff)

    if debug:
        f.write('diff='+diff)
        f.close()

    output.write(diff)
    output.close()

    if last:
        for res in results:
            if res['_raw']:
                res['_raw'] = re.sub(r'^.*\n','',res['_raw'])
        splunk.Intersplunk.outputResults(results)
    else:
        splunk.Intersplunk.outputResults(results)

    # splunk.Intersplunk.outputResults(results)

except Exception, e:
    splunk.Intersplunk.generateErrorResults("Unhandled exception:  %s" % (e,))
