ooniprobix
==========

Cross-platform GUI for OONIProbe report analysis


Installation from source, Debian Wheezy
=======================================

OONIProbix has been successfully tested on Debian Wheezy running Python 
After cloning our repo, you can download all the necessary librarires via apt-get 

~~~
sudo apt-get install git
git clone https://github.com/AccessNow/ooniprobix.git
cd ooniprobix
sudo apt-get install libyaml-0-2 python-yaml python-wxgtk2.8

To run the program, type the following:
python ooniprobix.py
~~~


Basic usage
===========

When OONIProbix starts, the main window lets you open a specific 
report file (Under "File") or a directory of report files (see screenshot 
"directory_list.png").  You can double click any of the reports to load 
them in a new window, and clicking a different report will bring it up in 
the same window in a different tab.  


Filtering multiple entries
==========================

If you have a report with a lot of entries in it (e.g. an http_requests/tcp-connect test 
that checks for blocking/resets of multiple sites), select "Filter on field(s)" from the Options menu to generate a report with just 
the values of certain variables in the hierarchy for each entry.  
For example, if we're looking at a large http_requests test report with a 
lot of sites, you can generate a report that lists the URL each entry 
tried to test with the body proportion field for each site by typing in input,report.body_proportion.  
The general syntax is:

top_item1,top_item2,top_item3.sub_a.sub_b

Where sub_a is below top_item 3 in the hierarchy.

Once the report is generated, you can export it to CSV by clicking "Export CSV".


