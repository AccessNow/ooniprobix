import wx
import yaml
import os

authors = "Peter Bourgelais"
version_number = "0.0.1"

class ProbixMainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent,title=title,size=(800,600))

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
	
		self.report_data = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY)
#		self.report_data.SetStyle(wx.TextAttr(wx.T)

		self.Show(True)

	def OnAbout(self, e):
		dig = wx.MessageDialog(self, "OONIProbix version " + version_number + " by " + authors + "\n" + "An OONIProbe report GUI, because nobody has time to read through a 50MB YAML file","About OONIProbix", wx.OK)
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
			f = open(os.path.join(self.dirname,self.filename),'r')
			self.yfile = yaml.safe_load_all(f)
			self.report_data.SetValue(f.read())
			f.close()
		dig.Destroy()		

app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
