import imaplib
import email

def connectToMail(username, password):
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(username, password)
	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.

getMailList('(HEADER Subject "Amazon.com order")')

def getMailList(search_string):
	result, data = mail.uid('search', None, search_string) # search and return uids instead
	email_list = data[0].split()
	print len(email_list)
	for i in email_list[len(email_list)-20:]:
	    result, data = mail.uid('fetch', i, '(RFC822)')
	    raw_email = data[0][1]
	    extractFromEmail(raw_email)
	# latest_email_uid = data[0].split()[-1]
	# result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
	# raw_email = data[0][1]

def extractFromEmail(raw_email):
	email_message = email.message_from_string(raw_email)
	 
	print email_message['To']
	 
	print email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>
	 
	print email_message.items() # print all headers
	 
	# note that if you want to get text content (body) and the email contains
	# multiple payloads (plaintext/ html), you must parse each message separately.
	# use something like the following: (taken from a stackoverflow post)
	def get_first_text_block(self, email_message_instance):
	    maintype = email_message_instance.get_content_maintype()
	    if maintype == 'multipart':
	        for part in email_message_instance.get_payload():
	            if part.get_content_maintype() == 'text':
	                return part.get_payload()
	    elif maintype == 'text':
	        return email_message_instance.get_payload()