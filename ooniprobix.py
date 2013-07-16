import wx
import yaml
import os

from yamlreports import *

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

class ProbixMainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent,title=title,size=(800,600))
		
		#TO-DO: Figure out how to handle the sizers for this and the 
		#text field
		self.report_tree = wx.TreeCtrl(self, size=(200, 600))
		self.root = self.report_tree.AddRoot('Report Entries')

		self.report_data = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY)

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
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, self.report_data)	

		self.Show(True)

	def OnAbout(self, e):
		dig = wx.MessageDialog(self, "OONIProbix version " + version_number + " by " + authors + "\n" + "An OONIProbe report GUI, because nobody has time to read through a 50MB YAML file","About OONIProbix", wx.OK)
		dig.ShowModal()
		dig.Destroy()

	def OnExit(self, e):
		self.Close(True)

	def LoadReportTree(self):
		for header in self.yfile.report_headers:
			self.report_tree.AppendItem(self.root, header.keys()[0], data=wx.TreeItemData(header[header.keys()[0]]))

	def OnKeyClick(self,event):
		print 'Value: ' + str(self.report_tree.GetPyData(event.GetItem()))

	def OnOpen(self,e):
		self.dirname = ""
		dig = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.yamloo", wx.OPEN)
		if dig.ShowModal() == wx.ID_OK:
			self.filename = dig.GetFilename()
			self.dirname = dig.GetDirectory()
			self.yfile = YAMLReport(os.path.join(self.dirname,self.filename))
#			self.reportTree.LoadReport(self.yfile)
#			self.report_data.SetValue(f.read())
			f.close()
			self.LoadReportTree()
		dig.Destroy()		

app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
