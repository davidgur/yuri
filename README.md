<div align="center">
  <img src="https://i.ibb.co/nM80Bcp/yuri-logo.png" alt="yuri-logo">
</div>

 -----------------
 
 
**yuri** is a program designed to take your image, and analyze it to find whatever is in it, and its colour. It accomplishes this by using the Mask-RCNN object detection method. Mask-RCNN outputs a mask, an image's location, and it's label. The mask (a 4D array) is then sent to a function which uses the KMeans method to determine the most prominent color in the mask. This is used to determine the name of the color.

This program is implemented as a Flask server. Each object detection process is run asynchronously so as to support multiple object detection jobs at a time. 


### Authors

  * **David Gurevich** - *Team Lead/Machine Learning Engineer*
  * **Kenan Liu** - *Back-end Software Engineer*
  * **AJ Heft** - *Project Manager*
  * **Daniel Madan** - *Web Developer*

### License

This project is licensed under the GNU Lesser General Public License v3.0
