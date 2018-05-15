# TouchDesigner Dominant Color  
An approach for finding dominant color in an image using KMeans clustering with scikit learn and openCV. The approach here is built for realtime applications using TouchDesigner and python multi-threading.

## Contributing Programers / Artists ##
**Matthew Ragan** | [ matthewragan.com](http://matthewragan.com)  

## TouchDesigner Version
099  
Build 2018.22800

## Python Dependencies
* numpy
* scipy
* sklearn 
* cv2

## Overview
![base_dominant_color](https://raw.githubusercontent.com/raganmd/touchdesigner-dominant-color/master/img-lib/op-view.PNG)

A tool for finding Dominant Color with openCV.

Here we find an attempt at locating dominant colors from a source image with openCV and KMeans clustering. The large idea is to sample colors from a source image build averages from clustered samples and return a best estimation of dominant color. While this works well, it's not perfect, and in this class you'll find a number of helper methods to resolve some of the shortcomings of this process. 

Procedurally, you'll find that that the process starts by saving out a small resolution version of the sampled file. This is then hadned over to openCV
for some preliminary analysis before being again handed over to sklearn (sci-kit learn) for the KMeans portion of the process. While there is a built-in
function for KMeans sorting in openCV the sklearn method is a little less cumbersome and has better reference documentation for building functionality. After the clustering process each resulting sample is processed to find its luminance. Luminance values outside of the set bounds are discarded before assembling a final array of pixel values to be used. 

It's worth noting that this method relies on a number of additional python libraries. These can all be pip installed, and the recomended build appraoch here would be to use Python35. In the developers experience this produces the least number of errors and issues - and boy did the developer stumble along the way here.

Other considerations you'll find below are that this extension supports a multi-threaded approach to finding results. 

## Parameters
**Dominant Color**  
* **Image Process Status** - (string) The thread process status.  
* **Temp Image Cache** - (folder) A directory location for a temp image file.  
* **Source Image** - (TouchDesigner TOP) A TOP (still) used for color analysis.  
* **Clusters** - (int) The number of requested clusters.  
* **Luminance Bounds** - (int, tuple) Luminance bounds, mine and max expressed as value between 0 and 1.   
* **Clusters within Bounds** - (int) The number of clusters within the Luminance Bounds.   
* **Smooth Ramp** - (toggle) Texture interpolation on output image.   
* **Ramp Width** - (int) Number of pixels in the output Ramp.   
* **Output Image** - (menu) A drop-down menu for selecting a ramp or only the returned clusters.   
* **Find Colors** - (pulse) Issues the command to find dominant colors.   

**Python**  
* **Python Externals** - (path) A path to the directory with python external libraries. 
* **Check Imports** - (pulse) A pulse button to check if sklearn was correctly imported.  

## Using this Module 
To use this module there are a few essential elements to keep in mind.

### Getting Python in Order
If you haven't worked with external Python Libraries inside of Touch yet, please take a moment to familiarize yourself with the process. You can read more about it on the Derivative Wiki - [Importing Modules](https://docs.derivative.ca/index.php?title=Introduction_to_Python_Tutorial#Importing_Modules)

Before you can run this module you'll need to ensure that your Python environment is correctly set-up. I'd recommend that you install Python 3.5+ as that matches the Python installation in Touch. In building out this tool I ran into some wobbly pieces that largely centered around installing sklearn using Python 3.6 - so take it from someone whose already ran into some issues, you'll encounter the fewest challenges / configuration issues if you start there. Sklearn (the primary external library used by this module) requires both scipy and numpy - if you have pip installed the process is straightforward. From a command prompt you can run each of these commands consecutively:  

`pip install numpy`  
`pip install scipy`  
`pip install sklearn`  

Once you've installed the libraries above, you can confirm that they're available in python by invoking python in your command prompt, and then importing the libraries one by one. Testing to make sure you've correctly installed your libraries in a Python only environment first, will help ensure that any debugging you need to do in TouchDesigner is more straightforward.

![python-externals-confirmation]()

### Working with TouchDesigner
#### Python | Importing Modules
If you haven't imported external libraries in TouchDesigner before there's an additional step you'll need to take care of - adding your external site-packages path to TouchDesigner. You can do this with a regular text DAT and by modifying the example below:

```python
import sys
mypath = "C:/Python35/Lib/site-packages/mymodule"
if mypath not in sys.path:
    sys.path.append(mypath)
```
Copy and paste the above into your text DAT, and modify `mypath` to be a string that points do your Python externals site-packages directory.

![python-page-dominant-color]()

If that sounds a little out of your depth, you can use a helper feature on the Dominant Color module. On the `Python` page, navigate to your Python Externals directory. It should likely be a path like: `C:\Program Files\Python35\Lib\site-packages`

Your path may be different, especially if when you installed Python you didn't use the checkbox to install for all users. After navigating to your externals directory, pulse the `Check imports` parameter. If you don't see a pop-up window then `sklearn` was successfully imported. If you do see a pop-up window then something is not quite right, and you'll need to do a bit of leg-work to get your Python pieces in order before you can use the module.

#### Using the Dominant Color
With all of your Python elements in order, you're ready to start using this module. 

![dominant-colors-parameters]()

The process for finding dominant color uses a [KMeans clustering algorithm](https://en.wikipedia.org/wiki/K-means_clustering) for grouping similar values. Luckily we don't need to know all of the statistics that goes into that mechanism in order to take full advantage of the approach, but it is important to know that we need to be mindful a few elements. For this to work efficiently, we'll need to save our image out to an external file. For this to work you need to make sure that this module has a cache for saving temporary images. The process will verify that the directory you've pointed it to exists before saving out a file, and will create a directory if one doesn't yet exist. That's mostly sanity checking to ensure that you don't have to loose time trying to figure out why your file isn't saving.

Give that this process happens in another thread, it's also important to consider that this functions based on a still image, not on a moving one. While it would be slick to have a fast operation for finding KMeans clusters in video, that's not what this tool does. Instead the assumption here is that you're using a single frame of reference content, not video. You point this module to a target source, by dropping a TOP onto the Source Image parameter.

Next you'll need to define the number of clusters you want to look for. Here the term clusters is akin to what's the target number of dominant colors you're looking to find - the top 3, the top 10, the top 20? It's up to you, but keep in mind that more clusters takes longer to produce a result. You're also likely to want to bound your results with some luminance measure - for example, you probably don't want colors that are too dark, or too light. The luminance bounds parameters are for luminance measures that are normalized as 0 to 1. Clusters within bounds, then, tells you how many clusters were returned from the process that fell within your specified regions. This is, essentially, a way to know how many swatches work within the brightness ranges you've set.

The output ramp from this process can be interpolated and smooth, or Nearest Pixel swatches. You can also choose to output a ramp that's any length. You might, for example, want a gradient that's spread over 100 or 1000 pixels rather than just the discrete samples. You can set the number of output pixels with the ramp width parameter.

On the otherside of that equation, you might just want only the samples that came out of the process. In the Output Image parameter, if you choose `clusters` from the drop down menu you'll get only the valid samples that fell within your specified luminance bounds.

Finally, to run the operation pulse `Find Colors`. As an operational note, this process would normally block / lock-up TouchDesigner. To avoid that unsavory circumstance, this module runs the KMeans clustering process in another thread. It's slightly slower than if it ran in the main thread, but the benefit is that Touch will continue running. You'll notice that `Image Process Status` parameter displays `Processing` while the separate thread is running. Once the result has been returned you'll `Ready` displayed in the parameter. 

## References
* [Dominant Colors with KMeans Clustering](https://buzzrobot.com/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036)  
* [KMeans Python Gist Example](https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e)  
* [openCV and KMeans color clustering](https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/)  
