<div align="center">
  <img src="https://i.ibb.co/nM80Bcp/yuri-logo.png" alt="yuri-logo">
</div>

 -----------------
 
 
**yuri** is a program designed to take your image, and analyze it to find whatever is in it, and its colour. It accomplishes this by using the Mask-RCNN object detection method. Mask-RCNN outputs a mask, an image's location, and it's label. The mask (a 4D array) is then sent to a function which uses the KMeans method to determine the most prominent color in the mask. This is used to determine the name of the color.

This program is implemented as a Flask server. Each object detection process is run asynchronously so as to support multiple object detection jobs at a time. 


## Usage Instructions
**yuri** is designed with ease of use in mind. There are a few steps to running yuri on your system.
**NOTE: yuri requires a relatively powerful CPU or GPU to work. In addition, it requires at least 8 GB of RAM to function.**

1. Install dependencies
  The dependencies are listed in `requirements.txt`. Install them, and there shouldn't be any issue.
2. Configure based on preferred computation target.
  **yuri** is preconfigured for use with the CPU. If you want to use the GPU to do the computation, change the line in `src/mask_rcnn.py`
    ``` python
    self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    ```
    to
    ``` python
    self.net.setPreferableTarget(cv.dnn.DNN_TARGET_OPENCL)
    ```
3. Launch Flask server
  Launch a terminal, and in the yuri folder, run `python src/controller.py`.
  This will start a Flask server that you can view at `localhost:5000`. You may change the host by navigating to `controller.py`, line 105 and in `app.run()`, adding an optional parameter `host=255.255.255.255`.

4. Using **yuri**
  Once you have navigated to the website, you can click on the "Drop file here" box, and select an image or video. Modifying the two dropdown menus will allow you to select what objects are detected by yuri. Finally, pressing "Upload" will launch the object detection process in an Async thread. When the process is complete, you will be redirected to the resulting image.


Example:
<div align='center'>
  <img src="https://i.ibb.co/JpzFd1Y/25691390-f9944f61b5-z.jpg" alt="25691390-f9944f61b5-z" border="0">
  <img src="https://i.ibb.co/pKnLXWk/a544e6ed-bc76-4ae7-b865-949c2ae1ce2c-predicted.jpg" alt="a544e6ed-bc76-4ae7-b865-949c2ae1ce2c-predicted" border="0">
</div>


### Authors

  * **David Gurevich** - *Team Lead/Machine Learning Engineer*
  * **Kenan Liu** - *Back-end Software Engineer*
  * **AJ Heft** - *Project Manager*
  * **Daniel Madan** - *Web Developer*

### License

This project is licensed under the GNU Lesser General Public License v3.0
