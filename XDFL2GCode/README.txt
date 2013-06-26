In order to make an executeable for windows follow these steps

1) move msvcp90.dll to the directory
2) run python setup.py py2exe
3) copy PyQt4\plugins\imageformats to dist/imageformats/.
4) add BFB3k.xml, RepRap.xml and Makerbot.xml to dist/Core/.

Afterwards FabConverterGui.exe will then work. 