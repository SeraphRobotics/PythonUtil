from distutils.core import setup  
import py2exe  
  
setup(console=[{
        "script":'manipulations.py',
        }],

      options={"py2exe": {
                        
                        "bundle_files":1,

                        }
              }
     ) 
'''
FROM :http://www.py2exe.org/index.cgi/Py2exeAndPyQt 
PyQt4 and image loading (JPG, GIF, etc)

PyQt4 uses plugins to read those image formats, so you'll need to copy the folder PyQt4\plugins\imageformats to <appdir>\imageformats. Like in the above cases, you can use data_files for this. This won't work with bundle_files on.

If the plugins are not reachable, then QPixmap.load/loadFromData will return False when loading an image in those formats.

This will work with bundle_files as well, but you need to exclude the Qt DLLs from bundle (using the dll_excludes option) and add them to the directory with the executable through some other mechanism (such as data_files).
'''

