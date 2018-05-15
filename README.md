# TouchDesigner Dominant Color  
An approach for finding dominant color in an image using KMeans clustering with scikit learn and openCV. The approach here is built for realtime applications using TouchDesigner and python multi-threading.

## Python Dependencies
* numpy
* scipy
* sklearn 
* cv2

## Contributing Programers / Artists ##
**Matthew Ragan** | [ matthewragan.com](http://matthewragan.com)  

## Overview
A tool for finding Dominant Color with openCV.

Here we find an attempt at locating dominant colors from a source image with openCV and KMeans clustering. The large idea is to sample colors from a source image build averages from clustered samples and return a best estimation of dominant color. While this works well, it's not perfect, and in this class you'll find a number of helper methods to resolve some of the shortcomings of this process. 

Procedurally, you'll find that that the process starts by saving out a small resolution version of the sampled file. This is then hadned over to openCV
for some preliminary analysis before being again handed over to sklearn (sci-kit learn) for the KMeans portion of the process. While there is a built-in
function for KMeans sorting in openCV the sklearn method is a little less cumbersom and has better reference documentation for building functionality. After the clustering process each resulting sample is processed to find its luminance. Luminance values outside of the set bounds are discarded before assembling a final array of pixel values to be used. 

It's worth noting that this method relies on a number of additional python libraries. These can all be pip installed, and the recomended build appraoch here would be to use Python35. In the developers experience this produces the least number of errors and issues - and boy did the developer stumble along the way here.

Other considerations you'll find below are that this extension supports a multi-threaded approach to finding results. 

## Using this Module 


## Paratmeters
**Dominant Color**  
Image Process Status - (string) The thread process status.  
Temp Image Cache - (folder) A directory location for a temp image file.  
Source Image - (TouchDesigner TOP) A TOP (still) used for color analysis.  
Clusters - (int) The number of requested cluseters.  
Luminance Bounds - (int, tuple) Luminance bounds, mine and max expressed as value between 0 and 1.   
Clusters within Bounds - (int) The number of clusters within the Lumiance Bounds.   
Smooth Ramp - (toggle) Texture interpolation on output image.   
Ramp Width - (int) Number of pixels in the output Ramp.   
Output Image - (menu) A drop-down menue for selecting a ramp or only the returned clusters.   
Find Colors - (pulse) Issues the command to find dominant colors.   

**Python**  
Python Externals - (path) A path to the directory with python external libraries. 
Check Imports - (pulse) A pulse button to check if sclearn was correclty imported.  

## References
* [Dominant Colors with KMeans Clustering](https://buzzrobot.com/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036)  
* [KMeans Python Gist Example](https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e)  
* [openCV and KMeans color clustering](https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/)  
