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
~~~


Basic usage
===========

When you first run python ooniprobix.py, the main window lets you open a specific 
report file (Under "File") or a directory of report files (see screenshot 
"directory_list.png").  You can double click any of the reports to load 
them in a new window, and clicking a different report will bring it up in 
the same window in a different tab.  OONIProbix works through the report and 
constructs a nested hierarchy, which you can browse like in report_window.png.  
If you have a report with a lot of entries in it (e.g. an http_requests/tcp-connect test 
that checks for blocking/resets of multiple sites), you can go to 
Options and select "Filter on field(s)" and generate a report with just 
specific values of certain variables in the hierarchy for each entry.  
For example, if we're looking at a large http_requests test report with a 
lot of sites, you can generate a report that lists the URL each entry 
tried to test with the body proportion (a basic metric to determine if 
censorship is occurring, the documentation says that body_proportion < 0.8 
usually means censorship has occurred) by typing in input,report.body_proportion.  
The general syntax is:

top_item1,top_item2,top_item3.sub_a.sub_b

Where sub_a is below top_item 3 in the hierarchy.

Once the report is generated, you can export it to CSV by clicking "Export CSV", as shown in filter_report_data.png

I know that what I have in terms of extracting relevant data is pretty basic, and I'm up for any changes you want to make, but keep in mind that this is part of a solution to a problem that hasn't completely formed yet.  Access is one of the first organizations trying to collect OONIProbe reports on a massive scale, and I think a lot of the most important features will come from Access' and others' future work on Network Interference.
