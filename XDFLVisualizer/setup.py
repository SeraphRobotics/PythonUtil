from distutils.core import setup  
import py2exe  
  
setup(windows=[{
        "script":'FabFileVisualizer.py',
        "icon_resources":[(1,"Main.ico")]
        }],
      data_files = [
            ('imageformats', [
              r'C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll'
              ])],
      zipfile = None,
      options={"py2exe": {
                        "includes": ["sip", "PyQt4.QtGui"],
                        "bundle_files":1,
                        "dll_excludes":["QtCore4.dll","QtGui4.dll"]
                        }
              }
     ) 