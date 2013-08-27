import wx
import yaml
import os
#import time

from yamlreports import YAMLReport

version_number = '0.0.4'

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

def unicode_clean(string):
	if type(string) is str:
		return unicode(string,'utf-8',errors='replace').encode('unicode-escape')
	if type(string) is unicode:
		return string.encode('unicode-escape')
	else:
		return string


#class FilterStack():
#	def __init__(self):
#		self.stk = []
#
#	def key_push(self,k):
#		self.stk.append(k)
#
#	def key_pop(self):
#		del self.stk[-1]
#
#	def dump_stack(self):
#		print self.stk

class ProbixMainFrame(wx.Frame):
    def __init__(self,parent,report):
        wx.Frame.__init__(self,parent,title="OONIProbix",size=(900,700))

        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT,"&About","About OONIProbix")
        menuOpen = filemenu.Append(wx.ID_OPEN,"&Open","Open an OONIProbe report")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit","Exit OONIProbix")	

        #Setup for "Options in menu bar
        optionsmenu = wx.Menu()
        menuFilterEntriesOnField = optionsmenu.Append(wx.ID_ANY,"&Filter on field(s)","Filter the entries on a specific field or fields")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(optionsmenu,"&Options")
        self.SetMenuBar(menuBar)

        #TO-DO: Will need for basic logging
        self.CreateStatusBar()

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnFilterEntries,menuFilterEntriesOnField)

        self.notebook = ProbixNotebook(self,report)
        self.Layout()
        self.Show(True)

    def AddReport(self,r):
        self.notebook.AddPage(r,self,"Ohioiowaidahohawaii Highway")

        
    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "OONIProbix version " + version_number + " by " + authors + "\n\n" + "An OONIProbe report GUI, because nobody has time to read through a 50MB YAML file","About OONIProbix", wx.OK)
        dig.ShowModal()
        dig.Destroy()

    def OnExit(self, e):
        self.Close(True)
		
    def OnOpen(self,e):
        self.dirname = ""
        dig = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.yamloo", wx.OPEN)
        if dig.ShowModal() == wx.ID_OK:
            self.filename = dig.GetFilename()
            self.dirname = dig.GetDirectory()
            #yfile = YAMLReport(os.path.join(self.dirname,self.filename))
            #self.LoadHeaderTree()
            #self.LoadEntryTree()
            self.notebook.AddPage(ProbixReportWindow(self.notebook,title="Ohioiowaidahohawaii Highway",yaml_file=os.path.join(self.dirname,self.filename)), text="Oklahomaiowaidahohawaii Highway")
#ProbixReportWindow(parent=self, title=self.filename + " - OONIProbix " + version_number,yaml_file=os.path.join(self.dirname,self.filename)),
#text=self.filename + " - OONIProbix " + version_number)
        dig.Destroy()         

    def OnFilterEntries(self,e):
        #TO-DO: Subject this dialog to various and sundry fuzzing tests perhaps?
        filterDialog = wx.TextEntryDialog(None,'Enter field(s) to filter on (comma-separated for multiple fields)','Entry Filter', style=wx.OK | wx.CANCEL)
        if filterDialog.ShowModal() == wx.ID_OK:
            filter = filterDialog.GetValue()
            filterDialog.Destroy()
            report = e.GetSelection().GenerateFilteredEntryList(filter)
            reportDialog = ProbixFilterWindow(self,report)



class ProbixNotebook(wx.Notebook):
    def __init__(self,parent,report):
        wx.Notebook.__init__(self,parent,id=wx.ID_ANY,style=wx.BK_TOP,size=(800,600))
        #Setup for "File" in menu bar
        text = os.path.basename(report) + " - OONIProbix " + version_number
        self.AddPage(ProbixReportWindow(self,text,report),text)

class ProbixReportWindow(wx.Panel):
    def __init__(self, parent, title,yaml_file):
        wx.Panel.__init__(self,parent,id=wx.ID_ANY,size=(750,550))
        
        #TO-DO: Figure out how to handle the sizers for this and the 
        #text field
        self.report_tree = wx.TreeCtrl(self,size=(295,550))

        self.report_root = self.report_tree.AddRoot('Report Hierarchy')
        self.header_root = self.report_tree.AppendItem(self.report_root,'Report Headers')
        self.entry_root = self.report_tree.AppendItem(self.report_root,'Report Entries')
        self.report_tree.SetItemHasChildren(self.header_root)
        self.report_tree.SetItemHasChildren(self.entry_root)

        self.report_data = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY, size=(450,550))

#	self.fstk = FilterStack()

        #Let's size this up *badumtish*
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.report_tree,1,wx.EXPAND | wx.ALIGN_LEFT)
        self.sizer.Add(self.report_data,2.75,wx.EXPAND | wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Layout()
        self.Show(True)

        self.yfile = YAMLReport(yaml_file)
        self.filename = yaml_file
#        start_time = time.clock()
        self.LoadHeaderTree()
        self.LoadEntryTree()
#	end_time = time.clock()
#	print 'Parsing took %g seconds' % (end_time - start_time)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, self.report_tree)	

    #TO-DO: Right now this only filters on fields that are one layer deep
    #Refactor this to recurse into the structure
    def GenerateFilteredEntryList(self,filter_text):
	#Generate some headers for the filtered report
	#We're looking at the name of the text and the schema used
        filtered_list_text = ''
        list_header = self.filename + '\n'
        list_header += filter_text + '\n'
        filtered_list_text += list_header
	
	#We want to separate out what is one level down in the entry structure
	#and what we have to "recurse" to get to

	#Think I need to separate recursive and non-recursive fields
        filter_text = filter_text.split(',')

        for entry in self.yfile.report_entries:
            if entry:
                row_text = ''
                data = entry
                for field in filter_text:
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
                            row_text += str(data)
                    else:
                        try:
                            if field == filter_text[-1]:
                                row_text += str(entry[field])
                            else:
                                row_text += str(entry[field])
                                row_text += ','
                        except KeyError:
                            if field == filter_text[-1]:
                                row_text += 'N/A'
                            else:
                                row_text += 'N/A'
                                row_text += ','
	            row_text += '\n'
                filtered_list_text += row_text
        return filtered_list_text

    def LoadHeaderTree(self):
        header_keys = self.yfile.report_header.keys()
        for header_key in header_keys:
            data = self.yfile.report_header[header_key]
            item = self.report_tree.AppendItem(self.header_root, unicode_clean(header_key))
            if (type(data) is dict) and len(data) >= 1:
                self.report_tree.SetItemHasChildren(item)
                self.report_tree.SetPyData(item,('nested data',False))
#                self.fstk.key_push(header_key)
#		self.fstk.dump_stack()
		self.LoadRecursiveDict(item,data)
#		self.fstk.key_pop()
            else:
#                self.fstk.key_push(header_key)
#		self.fstk.dump_stack()
                self.report_tree.SetPyData(item,(unicode_clean(self.yfile.report_header[header_key]),False))
#		self.fstk.key_pop()

    
    def LoadEntryTree(self):
        for entry in self.yfile.report_entries:
            if entry:
                if entry['input']:
                    item = self.report_tree.AppendItem(self.entry_root,unicode_clean(entry['input']))
#	            self.fstk.key_push(entry['input'])
                else:
                    item = self.report_tree.AppendItem(self.entry_root,'Test Case')                
#	            self.fstk.key_push('Test Case')
                self.report_tree.SetPyData(item,('nested data', False))
                self.report_tree.SetItemHasChildren(item)
                #print 'Constructing tree for entry ' + entry['input']
#		self.fstk.dump_stack()
                self.LoadRecursiveDict(item,entry)
#		self.fstk.key_pop()


    def LoadRecursiveDict(self,parent,child_dict):
        ckeys = child_dict.keys()
        for k in ckeys:
            if (type(child_dict[k]) is list or type(child_dict[k]) is set) and len(child_dict[k]) >= 1:
                i = self.report_tree.AppendItem(parent,unicode_clean(k))
                self.report_tree.SetPyData(i,('nested data', False))    
                self.report_tree.SetItemHasChildren(i)
#                self.fstk.key_push(k)
#		self.fstk.dump_stack()
                self.LoadRecursiveCollection(i,child_dict[k])
#		self.fstk.key_pop()
            elif type(child_dict[k]) is dict and len(child_dict[k]) >= 1:    
                item = self.report_tree.AppendItem(parent,unicode_clean(k))
                self.report_tree.SetPyData(item,('nested data', False))
                self.report_tree.SetItemHasChildren(item)
#                self.fstk.key_push(k)
#		self.fstk.dump_stack()
                self.LoadRecursiveDict(item,child_dict[k])
#		self.fstk.key_pop()
            else:
                i = self.report_tree.AppendItem(parent,unicode_clean(k))
                if type(child_dict[k]) is str or type(child_dict[k]) is unicode:
                    self.report_tree.SetPyData(i,(unicode_clean(child_dict[k]),False))
#	                self.fstk.key_push(k)
#			self.fstk.dump_stack()
#	                self.report_tree.SetPyData(i,(child_dict[k],False))
#			self.fstk.key_pop()
                else:	
#        	        self.fstk.key_push(k)
#			self.fstk.dump_stack()
                    self.report_tree.SetPyData(i,(unicode_clean(child_dict[k]),False))
#			self.fstk.key_pop()

    def LoadRecursiveCollection(self,parent,child_clct):
        for datum in child_clct:
            val_type = type(datum)
            if (type(datum) is list or type(datum) is set) and len(datum) >= 1:
	#	if val_type is not str and val_type is not unicode:
                val = unicode_clean(datum)
#		    val = val.encode('unicode-escape')
                i = self.report_tree.AppendItem(parent,str(child_clct.index(datum)))
                self.report_tree.SetPyData(i,(val, False))    
                self.report_tree.SetItemHasChildren(i)
                self.LoadRecursiveCollection(i,datum)
            elif type(datum) is dict and len(datum) >= 1:    
                #Problem: Collection --> dict without handy key
#                print 'Datum: ' + str(datum)
#                if val_type is not str and val_type is not unicode:
                val = unicode_clean(datum)
#		    val = val.encode('unicode-escape')
                item = self.report_tree.AppendItem(parent,str(child_clct.index(datum)))
                self.report_tree.SetPyData(item,(val, False))
                self.report_tree.SetItemHasChildren(item)
                self.LoadRecursiveDict(item,datum)
            else:
                if type(datum) is str or type(datum) is unicode:
                	i = self.report_tree.AppendItem(parent,unicode_clean(datum))
        	        self.report_tree.SetPyData(i,(unicode_clean(datum),False))	
                else:
                    i = self.report_tree.AppendItem(parent,unicode_clean(datum))
                    self.report_tree.SetPyData(i,(unicode_clean(datum),False))


    def OnKeyClick(self,event):
        val = self.report_tree.GetPyData(event.GetItem())[0]
        val_type = type(self.report_tree.GetPyData(event.GetItem())[0])
#        print val
        if val_type is str:
            val = unicode(val, 'utf-8', errors='replace')
            self.report_data.ChangeValue(val)
        else:
            val = str(val)
            #Just in case we're dealing with an alphabet not easily represented in ASCII
            self.report_data.ChangeValue(val)
       

class ProbixFilterWindow(wx.Frame):
    def __init__(self,parent,text):
        wx.Frame.__init__(self,parent,title='OONIProbix - Filter Report Data',size=(400,600))
        self.filter_text = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY, size=(400,500))
        self.filter_report = text
        #It's called ops_panel because it's where we put the button for various operations we want
        #to perform on the filtered data
        self.ops_panel = wx.Panel(self,wx.ID_ANY)
        self.export_to_csv = wx.Button(self.ops_panel,-1,"Export CSV",(0,0))
        self.export_to_csv.Bind(wx.EVT_BUTTON,self.OnExportToCSV)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.filter_text,10,wx.EXPAND | wx.ALIGN_TOP)
        self.sizer.Add(self.ops_panel,1,wx.EXPAND | wx.ALIGN_BOTTOM)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.filter_text.SetValue(text)
        self.Show(True)


    def OnExportToCSV(self,e):
        dlg = wx.FileDialog(self, "Export to CSV", os.getcwd(),'','*.csv',wx.SAVE|wx.OVERWRITE_PROMPT)        
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            f = open(filename,'w')
            f.write(self.filter_report)
        dlg.Destroy()        
