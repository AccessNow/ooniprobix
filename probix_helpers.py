# *****************************************************************************
# *                                                                           *
# * probix_helpers.py                                                         *
# *                                                                           *
# *                                                                           *
# * CONTAINS:                                                                 *
# * - ProbixMainFrame: Where all of the most basic setup and sizing happens.  *
# *   Change this class if you want to change the default dimensions or       *
# *   add to the menu bar                                                     *
# * - ProbixNotebook                                                          *
# *                                                                           *
# *                                                                           *
# *                                                                           *
# *                                                                           *
# * - ProbixReportWindow:                                                     *
# * - ProbixFilterWindow: A dialog window to enter filter strings for reports.*
# *   Also displays filtered data.                                            *
# *                                                                           *
# *                                                                           *
# *****************************************************************************
import wx
import yaml
import os
#import base64
#import binascii
#import time

from yamlreports import YAMLReport

version_number = '0.0.4'
colorize = False


#Full catalog of tests currently supported by ooniprobe.  
#Used to filter out specific types of tests
test_catalog = [ 'blocking/dnsconsistency',
	  'blocking/http_requests',
	  'blocking/tcpconnect',

	  'experimental/chinatrigger',
	  'experimental/dns_injection',
	  'experimental/domclass_collector',
	  'experimental/http_filtering_bypassing',
	  'experimental/http_keyword_filtering',
	  'experimental/http_trix',
	  'experimental/http_uk_mobile_networks',
	  'experimental/keyword_filtering',
	  'experimental/parasitictraceroute',
	  'experimental/script',
	  'experimental/squid',
	  'experimental/tls_handshake',

	  'manipulation/captiveportal',
	  'manipulation/daphne',
	  'manipulation/dnsspoof',
	  'manipulation/http_header_field_manipulation',
	  'manipulation/http_host',
	  'manipulation/http_invalid_request_line',
	  'manipulation/traceroute',

	  'scanning/http_url_list'
	]

#Done to santiize certain types read in from the files.  
#Some character encodings (e.g. the GB2312 Simplified Chinese encoding) throw 
#out all kinds of exceptions without some careful handling.
def unicode_clean(string):
    if type(string) is str:
#         string = string.encode('string-escape')
         #This is a temporary hack for now until I can come up with 
         #something better
         if 'charset=gb2312' in string:
             string = unicode(string,'gb2312', errors='replace')
         else:
             string = string.decode('utf-8', errors='replace')
#         return string.encode('string-escape')
#         string = unicode(string,'utf-8',errors='replace')
         return string
    if type(string) is unicode:
#        try:
#            string.decode('utf-8')
#            return string.decode('utf-8')
#        except UnicodeEncodeError:
#            return string.encode('utf-8',errors='replace')
         return string
    else:
        return str(string)

#A list-based stack that follows along whenever 
#OONIProbix runs through a report to 
#Generate the report hierarchy.
#Used for the drop-down menu when we want to filter on specific fields
class FilterStack():
    def __init__(self):
        self.stk = []

    def key_push(self,k):
        t = type(k)
        if type(t) is not str or type(t) is not unicode:
            self.stk.append(unicode(k))

    def key_pop(self):
        del self.stk[-1]

    def dump_stack(self):
        return self.stk

class ProbixMainFrame(wx.Frame):
    def __init__(self, parent, report):
        wx.Frame.__init__(self, parent, title="OONIProbix", size=(900, 700))
        #print 'Constructing window'

        #Setup for "File" in menu bar
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "About OONIProbix")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", 
                            "Open an OONIProbe report")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", "Exit OONIProbix")	

        #Setup for "Options" in menu bar
        optionsmenu = wx.Menu()
        menuFilterEntriesOnField = optionsmenu.Append(wx.ID_ANY, 
            "&Filter on field(s)", 
            "Filter the entries on a specific field or fields")

        #Setup for the menu bar itself
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(optionsmenu, "&Options")
        self.SetMenuBar(menuBar)

        #TO-DO: Will need for basic logging
        self.CreateStatusBar()

        #Bindings and multi-tab setup
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnFilterEntries, menuFilterEntriesOnField)
        #print 'constructing notebook'
        self.notebook = ProbixNotebook(self, report)
        self.Layout()
        self.Show(True)

    #Adds another tab to the Notebook and loads the given report
    def AddReport(self, r):
    	filename = os.path.basename(r) #TO-DO: If somebody opens a file outside of the current working directory, this should break.
        self.notebook.AddPage(ProbixReportWindow(self.notebook, title=filename, 
            yaml_file=r), text=filename)

    #The same basic About dialog from ooniprobix.py
    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "OONIProbix version " + version_number 
            + " by " + authors + "\n\n" + "An OONIProbe report GUI, because "
            + "nobody has time to read through a 50MB YAML file",
            "About OONIProbix", wx.OK)
        dig.ShowModal()
        dig.Destroy()

    #That's all folks!
    def OnExit(self, e):
        self.Close(True)

    #Opens and individual file		
    def OnOpen(self, e):
        self.dirname = ""
        dig = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.yamloo", wx.OPEN)
        if dig.ShowModal() == wx.ID_OK:
            self.filename = dig.GetFilename()
            self.dirname = dig.GetDirectory()
            #yfile = YAMLReport(os.path.join(self.dirname,self.filename))
            #self.LoadHeaderTree()
            #self.LoadEntryTree()
            self.notebook.AddPage(ProbixReportWindow(self.notebook, 
                                  title=self.filename, 
                                  yaml_file=os.path.join(self.dirname, 
                                                         self.filename)), 
                                  text=self.filename)
#ProbixReportWindow(parent=self, title=self.filename + " - OONIProbix " + version_number,yaml_file=os.path.join(self.dirname,self.filename)),
#text=self.filename + " - OONIProbix " + version_number)
        dig.Destroy()         

    #Brings up the entry filter dialog
    def OnFilterEntries(self, e):
        cboxlst = self.notebook.GetPage(self.notebook.GetSelection()).combo_box_list
        filterDialog = ProbixFilterDialog(self, 'Enter field(s) to filter on (comma-separated for multiple fields)','Entry Filter', cboxlst)
        if filterDialog.ShowModal() == wx.ID_OK:
            filter = filterDialog.GetValue()
            #print 'Value of filter: ' + filter
            filterDialog.Destroy()
            #print 'Type of e: ' + str(e)
            #print 'Type of e.GetSelection(): ' + str(e.GetSelection())
            report = self.notebook.GetPage(self.notebook.GetSelection()).GenerateFilteredEntryList(filter)
            reportDialog = ProbixFilterWindow(self, filter, report)
        

        #--------------[OLD pre-UI/UX enhancement version]-----------------
        #TO-DO: Subject this dialog to various and sundry fuzzing tests perhaps?
#        filterDialog = wx.TextEntryDialog(None, 'Enter field(s) to filter on (comma-separated for multiple fields)','Entry Filter', style = wx.OK | wx.CANCEL)
#        if filterDialog.ShowModal() == wx.ID_OK:
#            filter = filterDialog.GetValue()
#            #print 'Value of filter: ' + filter
#            filterDialog.Destroy()
            #print 'Type of e: ' + str(e)
            #print 'Type of e.GetSelection(): ' + str(e.GetSelection())
#            report = self.notebook.GetPage(self.notebook.GetSelection()).GenerateFilteredEntryList(filter)
#            reportDialog = ProbixFilterWindow(self, filter, report)

#Customized dialog window to handle filtering entries.
#Currently contains just a TextCtrl, ComboBox, and OK/Cancel buttons, but
#may be extended as necessary.
class ProbixFilterDialog(wx.Dialog):
    def __init__(self, parent, caption, title, cboxlst):
#        style = wx.DEFAULT_DIALOG_STYLE
        super(ProbixFilterDialog, self).__init__(parent, -1, title, size=(500,300))
        
        text = wx.StaticText(self, wx.ID_ANY, caption)
        
        self.filter_input = wx.TextCtrl(self, wx.ID_ANY, size=(200,30))

        cbox_choices = ['Select fields to filter']
        cbox_choices.extend(cboxlst)
        self.cbox = wx.ComboBox(self,id = wx.ID_ANY,value=cbox_choices[0], choices=cbox_choices, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)

        sizer = wx.BoxSizer(wx.VERTICAL)
        buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(text)
        sizer.Add(self.filter_input)
        sizer.Add(buttons, wx.RIGHT)
        sizer.Add(self.cbox, wx.LEFT)
        self.SetSizerAndFit(sizer)
       

        self.Bind(wx.EVT_COMBOBOX, self.AddToTextCtrl, self.cbox)


    def GetValue(self):
        return self.filter_input.GetValue()

    def AddToTextCtrl(self, e):
        if len(self.filter_input.GetValue()) > 0:
            self.filter_input.SetValue(self.filter_input.GetValue() + ','  + self.cbox.GetValue())          
        else:
            self.filter_input.SetValue(self.filter_input.GetValue() + self.cbox.GetValue())


#Out multi-tab class injerited from wx.Notebook
class ProbixNotebook(wx.Notebook):
    def __init__(self,parent,report):
        wx.Notebook.__init__(self,parent, id=wx.ID_ANY, style=wx.BK_TOP,
            size=(800,600))
        text = os.path.basename(report) + " - OONIProbix " + version_number
#        print 'Building report window'        
        self.AddPage(ProbixReportWindow(self, text, report), text)

#The part of the program that constructs the nested hierarchy with the data field display.
#Also contains the functionality for filtering on entry fields (e.g. body_proportion/input)
class ProbixReportWindow(wx.Panel):
    def __init__(self, parent, title, yaml_file):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=(750, 550))
        
        #TO-DO: Figure out how to handle the sizers for this and the 
        #text field
        self.report_tree = wx.TreeCtrl(self, size=(295, 550))

        self.report_root = self.report_tree.AddRoot('Report Hierarchy')
        self.header_root = self.report_tree.AppendItem(self.report_root, 'Report Headers')
        self.entry_root = self.report_tree.AppendItem(self.report_root, 'Report Entries')
        self.report_tree.SetItemHasChildren(self.header_root)
        self.report_tree.SetItemHasChildren(self.entry_root)

        self.report_data = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_CHARWRAP, size=(450,550))
#        self.report_data.SetMaxLength(0)

	self.fstk = FilterStack()
        self.combo_box_list = []

        #Let's size this up *badumtish*
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.report_tree, 1, wx.EXPAND | wx.ALIGN_LEFT)
        self.sizer.Add(self.report_data, 2.75, wx.EXPAND | wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Layout()
        self.Show(True)
        #print 'Loading report'
        self.yfile = YAMLReport(yaml_file)
        self.filename = yaml_file
#        start_time = time.clock()
        self.LoadHeaderTree()
        self.LoadEntryTree()
#	end_time = time.clock()
#	print 'Parsing took %g seconds' % (end_time - start_time)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, self.report_tree)	
        self.Bind(wx.EVT_TEXT_MAXLEN, self.MaxLen, self.report_data)

    def MaxLen(self):
        print 'Error!  Text exceeds max TextCtrl size!'

    #given a formatted string of (recursive and non-recursive) fields to 
    #filter on, return a list with the appropriate values for each entry.
    def GenerateFilteredEntryList(self, filter_text):
	#Generate some headers for the filtered report
	#We're looking at the name of the text and the schema used
#        filtered_list_text = ''
        filtered_list_text = []
        list_header = self.filename + ' '
        list_header += filter_text + '\n'
        filtered_list_text.append(list_header)
	
	#We want to separate out what is one level down in the entry structure
	#and what we have to "recurse" to get to

	#Think I need to separate recursive and non-recursive fields
        filter_text = filter_text.split(',')

        for entry in self.yfile.report_entries:
            if entry:
                row_text = ''
                data = entry
                for field in filter_text:
#                    print 'Value of field: ' + field
                    if '.' in field:
                        #print 'With field ' + field
                        flist = field.split('.')
                        #print 'flist: ' + str(flist)
                        for rfield in flist:
                            try:
                                #print 'rfield: ' + rfield
                                if rfield.isdigit():
                                    rfield=int(rfield)
                                data = data[rfield]		
                            except KeyError:
                                if field == filter_text[-1]:
                                    data = 'N/A'
                                    break
                                else:
                                    data = 'N/A'
                                    data += ','
                                    break
                        row_text += unicode(data)
                    else:
                        try:
                            if field == filter_text[-1]:
                                row_text += unicode(entry[field])
                            else:
                                row_text += unicode(entry[field])
                                row_text += ','
                        except KeyError:
                            if field == filter_text[-1]:
                                row_text += 'N/A'
                            else:
                                row_text += 'N/A'
                                row_text += ','
                    print 'Done with field ' + field
	            print 'printing newline'
	        row_text += '\n'
                filtered_list_text.append(row_text)
        return filtered_list_text

    def LoadHeaderTree(self):
        header_keys = self.yfile.report_header.keys()
        for header_key in header_keys:
            data = self.yfile.report_header[header_key]
            item = self.report_tree.AppendItem(self.header_root, unicode_clean(header_key))
            self.AssignColor(item)
            if (type(data) is dict) and len(data) >= 1:
                self.report_tree.SetItemHasChildren(item)
                self.report_tree.SetPyData(item, ('nested data', False))
#                self.fstk.key_push(header_key)
#		self.fstk.dump_stack()
		self.LoadRecursiveDict(item, data)
#		self.fstk.key_pop()
            else:
#                self.fstk.key_push(header_key)
#		self.fstk.dump_stack()
                self.report_tree.SetPyData(item, 
                (unicode_clean(self.yfile.report_header[header_key]), False))
#		self.fstk.key_pop()

    def AssignColor(self, item):
        global colorize
        if colorize:
            self.report_tree.SetItemBackgroundColour(item, 
                                                wx.NamedColour('LIGHT GREY'))
            colorize=False
        else:
            colorize=True

    def FlipColorize(self):
        global colorize
        if colorize:
            colorize=False
        else:
            colorize=True

    def LoadEntryTree(self):
        for entry in self.yfile.report_entries:
            if entry:
                if entry['input']:
                    item = self.report_tree.AppendItem(self.entry_root, 
                           unicode_clean(entry['input']))
                    self.AssignColor(item)
#	            self.fstk.key_push(entry['input'])
                else:
                    item = self.report_tree.AppendItem(self.entry_root,
                        'Test Case')
                    self.AssignColor(item)
#	            self.fstk.key_push('Test Case')
                self.report_tree.SetPyData(item, ('nested data', False))
                self.report_tree.SetItemHasChildren(item)
                #print 'Constructing tree for entry ' + entry['input']
#		self.fstk.dump_stack()
                self.LoadRecursiveDict(item, entry)
#		self.fstk.key_pop()


    def LoadRecursiveDict(self, parent, child_dict):
        ckeys = child_dict.keys()
        for k in ckeys:
            if (type(child_dict[k]) is list or type(child_dict[k]) is set) and len(child_dict[k]) >= 1:
                i = self.report_tree.AppendItem(parent, unicode_clean(k))
                self.AssignColor(i)
                self.report_tree.SetPyData(i, ('nested data', False))    
                self.report_tree.SetItemHasChildren(i)
                self.fstk.key_push(k)
#		self.fstk.dump_stack()
                self.LoadRecursiveCollection(i, child_dict[k])
		self.fstk.key_pop()
            elif type(child_dict[k]) is dict and len(child_dict[k]) >= 1:    
                i = self.report_tree.AppendItem(parent, unicode_clean(k))
                self.AssignColor(i)
                self.report_tree.SetPyData(i, ('nested data', False))
                self.report_tree.SetItemHasChildren(i)
                self.fstk.key_push(k)
#		self.fstk.dump_stack()
                self.LoadRecursiveDict(i, child_dict[k])
		self.fstk.key_pop()
            else:
                i = self.report_tree.AppendItem(parent, unicode_clean(k).encode('unicode-escape'))
                self.AssignColor(i)
                if type(child_dict[k]) is str or type(child_dict[k]) is unicode:
                    self.report_tree.SetPyData(i, (unicode_clean(child_dict[k]), False))
                    self.fstk.key_push(k)
                    try:
                        base_string = '.'.join(self.fstk.dump_stack())
                    except Exception:
                        print 'self.fstk.dump_stack() value: ' + str(self.fstk.dump_stack())
                    if base_string not in self.combo_box_list:
                        self.combo_box_list.append(base_string)

#			self.fstk.dump_stack()
#	                self.report_tree.SetPyData(i,(child_dict[k],False))
                    self.fstk.key_pop()
                else:	
                    self.fstk.key_push(k)

                    base_string = '.'.join(self.fstk.dump_stack())
                    if base_string not in self.combo_box_list:
                        self.combo_box_list.append(base_string)

#			self.fstk.dump_stack()
                    self.report_tree.SetPyData(i, 
                                     (unicode_clean(child_dict[k]), False))
                    self.fstk.key_pop()
        parent = self.report_tree.GetItemParent(i)
        if self.report_tree.GetItemBackgroundColour(i) != self.report_tree.GetItemBackgroundColour(parent):
            self.FlipColorize()
        

    def LoadRecursiveCollection(self, parent, child_clct):
        for datum in child_clct:
            val_type = type(datum)
            if (type(datum) is list or type(datum) is set) and len(datum) >= 1:
	#	if val_type is not str and val_type is not unicode:
                val = unicode_clean(datum)
#		    val = val.encode('unicode-escape')
                i = self.report_tree.AppendItem(parent, str(child_clct.index(datum)))
                self.AssignColor(i)
                self.report_tree.SetPyData(i, (val, False))    
                self.report_tree.SetItemHasChildren(i)
                self.fstk.key_push(str(child_clct.index(datum)))
                self.LoadRecursiveCollection(i, datum)
                self.fstk.key_pop()
            elif type(datum) is dict and len(datum) >= 1:    
                #Problem: Collection --> dict without handy key
#                print 'Datum: ' + str(datum)
#                if val_type is not str and val_type is not unicode:
                val = unicode_clean(datum)
#		    val = val.encode('unicode-escape')
                item = self.report_tree.AppendItem(parent, str(child_clct.index(datum)))
                self.AssignColor(item)
                self.report_tree.SetPyData(item, (val, False))
                self.report_tree.SetItemHasChildren(item)
                self.fstk.key_push(str(child_clct.index(datum)))
                self.LoadRecursiveDict(item, datum)
                self.fstk.key_pop()
            else:
                if type(datum) is str or type(datum) is unicode:
                    i = self.report_tree.AppendItem(parent, 
                        unicode_clean(datum).encode('unicode-escape'))
                    self.AssignColor(i)
                    self.report_tree.SetPyData(i, (unicode_clean(datum), False))	
                else:
                    i = self.report_tree.AppendItem(parent, 
                        unicode_clean(datum).encode('unicode-escape'))
                    self.AssignColor(i)
                    self.report_tree.SetPyData(i, (unicode_clean(datum), False))


    def OnKeyClick(self, event):
        val = self.report_tree.GetPyData(event.GetItem())[0]
#        val_type = type(self.report_tree.GetPyData(event.GetItem())[0])
#        print type(val)
#        try:
#            if val_type is str:
#        val = unicode(val, 'utf-8', errors='replace')
        self.report_data.ChangeValue(val)
#            else:
#                val = unicode(val, 'utf-8', errors='replace')
            #Just in case we're dealing with an alphabet not easily represented in ASCII
#                self.report_data.ChangeValue(val)
#        except Exception as e:
#            print str(e)
#        print val
#        print len(val)

class ProbixFilterWindow(wx.Frame):
    def __init__(self, parent, columns, text):
        self.report_title = os.path.basename(text[0].split(' ')[0])
        self.columns = columns
#        self.entry_model = parent.combo_box_list

        wx.Frame.__init__(self, parent, 
                 title=self.report_title + ' - OONIProbix - Filter Report Data',
                 size=(400,600))
        text.remove(text[0])
        self.rtext=text
#        self.filter_text = wx.TextCtrl(self, 
#                              style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH,
#                              size=(400,500))
        self.filter_text = wx.ListCtrl(self, wx.ID_ANY, style = wx.LC_REPORT,size=(550,350))        
        columns_lst = columns.split(',')
#        print columns_lst
        index = 0

        for column in columns_lst:
            i = columns_lst.index(column)
            self.filter_text.InsertColumn(i,column)
            self.filter_text.SetColumnWidth(i,200)

        for row in text:
            split_row = row.split(',')
            self.filter_text.InsertStringItem(index=index, label = split_row[0])

            if index % 2:
                self.filter_text.SetItemBackgroundColour(index,wx.NamedColour('LIGHT GREY'))

            for datum in split_row:
#                print 'Inserting item ' + datum + ' at index ' + str(split_row.index(datum))
                self.filter_text.SetStringItem(index,split_row.index(datum),datum)
            index += 1

        self.filter_report = text

        #It's called ops_panel because it's where we put the button for various operations we want
        #to perform on the filtered data

        self.ops_panel = wx.Panel(self, wx.ID_ANY)
        self.export_to_csv = wx.Button(self.ops_panel, -1, 
                                       "Export CSV", (0,0))
        self.export_to_csv.Bind(wx.EVT_BUTTON, self.OnExportToCSV)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.filter_text, 10, wx.EXPAND | wx.ALIGN_TOP)
        self.sizer.Add(self.ops_panel, 1, wx.EXPAND | wx.ALIGN_BOTTOM)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
#        self.filter_text.SetValue(text)
        self.Show(True)

    def GenerateCSVString(self):
        csv_string = ''
        csv_string += self.report_title + '\n'
        csv_string += self.columns + '\n'
        for row in self.rtext:
            csv_string += row
        return csv_string

    def OnExportToCSV(self, e):
        dlg = wx.FileDialog(self, "Export to CSV", os.getcwd(), 
                            '', '*.csv', wx.SAVE|wx.OVERWRITE_PROMPT)        
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            f = open(filename, 'w')
            f.write(self.GenerateCSVString())
        dlg.Destroy()        
