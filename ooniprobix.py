from yamlreports import YAMLReport
from probix_helpers import *

authors = "Peter Bourgelais"
version_number = "0.0.3"

class ProbixMainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(500,600))

        self.report_tree = wx.TreeCtrl(self,size=(500,600))

        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT,"&About","About OONIProbix")
        menuOpen = filemenu.Append(wx.ID_OPEN,"&Open Directory","Select a directory of OONIProbe reports")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit","Exit OONIProbix")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")    
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDirectory, menuOpen)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, self.report_tree)    
        self.Layout()
        self.Show(True)

    
    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "OONIProbix version " + version_number + " by " + authors + "\n" + "An OONIProbe report GUI, because nobody has time to read through a 50MB YAML file","About OONIProbix", wx.OK)
        dig.ShowModal()
        dig.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnOpenDirectory(self,e):
        print 'Sanity check for OnOpenDirectory'
        
    def OnKeyClick(self,e):
        print 'Sanity check for OnKeyClick'



app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
