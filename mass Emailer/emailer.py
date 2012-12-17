import smtplib
from email.mime.text import MIMEText
import xml.etree.ElementTree as etree
import xml, sys, copy, os, sets, random, subprocess, zipfile
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

gmail_user = "orthoticsStudy@gmail.com"
gmail_pwd = "BigRedTape"
gmail_smtp = "smtp.gmail.com"
gmail_smtp_port = 587

def mail(to, subject, text, attachments):

	# Send an email to email address "to" with subject "subject",
	# body text "text" and an attachment "attach"
	# Code Adapted from http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html

   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))

   for attach in attachements:
       part = MIMEBase('application', 'octet-stream')
       part.set_payload(open(attach, 'rb').read())
       Encoders.encode_base64(part)
       part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
       msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", gmail_smtp_port)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def parseTree(tree):
	
	# Converts an element tree to a set of dictionaries, where each dictionary
	# represents one top level item in the input xml file
	
	out = []
	for el in list(tree.getroot()):
		name = el.find("name").text
		name = name.replace(", DPM", "")
		fax = el.find("fax").text.replace("fax", "").replace("-", "")
		fax = fax.replace("(", "+1").replace(")", "").replace(" ", "")
		zip_code =  el.find("zip_code").text[:5]
		out.append((name,fax,zip_code))

	return out

def selectSample(filename, past_sent):
	
	# Select a weighted sample (by zip-code, with no more than two doctors from
	# the same zip-code)

	tree = etree.ElementTree()
	tree.parse(filename)
	doctors = parseTree(tree)
	sample = []
	zips, faxes = sets.Set(), sets.Set()
	random.seed()
	while ((len(sample) < 23) and (len(doctors)>1)):
		s = random.randint(0, len(doctors) - 1)
		if doctors[s][2] not in zips and (doctors[s][1] not in past_sent):
			zips.add(doctors[s][2])
			sample.append(doctors[s])
			faxes.add(doctors[s][1])
			doctors.remove(doctors[s])

		else: doctors.remove(doctors[s])
	if len(doctors)==1 and (doctors[0][1] not in past_sent):
		sample.append(doctors[0])
		faxes.add(doctors[0][1])
		doctors.remove(doctors[0])
    
	return faxes, sample

def generateAttachment(name, template_copy):
	
	# Replace "SOANDSO" with the doctor's name (the name argument)
	# template_copy is a path to an editable copy of the template

	f = open(template_copy)
	contents = f.readlines()
	contents[1] = contents[1].replace("SOANDSO", name)
	f.close()
	f = open(template_copy, 'w')	
	for l in contents: f.write(l)
	f.close()	

def zipTemplate():

	# Util method that zips the template copy edited by the 
	# generateAttachment method. The archive will be named
	# temp.zip

	archive = zipfile.ZipFile("temp.zip", 'w')
	out = []
	for dirname, dirnames, filenames in os.walk('./temp'):
		for subdirname in dirnames:
			new_path = os.path.join(dirname, subdirname)
			out.append(new_path)
			#archive.write(new_path, new_path.replace("temp/", "")) 
		for filename in filenames:
			new_path = os.path.join(dirname, filename)
			out.append(new_path)
			#archive.write(new_path, new_path.replace("temp/", ""))
	for path in [x for x in out if not ".DS_Store" in x]:
		archive.write(path, path.replace("temp/", ""))

	archive.close()

	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: python emailer.py <database> <path_to_template>" 
		sys.exit(0)
		
	sent = sets.Set()
	if os.path.isfile("./METADATA.txt"):
		f = open("METADATA.txt", 'r')
		for line in f:
			sent.add(line.replace('\n', '').replace(" ", ''))	
		f.close()	

	f = open("METADATA.txt", "a+")
	faxes, sample = selectSample(sys.argv[1], sent)
	for s in sample:
		# Make templates
		subprocess.call("cp -r %s ./temp" % sys.argv[2], shell=True)
		generateAttachment(s[0], "./temp/word/document.xml")
		zipTemplate()	
		subprocess.call("mv ./%s ./survey.docx" % "temp.zip", shell=True )
		
		#Send faxes
		mail(s[1] + "@srfax.com", "Othortics Survey", "", "./survey.docx")
		#mail("orthoticsstudy@gmail.com", "orthotics survey", "", "./survey.docx")
		#Write faxes sent to a "METADATA.txt" file
		f.write(s[1] + "\n")
		#remove the zipped file
		subprocess.call("rm survey.docx", shell=True)
		subprocess.call("rm -r temp", shell=True)

	f.close()
