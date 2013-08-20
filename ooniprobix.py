from yamlreports import YAMLReport
from probix_helpers import *

authors = "Peter Bourgelais"
version_number = "0.0.4"

class ProbixMainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(500,300))

        self.report_tree = wx.TreeCtrl(self,size=(500,300))
<<<<<<< HEAD
        self.fileMenu = wx.Menu()
	self.optionsMenu = wx.Menu()

        self.menuAbout = self.fileMenu.Append(wx.ID_ABOUT,"&About","About OONIProbix")
        self.menuOpen = self.fileMenu.Append(wx.ID_OPEN,"&Open Directory","Select a directory of OONIProbe reports")
        self.fileMenu.AppendSeparator()
        self.menuExit = self.fileMenu.Append(wx.ID_EXIT,"&Exit","Exit OONIProbix")

        
	self.filterOption = wx.Menu()
#        self.filterOption.Enable(False)

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.fileMenu,"&File")    
	self.menuBar.Append(self.optionsMenu,"&Options")
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.OnAbout, self.menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, self.menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDirectory, self.menuOpen)
=======
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT,"&About","About OONIProbix")
        menuOpen = filemenu.Append(wx.ID_OPEN,"&Open Directory","Select a directory of OONIProbe reports")
	menuOpenFile = filemenu.Append(wx.ID_OPEN,"&Open File", "Open a specific OONIProbe report")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit","Exit OONIProbix")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")    
        self.SetMenuBar(menuBar)

	self.statusBar = self.CreateStatusBar()

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDirectory, menuOpen)
	self.Bind(wx.EVT_MENU, self.OnOpenReport,menuOpenFile)
>>>>>>> 27034d603323c9e3535d602eda18256020e013a3
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
        self.GenerateReportTree(self.working_directory,'')
        
<<<<<<< HEAD
    def GenerateReportTree(self,directory,filterTest):
        #Reset the directory if it already exists
=======
    def OnOpenReport(self,e):
	fd = wx.FileDialog(self, "Select report to open", "", "", "YAML files (*.yamloo)|*.yamloo", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	if fd.ShowModal() == wx.ID_OK:
		self.statusBar.SetStatusText('Loading...')
	        ProbixReportWindow(None,"OONIProbix " + version_number,fd.GetPath())
		self.statusBar.SetStatusText('')		
	fd.Destroy()
	

    def GenerateReportTree(self,directory):
>>>>>>> 27034d603323c9e3535d602eda18256020e013a3
        if self.report_tree.ItemHasChildren(self.report_tree.GetRootItem()):
            self.report_tree.DeleteAllItems()
            
        flist = []
        for file in os.listdir(directory):
            if file.endswith(".yamloo"):
                flist.append(file)
        #print os.listdir(directory)
	if len(filterTest) > 0:
		print 'Searching for tests with ' + filterTest.split('/')[1]
		flist = filter(lambda s: s.find(filterTest.split('/')[1]) > -1,flist)
		print 'Found tests ' + str(flist)
        if len(flist) > 0:
            #print flist
            self.report_root = self.report_tree.AddRoot('OONIProbe Report List')
            for report in flist:
                #print report
                report_id = self.report_tree.AppendItem(self.report_root,report)
                self.report_tree.SetPyData(report_id,report)
#	    self.filterOption.Enable(True)
	if len(filterTest) == 0:
	    self.GenerateFilterList(flist)
    	    self.optionsMenu.AppendMenu(wx.NewId(),"Filter by Test Name",self.filterOption)
	self.report_tree.ExpandAll()

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
        ProbixReportWindow(None,"OONIProbix " + version_number,val)



app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
