from yamlreports import YAMLReport
from probix_helpers import *

authors = "Peter Bourgelais"
version_number = "0.0.4"

class ProbixMainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(500,300))

        self.report_tree = wx.TreeCtrl(self,size=(500,300))
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
        dd = wx.DirDialog(None, "Select directory to open", "~/", 0, (10, 10), wx.Size(400, 300))
        if dd.ShowModal() == wx.ID_OK:
            self.working_directory = dd.GetPath()            
        dd.Destroy()
        self.GenerateReportTree(self.working_directory)
        
    def GenerateReportTree(self,directory):
        flist = []
        for file in os.listdir(directory):
            if file.endswith(".yamloo"):
                flist.append(file)
        #print os.listdir(directory)
        if len(flist) > 0:
            #print flist
            self.report_root = self.report_tree.AddRoot('OONIProbe Report List')
            for report in flist:
                #print report
                report_id = self.report_tree.AppendItem(self.report_root,report)
                self.report_tree.SetPyData(report_id,report)
        
    def OnKeyClick(self,e):
        val = os.path.join(self.working_directory,self.report_tree.GetPyData(e.GetItem()))
        ProbixReportWindow(None,"OONIProbix " + version_number,val)



app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
