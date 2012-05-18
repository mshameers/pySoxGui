import gtk,os,commands,string


COMMON_SOUND_FILES = "*.mp3;*.ogg;*.mp4;*.vorbix;*.vox;*.raw;*.wav"
HEADERLESS_SOUND_LIST = ['raw','wav']
TEMP_PATH = "/tmp/out.ogg"
 


class MainWindow:       
	def __init__(self):
		self.mainbuilder = gtk.Builder()
		self.mainbuilder.add_from_file("pySoxGui.glade")
		self.soxwin = self.mainbuilder.get_object("pysoxwindow")
		self.vbox = self.mainbuilder.get_object("invbox")
		connectDic = {"on_window_destroy" : gtk.main_quit,"on_openFileAction_activate":self.menuOpenfile,"on_show_editWin_toggled":self.settings,
						"on_ginspin_value_changed":self.effOk, "on_goutspin_value_changed":self.effOk , "on_decayspin_value_changed":self.effOk,"on_delayspin_value_changed":self.effOk}					
		self.mainbuilder.connect_signals(connectDic)
		
		self.echo = {"ginspin":0,"goutspin":0,"decayspin":0,"delayspin":0}
		
		self.soxwin.show()
		#self.window.maximize()
	
	def menuOpenfile(self,widget):
		self.infileChooser = gtk.FileChooserDialog(title="OpenFile...", parent=None, action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=( gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT), backend=None)
		self.fileFilFun(self.infileChooser,"Common Sound Files",COMMON_SOUND_FILES)
		self.fileFilFun(self.infileChooser,"All Files","*")
		response=self.infileChooser.run()
		if response == gtk.RESPONSE_OK:
			bufferbuilder = gtk.Builder()
			bufferbuilder.add_from_file("inWing.glade")
			#inWin = bufferbuilder.get_object("hbox1")
			#self.vbox.pack_start(inWin,False)
			print self.infileInfo()
			#label = self.infileInfo()[1] + ' ('  + str(self.infileInfo()[0]) +'mins)'
			inWin = inWindow(self.mainbuilder,self.vbox,self.infileInfo())#,label)
			self.soxwin.show_all()			
		self.infileChooser.destroy()
		
	def fileFilFun(self,forFile,fileTitle,filePattern):
		fileFil = gtk.FileFilter()
		fileFil.set_name(fileTitle);
		patterns = filePattern.split(";")
		for i in patterns:
			fileFil.add_pattern(i)
		forFile.add_filter(fileFil)
		
	def infileInfo(self):
		infileLabel = self.infileChooser.get_filename().split('/')[-1]
		if ' ' in self.infileChooser.get_filename():
			self.infilename = string.replace(self.infileChooser.get_filename(), ' ', '\ ')
		else:
			self.infilename = self.infileChooser.get_filename()
		self.infileDetails = commands.getoutput('soxi '+self.infilename).split()
		dur = self.infileDetails[self.infileDetails.index('Duration')+2].split(':')
		duration = str(int(dur[0])*60+int(dur[1]))+'.'+str(float(dur[2])+0.5).split('.')[0]
		self.infileDursec = int(dur[0])*60*60+int(dur[1])*60+int(dur[2].split('.')[1])
		return self.infilename,float(duration),infileLabel
	def settings(self,widget):
		editvbox = self.mainbuilder.get_object("editvbox")
		edit_frame = self.mainbuilder.get_object("edit_frame")
		show_editWin = self.mainbuilder.get_object("show_editWin")
		if show_editWin.get_active():
			editvbox.reorder_child(edit_frame, 1)
		else:
			editvbox.reorder_child(edit_frame, 0)
	def effOk(self,widget):
		print gtk.Buildable.get_name(widget)
		
		self.echo[gtk.Buildable.get_name(widget)] = widget.get_text()
		self.echoCommand = 'echo '+str(self.echo["ginspin"])+' '+str(self.echo["goutspin"])+' '+str(self.echo["decayspin"])+' '+str(self.echo["delayspin"])
		print self.echoCommand
			
if __name__ == "__main__":
	window = MainWindow()
	gtk.main()
