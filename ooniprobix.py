from yamlreports import YAMLReport
from probix_helpers import *

authors = "Peter Bourgelais"
version_number = "0.0.4"

class ProbixMainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(600,300))

        self.report_tree = wx.TreeCtrl(self,size=(500,300))
        self.fileMenu = wx.Menu()
        self.optionsMenu = wx.Menu()

        self.menuAbout = self.fileMenu.Append(wx.ID_ABOUT,"&About","About OONIProbix")
        self.menuOpen = self.fileMenu.Append(wx.ID_ANY,"&Open Directory","Select a directory of OONIProbe reports")
        self.menuOpenFile = self.fileMenu.Append(wx.ID_ANY,"&Open File", "Open a specific OONIProbe report")

        self.fileMenu.AppendSeparator()
        self.menuExit = self.fileMenu.Append(wx.ID_EXIT,"&Exit","Exit OONIProbix")

      
        self.filter_sentinel = False
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.fileMenu,"&File")    
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.OnAbout, self.menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, self.menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDirectory, self.menuOpen)
        self.Bind(wx.EVT_MENU, self.OnOpenReport,self.menuOpenFile)

        self.statusBar = self.CreateStatusBar()

        self.report_window = None

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
        self.menuBar.Append(self.optionsMenu,"&Options")
        self.filterOption = wx.Menu()
        self.optionsMenu.AppendMenu(wx.ID_ANY,"Filter by Test Name",self.filterOption)
        self.GenerateReportTree(self.working_directory,'')
        
    def GenerateReportTree(self,directory,filterTest):
        #Reset the directory if it already exists
        if self.report_tree.ItemHasChildren(self.report_tree.GetRootItem()):
            self.report_tree.DeleteAllItems()
            
        flist = []
        for file in os.listdir(directory):
            if file.endswith(".yamloo"):
                flist.append(file)
        if len(filterTest) > 0:
            flist = filter(lambda s: s.find(filterTest.split('/')[1]) > -1,flist)
            if len(flist) > 0:
                self.report_root = self.report_tree.AddRoot('OONIProbe Report List')
                for report in flist:
                    report_id = self.report_tree.AppendItem(self.report_root,report)
                    self.report_tree.SetPyData(report_id,report)

        else:
#		self.filterOption.Enable(True)
                self.report_root = self.report_tree.AddRoot('OONIProbe Report List')
                if len(flist) > 0:
                    for report in flist:
                        report_id = self.report_tree.AppendItem(self.report_root,report)
                        self.report_tree.SetPyData(report_id,report)		
                if self.filter_sentinel == False:
                    self.GenerateFilterList(flist)
                    self.filter_sentinel = True
        self.report_tree.ExpandAll()

    def OnOpenReport(self,e):
        fd = wx.FileDialog(self, "Select report to open", "", "", "YAML files (*.yamloo)|*.yamloo", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fd.ShowModal() == wx.ID_OK:
            self.statusBar.SetStatusText('Loading...')
            if self.report_window:
#               self.report_window.AddPage(ProbixReportWindow(self,os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number,fd.GetPath()), os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number)
                self.report_window.AddReport(fd.GetPath())
            else:
                self.report_window=ProbixMainFrame(self,fd.GetPath())
#            ProbixMainFrame(None,os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number,fd.GetPath())
            self.statusBar.SetStatusText('')		
	    fd.Destroy()
	
    def GenerateFilterList(self,fileList):
        count = len(fileList)
        for test in test_catalog:
            lst = filter(lambda s: s.find(test.split('/')[1]) > -1,fileList)
            count = count - len(lst)
            if len(lst) > 0:
                option = self.filterOption.Append(wx.ID_ANY,"&" + test,"")
                self.Bind(wx.EVT_MENU,lambda evt, txt=test: self.OnFilterByTestName(evt,txt),option)
            if count == 0:
                return		

    def OnFilterByTestName(self,e,testName):
        self.GenerateReportTree(self.working_directory,testName)
        self.report_tree.ExpandAll()
	
    def OnKeyClick(self,e):
        val = os.path.join(self.working_directory,self.report_tree.GetPyData(e.GetItem()))
        self.statusBar.SetStatusText('Loading...')
#        ProbixReportWindow(None,"OONIProbix " + version_number,val)
        if self.report_window:
#               self.report_window.AddPage(ProbixReportWindow(self,os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number,fd.GetPath()), os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number)
            self.report_window.AddReport(val)
            self.statusBar.SetStatusText('')
        else:
            self.report_window=ProbixMainFrame(self,val)
#            ProbixMainFrame(None,os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number,fd.GetPath())
            self.statusBar.SetStatusText('')        

        self.statusBar.SetStatusText('')		

app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
