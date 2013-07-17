import wx
import yaml
import os

#from yamlreports import *

authors = "Peter Bourgelais"
version_number = "0.0.2"

class YAMLReport():
        def __init__(self, filename):
                f = open(filename,'r')
                yamloo = yaml.safe_load_all(f)
                self.report_header = yamloo.next()
                self.report_entries = []
                for entry in yamloo:
                        self.report_entries.append(entry)
		f.close()

#        def LoadYReport(self,yreport):
#                #TO-DO: Change this to the name of the test, maybe with timestamp
#                self.root = self.AddRoot(yreport.report_header['test_name'])
#                self.SetItemHasChildren(root)
#
#                for entry in yreport.report_entries:
#                        tree_entry = self.AppendItem(root,wx.TreeItemData(entry))
#			self.report_tree.SetPyData(tree_entry,(self.yfile.report_header[header_key],False))
#                        self.SetItemHasChildren(tree_entry,False)
#                       EnumerateChildren(tree_entry,entry)


#        def EnumerateChildren(self,wx_parent,parent):
#                        parent_keys = parent.keys()
#                        for key in parent_keys:
#                                child = self.AppendItem(self,parent=wx_parent,text=key)
				
#                                if type(parent[key]) is type(parent[key]) is dict or type(parent[key]) is list $
#                                        self.SetItemHasChildren(child, len(parent[key]) > 0)
#                                else:
#                                        self.SetItemHasChildren(child, False)


class ProbixMainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent,title=title,size=(800,600))
		
		#TO-DO: Figure out how to handle the sizers for this and the 
		#text field
		self.report_tree = wx.TreeCtrl(self)
		self.report_root = self.report_tree.AddRoot('Report Hierarchy')
		self.header_root = self.report_tree.AppendItem(self.report_root,'Report Headers')
		self.entry_root = self.report_tree.AppendItem(self.report_root,'Report Entries')
		self.report_tree.SetItemHasChildren(self.header_root)
		self.report_tree.SetItemHasChildren(self.entry_root)

		self.report_data = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY)

		#Let's size this up *badumtish*
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.report_tree,1,wx.EXPAND | wx.ALIGN_LEFT)
		self.sizer.Add(self.report_data,3,wx.EXPAND)
		
		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.Show()

		#TO-DO: Will need for basic logging
		self.CreateStatusBar()

		filemenu = wx.Menu()
		menuAbout = filemenu.Append(wx.ID_ABOUT,"&About","About OONIProbix")
		menuOpen = filemenu.Append(wx.ID_OPEN,"&Open","Open an OONIProbe report")
		filemenu.AppendSeparator()
		menuExit = filemenu.Append(wx.ID_EXIT,"&Exit","Exit OONIProbix")
		
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, self.report_tree)	

		self.Show(True)

	def OnAbout(self, e):
		dig = wx.MessageDialog(self, "OONIProbix version " + version_number + " by " + authors + "\n" + "An OONIProbe report GUI, because nobody has time to read through a 50MB YAML file","About OONIProbix", wx.OK)
		dig.ShowModal()
		dig.Destroy()

	def OnExit(self, e):
		self.Close(True)

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
			item = self.report_tree.AppendItem(self.entry_root,'Test Case')
			self.report_tree.SetPyData(item,('nested data', False))
			self.report_tree.SetItemHasChildren(item)
			self.LoadRecursiveDict(item,entry)

	def LoadRecursiveDict(self,parent,child_dict):
		ckeys = child_dict.keys()
		for k in ckeys:
			i = self.report_tree.AppendItem(parent,k)
			self.report_tree.SetPyData(i,(child_dict[k],False))


	def OnKeyClick(self,event):
		val = self.report_tree.GetPyData(event.GetItem())[0]
		if type(val) is str:
			self.report_data.SetValue(self.report_tree.GetPyData(event.GetItem())[0])
		else:
			self.report_data.SetValue(str(self.report_tree.GetPyData(event.GetItem())[0]))


	def OnOpen(self,e):
		self.dirname = ""
		dig = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.yamloo", wx.OPEN)
		if dig.ShowModal() == wx.ID_OK:
			self.filename = dig.GetFilename()
			self.dirname = dig.GetDirectory()
			self.yfile = YAMLReport(os.path.join(self.dirname,self.filename))
#			self.reportTree.LoadReport(self.yfile)
#			self.report_data.SetValue(f.read())
#			f.close()
			self.LoadHeaderTree()
			self.LoadEntryTree()
		dig.Destroy()		

app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
