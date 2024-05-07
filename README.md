## Instructions

`cd DIRECTORY_WITH_APP1.py`


`python -u app1.py -txr Texture -img IMAGES -tmp TEMPLATES`

where 

  `txr` is the flag denoting the path to the page textures/background images for the documents 

  `img` refers to the path of the images folder to be used while adding pictures in the documents 
  
  `tmp` refers to the path of folder where templates for automation are stored.


All these paths are relative paths wrt to the current working directory.

`TEMPLATES`  folder gets created if it is not already present in the current directory while you `Add Template`.
However, during automation, you must provide with the `TEMPLATES` folder's relative location.



