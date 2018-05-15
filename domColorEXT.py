'''
	matthew ragan | matthewragan.com
'''

import sys
import os
import cv2
import webbrowser
import numpy
import queue
import threading
from sklearn.cluster import KMeans

class DomColor:
	'''
		A tool for finding Dominant Color with openCV.

		Here we find an attempt at locating dominant colors from a source image with openCV
		and KMeans clustering. The large idea is to sample colors from a source image build
		averages from clustered samples and return a best estimation of dominant color. While
		this works well, it's not perfect, and in this class you'll find a number of helper
		methods to resolve some of the shortcomings of this process. 

		Procedurally, you'll find that that the process starts by saving out a small
		resolution version of the sampled file. This is then hadned over to openCV
		for some preliminary analysis before being again handed over to sklearn
		(sci-kit learn) for the KMeans portion of the process. While there is a built-in
		function for KMeans sorting in openCV the sklearn method is a little less cumbersom
		and has better reference documentation for building functionality. After the clustering
		process each resulting sample is processed to find its luminance. Luminance values
		outside of the set bounds are discarded before assembling a final array of pixel values
		to be used. 

		It's worth noting that this method relies on a number of additional python libraries.
		These can all be pip installed, and the recomended build appraoch here would be to
		use Python35. In the developers experience this produces the least number of errors
		and issues - and boy did the developer stumble along the way here.

		Other considerations you'll find below are that this extension supports a multi-threaded
		approach to finding results. 

		python dependencies
		> numpy
		> scipy
		> sklearn
		> cv2

		references
		> https://buzzrobot.com/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036
		> https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e
		> https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

		ToDo
		---------------
		[ ] consider a slightly different approach vs. using a ramp TOP
	'''

	def __init__(self, ext_op):
		
		self.DomColorOp 					= op(ext_op)
		self.Clusters						= op(ext_op).par.Clusters
		self.PythonExternals				= op(ext_op).par.Pythonexternals
		self.TempFolder						= op(ext_op).par.Tempimagecache
		self.RampDAT						= op('ramp1_keys')
		self.SourceImgTOP					= op('null1')
		self.RampHeaders 					= ['pos', 'r', 'g', 'b', 'luminosity', 'a']
		self.LuminList 						= []
		self.ColorsForDAT 					= []
		self.LuminRange 					= (0, 1)

		self.GlslTOP 						= op('glslmulti1')

		self.ExecuteDAT 					= op('execute1')

		self.ColorQ 						= queue.Queue()

		op(ext_op).store('DominantColors', self.ColorQ)

		op(ext_op).par.Imageprocessstatus	= "Standby"
		op('execute1').par.framestart 		= 0

		print("Dominant Color Init")

		return

	def Fill_ramp(self, sorted_colors=None):
		'''
			Fill the target network ramp with dominant colors.

			While this is not a partciularly exciting process, this is an essentail element
			in the resulting process. This clears a table DAT of any results, then first
			normalizes the results, discards vals that are outside of the set luminosity range
			then fills in the target table with the results. This is the last step in the 
			process of finding dominant color
			
			Notes
			---------------
			

			Args
			---------------
			sorted_colors (numpy_array)
			> a list of lists containing the results of the KMeans process. These are
			> used to generate the final pixel values that are returned from this
			> module.

			Returns
			---------------
			none
		'''	
		# clear and setup ramp for new keys
		self.RampDAT.clear()
		self.RampDAT.appendRow(self.RampHeaders)

		# grab bounds parameters
		self.LuminRange 		= (parent().par.Lbounds1.val, parent().par.Lbounds2.val)

		# dummy check
		if sorted_colors == None:
			print("Fill_ramp() failed, missing args" )

		else:		
			# colors clean-up and prep
			for item in enumerate( sorted_colors ):
				# normalize vals
				colors_normalized   = [color_val / 255 for color_val in item[1]]

				# discard vals that are too bright or too dark
				if colors_normalized[-1] < self.LuminRange[0] or colors_normalized[-1] > self.LuminRange[1]:
					pass

				else:
					self.ColorsForDAT.append(colors_normalized)

			# send vals to DAT
			for item in enumerate(self.ColorsForDAT):
				pos                 = item[0] / ( len(self.ColorsForDAT) - 1)

				# add position
				item[1].insert(0, pos)

				# add in alpha val for ramp top
				item[1].append(1)

				self.RampDAT.appendRow(item[1])
			
			self.GlslTOP.par.resolutionw 				= len(self.ColorsForDAT)
			self.DomColorOp.par.Clusterswithinbounds 	= len(self.ColorsForDAT)

		return

	def Process_image(self):
		'''
			The process method called when the "Find Colors" parameter is pulsed.

			The process to retrieve a set of useable colors would normally be a blocking
			operation if implimeted only through Python in Touch. As a result this helper method
			handles gathering and setting the approriate pieces in motion so that the work from this
			process can happen in another thread. That result is not as fast as if it happened
			in the main thread, however it no longer blocks operation with Touch. 

			Importantly, you'll find that this method checks to see if the cache directory
			exists before saving out an image, and will create the director in the case that it
			hasn't yet been set-up. The error handling in this extension may seem overkill, but
			helps to ensure that something fails to run, there are some bread crumbs as to what
			may have gone wrong.

			Args
			---------------
			None

			Returns
			---------------
			None
		'''
		colorImgFilePath 				= "{project}/{temp}/temp_img.jpg".format(project=project.folder, temp=self.TempFolder)
		colorImgDir 					= "{project}/{temp}".format(project=project.folder, temp=self.TempFolder)

		# clear previous results
		self.LuminList 					= []
		self.ColorsForDAT 				= []

		# check to see if the temp directory exists and make it if it's not there
		self.Check_path(colorImgDir)

		# save image to cache
		self.SourceImgTOP.save( colorImgFilePath , async=False )

		# start separate thread
		myThread 						= threading.Thread(	target=self.Process_image_thread_worker, 
															args=(colorImgFilePath, self.Clusters.val, self.ColorQ,))
		myThread.start()

		# turn on execuate DAT to begin watching for results
		self.ExecuteDAT.par.framestart 	= 1

		return
	
	def Check_path(self, colorImgDir):
		'''
			Checks to see if a directory exists.

			While this seems out of place as a helper method, this really comes from an existing
			code snippet to solve this problem. If you've gotten this far, and are reading these
			doc strings - steal this method. Use this helper fucntion in your own work to save
			yourself the hassle of missing directories and filed file writes.
			

			Args
			---------------
			colrImgDir (str):
			> a file path to check for existing

			Returns
			---------------
			none
		'''
		if os.path.isdir(colorImgDir):
			pass
		else:
			os.mkdir(colorImgDir)
		return
		
	def Process_image_thread_worker(self, pathToFile, clusters, myQ):
		'''
			The Process_imamge_thread_worker is the threaded working function.

			A thread safe approach in TouchDesigner requires that functions to do not touch any
			TouchDesigner objects. You'll see below that the method employed could be executed
			outside of the conetext of Touch - the standard for determining if the operation
			will be thread safe. As such into this operation we need to pass the path to the
			file we'll be using, the number of clusters, and the queue object used for 
			data handoff with the main thread. When this method is first called it will 
			set the status of the queue object to "Processing" which is in turn used to display
			if the thread is running. Before the thread exits it will update the queue object
			to hold the returned data from the KMeans process. 

			Currently the appraoch is to sort colors by lumiance before returning an array.
			While that does work, it fails on a few fronts. Another method for sorting should
			be cosidered for future work on this module.

			Args
			---------------
			pathToFile (str):
			> a path to the file used for dominant color analysis

			clusters (int):
			> the number of clusters to use for KMeans clustering

			myQ (queue):
			> a queue object to be used for hanndling data i/o with the working
			thread.

			Returns
			---------------
			none
		'''

		# mark thread as processing
		myQ.put("Processing")

		# open image with openCV
		img 					= cv2.imread(pathToFile, 1)

		# transform image from bgr to rgb
		img 					= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		# reshape the data
		img                     = img.reshape(img.shape[0] * img.shape[1], 3)

		# kmeans process
		kmeans                  = KMeans(n_clusters=clusters)
		kmeans.fit(img)
		colors                  = kmeans.cluster_centers_
		labels                  = kmeans.labels_
		ramp_colors             = colors.astype(int)
		lumin_list              = []
		colors_forDAT           = []

		# calculate and add luminosity to the color
		for color in ramp_colors:
			R = color[0]
			G =	color[1]
			B = color[2]
			luminance 			= math.sqrt((0.299 * (R*R)) + (0.587 * (G*G)) + (0.114 * (B*B)))
			
			lumin_list.append(luminance)

		# add luminosity vals into numpy array
		color_and_lumin         = numpy.insert(ramp_colors, 3, lumin_list, axis=1)
		
		# sort colors based on luminance
		sorted_colors           = sorted(color_and_lumin, key=lambda x: x[3])

		# put array into queue object when process completes
		myQ.put(sorted_colors)

		return
	
	def Queue_examine(self):
		'''
			The Queue examine method is used to asses if the thread_worker is running.

			After starting the process of KMeans analysis in another thread, a DAT Execute
			is enabled, allowing Touch to check each frame for the completion of the task.
			This resembles a kind of callback appraoch, this just serves as a mechanism for
			inspecting the queue object, and updating the parent with a status message.

			Once the thread exists, the resulting vals are pulled form the queue object
			and passed over to fill in the Ramp table to provide the user with
			the resulting colors.

			Args
			---------------
			none

			Returns
			---------------
			none
		'''
		# try and except approach for checking for results
		try:
			
			# retrieve the queue object from straoge and check the values
			myQ 	= self.DomColorOp.fetch('DominantColors')
			values 	= myQ.get_nowait()
			
			# update the Image Process Status par for the parent
			if values == 'Processing':
				op(self.DomColorOp).par.Imageprocessstatus	= "Processing"

			# update status, call Fill_ramp, and turn off the frame start script
			elif values != 'Processing':
				self.Fill_ramp(values)
				op(self.DomColorOp).par.Imageprocessstatus	= "Ready"
				self.ExecuteDAT.par.framestart 	= 0
			
		except:
			pass

		return

	def Import_external_test(self):
		'''
			A helper method to give the user feedback about external libraries.

			This method is used to help ensrue that the external python library has been
			correclty loaded and added to sys.path. This is called by the Check Imports pulse
			button on the parent object, and is largely a helper for the user to track down
			any dependent elements that may not be loading correctly.

			Args
			---------------
			none

			Returns
			---------------
			none
		'''

		importHelp 				= 'http://derivative.ca/wiki099/index.php?title=Introduction_to_Python_Tutorial#Importing_Modules'
		messagBoxTitle			= 'Import Failure'
		messageBoxMessage		= '''\r
It looks like something when wrong importing
skLearn. Make sure you've added a path to your 
Python Externals library, and that you've sucessfully
installed sci-kit learn (sklearn) for your version
of Python.
'''
		messageBoxButtons		= ['Get Help', 'Close']
		pythonPath 				= "{}/".format(self.PythonExternals)

		# check to make sure the externals are in sys.path
		if pythonPath not in sys.path:
			sys.path.append(pythonPath)
		else:
			pass

		# check to see if we've imported sklearn yet
		if self.ExternalsImport:
			pass

		else:
			# safe attempts to check for sklearn module
			try:
				from sklearn.cluster import KMeans
				print("Loading sklearn sucessful")

			# warn the user that import failed
			except:
				messageResults = ui.messageBox(	messagBoxTitle, 
												messageBoxMessage, 
												buttons=messageBoxButtons)

				if messageResults:
					pass

				else:
					# launch derivative wiki for help
					webbrowser.open(importHelp)

		return

	def Clean_up(self):
		'''
			Any code clean up process necessary for clean execution.

			Nearly all extensions endup needing some love and care when they're started up
			and when they're shut down. In this case, the queue object can't persist in
			storage. That means that when a project file is saved, or when you quit Touch
			you would typically see an unexpected error message about a potential issue.
			This helper ensures that object's storage is cleaned up - and eliminates
			errors that would otherwise present.
			
			Args
			---------------
			none

			Returns
			---------------
			none
		'''

		# clear out storage 
		self.DomColorOp.unstore('*')
		return