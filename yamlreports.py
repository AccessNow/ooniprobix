# Base parser for OONIProbix
# Heavily modified from the example_parser.py script in the OONIProbe repo

# TO-DO: Look at the request headers.  Why they couldn't have stored them as
# dictionaries is beyond me.  Displaying this is a separete problem, but much
# more of a pain now.  
import yaml
import sys
import wx

#print "Opening %s" % sys.argv[1]
#f = open(sys.argv[1])
#yamloo = yaml.safe_load_all(f)

# report_header = yamloo.next()
# for k in report_header:
# 	print k

def walk_dict(dictionary,tabs):
	ks = dictionary.keys()
	for k in ks:
		if type(dictionary[k]) is dict:
			print '\t' * tabs + k
			walk_dict(dictionary[k],tabs+1)
		elif type(dictionary[k]) is list:
			print '\t' * tabs + k
			walk_list(dictionary[k],tabs+1)
		else:
			print '\t' * tabs + k
		

def walk_list(lst,tabs):
	for l in lst:
		if type(l) is dict:
			walk_dict(l,tabs+1)
		elif type(l) is list:
			walk_list(l,tabs+1)
		else:
			pass
			if type(l) is str:
				if len(l) < 50:
					print '\t' * tabs + l
			else:
				print '\t' * tabs + l
				
class YAMLReport():
	def __init__(self, filename):
		f = open(filename,'r')
		yamloo = yaml.safe_load_all(f)
		self.report_header = yamloo.next()
		self.report_entries = []
		for entry in yamloo:
			self.report_entries.append(entry)
		

# for report_entry in yamloo:
# 	ks = report_entry.keys()
# 	print '---'
# 	for k in ks:
# 		if type(report_entry[k]) is dict:
# 			print k
# 			walk_dict(report_entry[k],1)
# 		elif type(report_entry[k]) is list:
# 			print k
# 			walk_list(report_entry[k],1)
# 		else:
# 			print k
# 
# f.close()

# class YAMLReportTree(wx.TreeCtrl):
# 	def __init__(self):
# 		super(YAMLReportTree, self).__init__(*args, **kwargs)
# #		self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
# #		self.Bind(wx.EVT_TREE_ITEM_COLLAPSING,self.OnCollapseItem)
# 		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.OnItemActivated)
# 		self.__collapsing = False
# 
# 
# 	# Given a parent node, enumerate its children, noting whether or not
# 	# those children have child nodes too
# 
# 	# TO-DO: For purposes of this version, a node n "has children" if it is of
# 	# type dict and if len(n) > 0.  We'll handle lists later
# 	# REQUIRE: parent is a dict with at least one key 
# 
# 	def LoadYReport(self,yreport):
# 		#TO-DO: Change this to the name of the test, maybe with timestamp
# 		self.root = self.AddRoot(yreport.report_header['test_name'])
# 		self.SetItemHasChildren(root)
# 
# 		for entry in yreport.report_entries:
# 			tree_entry = self.AppendItem(root,wx.TreeItemData(entry))	
# 			self.SetItemHasChildren(tree_entry,False)
# #			EnumerateChildren(tree_entry,entry)
# 
# 
# 	def EnumerateChildren(self,wx_parent,parent):
# 			parent_keys = parent.keys()
# 			for key in parent_keys:
# 				child = self.AppendItem(self,parent=wx_parent,text=key,data=TreeItemData(parent[key]))
# 				if type(parent[key]) is type(parent[key]) is dict or type(parent[key]) is list or type(parent[key]) is set:
# 					self.SetItemHasChildren(child, len(parent[key]) > 0)
# 				else:
# 					self.SetItemHasChildren(child, False)
# 	
# 	def OnItemActivated(self,event):
# 		thing_to_print = str(self.GetPyData(event.GetItem()))
#                 dig = wx.MessageDialog(self, thing_to_print)
#                 dig.ShowModal()
#                 dig.Destroy()
# 		
# 
# 	def OnExpandItem(self,event):
# 		pass
# 
# 	def OnCollapseItem(self,event):
# 		pass
# #		if self.__collapsing:
# #			event.Veto()
# #		else:
# #			self.__collapsing = True
# #			item = event.GetItem()
# #			self.CollapseAllChildren(item)
# #			self.SetItemHasChildren(item)
# #			self.__collapsing = False

# class YAMLReportTreeFrame(wx.Frame()):
# 	def __init__(self, *args, **kwargs):
# 		super(YAMLReportTreeFrame, self).__init__(*args, **kwargs)
# 		self.__tree = YAMLReportTree(self)
		
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

class YAMLReport():
        def __init__(self, filename):
                f = open(filename,'r')
                yamloo = yaml.safe_load_all(f)
                self.report_name = filename
		self.report_header = yamloo.next()
                self.report_entries = []
                for entry in yamloo:
                        self.report_entries.append(entry)
		f.close()