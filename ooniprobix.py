# *****************************************************************************
# *                                                                           *
# * ooniprobix.py                                                             *
# * The main script with the initial directory view                           *
# *                                                                           *
# * CONTAINS:                                                                 *
# * -  class ProbixMainWindow:  The window loaded on startup.  Also displays  *
# *    a directory of reports.                                                *
# *                                                                           *
# *****************************************************************************

from yamlreports import YAMLReport
from probix_helpers import *

authors = "Peter Bourgelais"
version_number = "0.0.4"
colorize = True


class ProbixMainWindow(wx.Frame):
    def __init__(self, parent, title):
        #Basic dimensions and instantiations
        wx.Frame.__init__(self, parent, title=title, size=(600,300))

        self.report_tree = wx.TreeCtrl(self, size=(500,300))
        self.fileMenu = wx.Menu()
        self.optionsMenu = wx.Menu()

        #Set up the menu bar
        self.menuAbout = self.fileMenu.Append(wx.ID_ABOUT, "&About", 
            "About OONIProbix")
        self.menuOpen = self.fileMenu.Append(wx.ID_ANY, "&Open Directory", 
        "Select a directory of OONIProbe reports")
        self.menuOpenFile = self.fileMenu.Append(wx.ID_ANY, "&Open File", 
            "Open a specific OONIProbe report")
        self.fileMenu.AppendSeparator()
        self.menuExit = self.fileMenu.Append(wx.ID_EXIT,"&Exit", 
            "Exit OONIProbix")

        #See the documentation in GenerateReportTree for an explanation
        self.filter_sentinel = False

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.fileMenu, "&File")    
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.OnAbout, self.menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, self.menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDirectory, self.menuOpen)
        self.Bind(wx.EVT_MENU, self.OnOpenReport, self.menuOpenFile)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnKeyClick, 
            self.report_tree)    

        self.statusBar = self.CreateStatusBar()

        self.report_window = None

        self.Layout()
        self.Show(True)

    #A simple popup to display the version number and authors.
    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "OONIProbix version " + version_number + 
        " by " + authors + "\n\n" + "An OONIProbe report GUI, because nobody "
        + "has time to read through a 50MB YAML file", "About OONIProbix", 
        wx.OK)
        dig.ShowModal()
        dig.Destroy()

    def OnExit(self, e):
        self.Close(True)

    #Opens a directory of reports for browsing.  Also adds the options menu 
    def OnOpenDirectory(self,e):
        dd = wx.DirDialog(None, "Select directory to open", "~/", 0, (10, 10),
            wx.Size(400, 300))
        if dd.ShowModal() == wx.ID_OK:
            self.working_directory = dd.GetPath()            
            #Added so we don't have two Options menus
            if self.optionsMenu.GetMenuItemCount() < 1:
                self.menuBar.Append(self.optionsMenu, "&Options")
                self.filterOption = wx.Menu()
                self.optionsMenu.AppendMenu(wx.ID_ANY, "Filter by Test Name", 
                    self.filterOption)
            self.GenerateReportTree('')
        dd.Destroy()
    
    #Given a directory, list the reports and figure out which ones are 
    #present so that the user can filter on a specific test name.    
    def GenerateReportTree(self,filterTest):
        global colorize
        #Reset the directory if it already exists
        if self.report_tree.ItemHasChildren(self.report_tree.GetRootItem()):
            print 'Clearing report tree'
            self.report_tree.DeleteAllItems()

        #Find all the .yamloo files in the current working directory
        flist = []
        for file in os.listdir(self.working_directory):
            print 'checking directory'
            if file.endswith(".yamloo"):
                flist.append(file)
                print 'added file ' + file + ' to report hierarchy'

        #If we are trying to display only certain types of tests
        if len(filterTest) > 0:
            #self.filterOption.DeleteAllItems()
            #Filter the tests in the directory by name
            flist = filter(lambda s: s.find(filterTest.split('/')[1]) > -1, 
                flist)
            #If such tests exist in the directory, reconstruct the report list
            #with only those tests.
            print 'in len(filterTest) > 0 if'
            if len(flist) > 0:
                print 'in len(flist) > 0 if'
                self.report_root = self.report_tree.AddRoot('OONIProbe Report List')
                for report in flist:
                    print 'appending report to tree'
                    report_id = self.report_tree.AppendItem(self.report_root, 
                                                                      report)
                    self.report_tree.SetPyData(report_id,report)

        #If we are NOT trying to display only certain types of tests,
        #just load all of them
        else:
#           self.filterOption.Enable(True)
            #self.filterOption.DeleteAllItems()
            print 'in else'
            self.report_root = self.report_tree.AddRoot('OONIProbe Report List')
            if len(flist) > 0:
                print 'in else-->if len(flist) > 0'
                for report in flist:
                    print 'appended item ' + report
                    report_id = self.report_tree.AppendItem(self.report_root, 
                                                                      report)
                    
                    self.report_tree.SetPyData(report_id, report)		
                    if colorize:
                        self.report_tree.SetItemBackgroundColour(report_id,
                                              wx.NamedColour('LIGHT GREY'))
                        colorize=False
                    else:
                        colorize=True                    

        #If we just opened the directory (i.e. there is no test specified to
        #filter on, delete the old Filter by Test Name option (doesn't work yet)
        #and call GenerateFilterList to add the filter options

        #PROBLEM BRO: Well, more than one problem:
     
        #1. If we're just filtering an already opened directory, it doesn't make sense to change the list of tests in the 
        #filter by test name option.
        
        #2. If we open a new directory, the current code block as it is failt to rebuild the filter by test name option.  There's a subproblem here.
        #2a. In the interest of keeping things nice and MVC, it might be a good idea to pass the job of reconstructing the options menu off to a
        #separate method.

        if self.filterOption.GetMenuItemCount() > 0 and len(filterTest) == 0:
            print 'generating filter by test name list'
            self.optionsMenu.DeleteItem(self.filterOption)
            self.filterOption = wx.Menu()
            self.optionsMenu.AppendMenu(wx.ID_ANY, "Filter by Test Name", 
                self.filterOption)

        self.GenerateFilterList(flist, self.filterOption.GetMenuItemCount())
        self.report_tree.ExpandAll()

    #Lets the user select a specific .yamloo file and passes it to 
    #ProbixMainFrame for opening/parsing/analysis.
    def OnOpenReport(self,e):
        fd = wx.FileDialog(self, "Select report to open", "", "", 
            "YAML files (*.yamloo)|*.yamloo", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fd.ShowModal() == wx.ID_OK:
            self.statusBar.SetStatusText('Loading...')
            if self.report_window:
#               self.report_window.AddPage(ProbixReportWindow(self,os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number,fd.GetPath()), os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number)
                self.report_window.AddReport(fd.GetPath())
            else:
                self.report_window=ProbixMainFrame(self, fd.GetPath())
#            ProbixMainFrame(None,os.path.basename(fd.GetPath()) + " - OONIProbix " + version_number,fd.GetPath())
            self.statusBar.SetStatusText('')		
	    fd.Destroy()
	
    #Looks through the list of reports in the directory and searches against 
    #the master list of tests in probix_helpers.py
    #If a given type of report exists, the option to filter out only that 
    #type is added to the "Filter on field(s)" option submenu
    def GenerateFilterList(self,fileList,oldItems):
        if oldItems > 0:
            for item in self.filterOption.GetMenuItems():
                self.filterOption.DestroyItem(item)
#        self.optionsMenu.DestroyItem(self.optionsMenu.FindItemById(self.filterOption.GetMenuId()))
        count = len(fileList)
        for test in test_catalog:
            lst = filter(lambda s: s.find(test.split('/')[1]) > -1, fileList)
            count = count - len(lst)
            if len(lst) > 0:
                option = self.filterOption.Append(wx.ID_ANY, "&" + test, "")
                self.Bind(wx.EVT_MENU,
                lambda evt, txt=test: self.OnFilterByTestName(evt,txt), option)
            if count == 0:
                return		

    #Event handler reconstructs the directory listing so that only the tests 
    #with a name matching testName show in the report hierarchy
    def OnFilterByTestName(self,e,testName):
        self.GenerateReportTree(testName)
        self.report_tree.ExpandAll()
	
    #Load the selected report
    def OnKeyClick(self,e):
        val = os.path.join(self.working_directory, 
            self.report_tree.GetPyData(e.GetItem()))
        self.statusBar.SetStatusText('Loading...')
        if self.report_window:
            self.report_window.AddReport(val)
            self.statusBar.SetStatusText('')
        else:
            self.report_window=ProbixMainFrame(self,val)
            self.statusBar.SetStatusText('')        

        self.statusBar.SetStatusText('')		

app = wx.App(False)
frame = ProbixMainWindow(None, "OONIProbix " + version_number)
app.MainLoop()
