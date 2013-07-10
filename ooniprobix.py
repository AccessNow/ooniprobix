import wx

authors = 'Peter Bourgelais'
version_number = '0.0.1'

class ProbixMainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent,title=title,size=(800,600))

		#TO-DO: Will need for basic logging
		self.CreateStatusBar()

		filemenu = wx.Menu()
		filemenu.Append(wx.ID_ABOUT,'&About','OONIProbix version ' + version_number + ' by ' + authors)
		filemenu.AppendSeparator()
		filemenu.Append(wx.ID_EXIT,'&Exit','Exit OONIProbix')
	
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,'&File')
	
		self.SetMenuBar(menuBar)
	
		self.Show(True)



app = wx.App(False)
frame = ProbixMainWindow(None, 'OONIProbix ' + version_number)
app.MainLoop()
