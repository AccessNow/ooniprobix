import wx
import yaml
import os

from yamlreports import YAMLReport

class ProbixReportWindow(wx.Frame):
    def __init__(self, parent, title,yaml_file):
        wx.Frame.__init__(self,parent,title=title,size=(800,600))
        
        #TO-DO: Figure out how to handle the sizers for this and the 
        #text field
        self.report_tree = wx.TreeCtrl(self,size=(300,600))
        self.report_root = self.report_tree.AddRoot('Report Hierarchy')
        self.header_root = self.report_tree.AppendItem(self.report_root,'Report Headers')
        self.entry_root = self.report_tree.AppendItem(self.report_root,'Report Entries')
        self.report_tree.SetItemHasChildren(self.header_root)
        self.report_tree.SetItemHasChildren(self.entry_root)

        self.report_data = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY, size=(500,600))

        #Let's size this up *badumtish*
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.report_tree,1,wx.EXPAND | wx.ALIGN_LEFT)
        self.sizer.Add(self.report_data,2.75,wx.EXPAND | wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        #TO-DO: Will need for basic logging
        self.CreateStatusBar()

        #Setup for "File" in menu bar
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

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnFilterEntries,menuFilterEntriesOnField)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, self.report_tree)    

        self.Layout()
        self.Show(True)

        self.yfile = YAMLReport(yaml_file)
        self.LoadHeaderTree()
        self.LoadEntryTree()

    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "OONIProbix version " + version_number + " by " + authors + "\n" + "An OONIProbe report GUI, because nobody has time to read through a 50MB YAML file","About OONIProbix", wx.OK)
        dig.ShowModal()
        dig.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnFilterEntries(self,e):
        #TO-DO: Subject this dialog to various and sundry fuzzing tests perhaps?
        filterDialog = wx.TextEntryDialog(None,'Enter field(s) to filter on (comma-separated for multiple fields)','Entry Filter', style=wx.OK | wx.CANCEL)
        if filterDialog.ShowModal() == wx.ID_OK:
            filter = filterDialog.GetValue()
            filterDialog.Destroy()
            report = self.GenerateFilteredEntryList(filter)
            reportDialog = ProbixFilterWindow(self,report)

    #TO-DO: Right now this only filters on fields that are one layer deep
    #Refactor this to recurse into the structure
    def GenerateFilteredEntryList(self,filter_text):
        filtered_list_text = ''
        list_header = self.filename + '\n'
        list_header += filter_text + '\n'
        filtered_list_text += list_header
        filter_text = filter_text.split(',')
        #print 'filter_text: ' + str(filter_text)
        
        #TO-DO: I can almost hear somebody with a databases background telling me that this is inefficient.
        #It's open source, man.  If you have a better idea, hack away.
        for entry in self.yfile.report_entries:
            if entry:
                row_text = ''
                for field in filter_text:
                    try:
                        #If it's the last field we're filtering on, we don't want a comma on the end
                        #TO-DO: Assign entry[field] to a local variable and possibly save a few LOCs
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
            item = self.report_tree.AppendItem(self.header_root, header_key)
            if (type(data) is dict) and len(data) >= 1:
                self.report_tree.SetItemHasChildren(item)
                self.report_tree.SetPyData(item,('nested data',False))
                self.LoadRecursiveDict(item,data)
            else:
                self.report_tree.SetPyData(item,(self.yfile.report_header[header_key],False))
    
    def LoadEntryTree(self):
        for entry in self.yfile.report_entries:
            if entry:
                if entry['input']:
                    item = self.report_tree.AppendItem(self.entry_root,entry['input'])
                else:
                    item = self.report_tree.AppendItem(self.entry_root,'Test Case')                
                self.report_tree.SetPyData(item,('nested data', False))
                self.report_tree.SetItemHasChildren(item)
                #print 'Constructing tree for entry ' + entry['input']
                self.LoadRecursiveDict(item,entry)

    def LoadRecursiveDict(self,parent,child_dict):
        ckeys = child_dict.keys()
        for k in ckeys:
            if (type(child_dict[k]) is list or type(child_dict[k]) is set) and len(child_dict[k]) >= 1:
                i = self.report_tree.AppendItem(parent,k)
                self.report_tree.SetPyData(i,('nested data', False))    
                self.report_tree.SetItemHasChildren(i)
                self.LoadRecursiveCollection(i,child_dict[k])
            elif type(child_dict[k]) is dict and len(child_dict[k]) >= 1:    
                item = self.report_tree.AppendItem(parent,k)
                self.report_tree.SetPyData(item,('nested data', False))
                self.report_tree.SetItemHasChildren(item)
                self.LoadRecursiveDict(item,child_dict[k])
            else:
                i = self.report_tree.AppendItem(parent,k)
                self.report_tree.SetPyData(i,(child_dict[k],False))

    def LoadRecursiveCollection(self,parent,child_clct):
        for datum in child_clct:
            val_type = type(datum)
            if (type(datum) is list or type(datum) is set) and len(datum) >= 1:
                if val_type is not str and val_type is not unicode:
                    val = str(datum)
                i = self.report_tree.AppendItem(parent,'nested data')
                self.report_tree.SetPyData(i,(val, False))    
                self.report_tree.SetItemHasChildren(i)
                self.LoadRecursiveCollection(i,datum)
            elif type(datum) is dict and len(datum) >= 1:    
                #Problem: Collection --> dict without handy key
#                print 'Datum: ' + str(datum)
                if val_type is not str and val_type is not unicode:
                    val = str(datum)
                item = self.report_tree.AppendItem(parent,'nested data')
                self.report_tree.SetPyData(item,(val, False))
                self.report_tree.SetItemHasChildren(item)
                self.LoadRecursiveDict(item,datum)
            else:
                i = self.report_tree.AppendItem(parent,datum)
                self.report_tree.SetPyData(i,(datum,False))


    def OnKeyClick(self,event):
        val = self.report_tree.GetPyData(event.GetItem())[0]
        val_type = type(self.report_tree.GetPyData(event.GetItem())[0])
        
        if val_type is not str and val_type is not unicode:
            val = str(val)
        #Just in case we're dealing with an alphabet not easily represented in ASCII
        #val = unicode(val, 'utf-8')
        self.report_data.ChangeValue(val)


    def OnOpen(self,e):
        self.dirname = ""
        dig = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.yamloo", wx.OPEN)
        if dig.ShowModal() == wx.ID_OK:
            self.filename = dig.GetFilename()
            self.dirname = dig.GetDirectory()
            self.yfile = YAMLReport(os.path.join(self.dirname,self.filename))
            self.LoadHeaderTree()
            self.LoadEntryTree()
        dig.Destroy()        

class ProbixFilterWindow(wx.Frame):
    def __init__(self,parent,text):
        wx.Frame.__init__(self,parent,title='OONIProbix - Filtered Report Data',size=(400,600))
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
#            self.filename = dig.GetFilename()
#            self.dirname = dig.GetDirectory()
#            self.yfile = YAMLReport(os.path.join(self.dirname,self.filename))
#            self.reportTree.LoadReport(self.yfile)
#            self.report_data.SetValue(f.read())
#            f.close()
#            self.LoadHeaderTree()
#            self.LoadEntryTree()
        dlg.Destroy()        
