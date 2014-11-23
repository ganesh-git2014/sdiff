### Splunk version of sdiff

### Overview
There are not many components:

1) The custom Splunk sdiff command:

The command uses Python's difflib to generate html, which looks much like a sdiff.

	http://docs.python.org/2/library/difflib.html

The html is over written with the execution of each new search.

2) Web interface:

The form allows a user to easily interact with the sdiff command and all of its 
functions.  While you can use the command in a regular search window, it is not 
especially useful since you cannot see the html!  You *could* open the html directly
in another window and watch it refresh with your searches.

The html is am embedded iframe, which refreshes itself every 4 seconds by defaut.  
You can change this in sdiff.py if you would like it to refresh faster.  


### Dependencies
I've only tested it on Splunk 6.0+.

### Contact
This project was initiated by James Donn
<table>
  <tr>
    <td><em>Email</em></td>
    <td>jim@splunk.com</td>
  </tr>
</table>
