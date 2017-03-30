# -*- coding: utf-8 -*-
# filename: scihub.py
import urllib
from bs4 import BeautifulSoup
import re
import os
import os.path
import subprocess
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
def sendemail(paperdir, filename, email):
    print 'sendemail - enter'
    msg = MIMEMultipart()
    att1 = MIMEText(open(paperdir+filename, 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename='+filename
    print filename
    msg.attach(att1)

    msg['to'] = email
    msg['from'] = 'wechat.papers@gmail.com'
    msg['subject'] = 'Papers'
    print 'sendemail - start'
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com',465)
        print 'sendemail - 0'
        server_ssl.ehlo()
        #server.starttls()
        print 'sendemail - 1'
        server_ssl.login('wechat.papers@gmail.com','papers111005')
        print 'sendemail - 2'
        server_ssl.sendmail(msg['from'], msg['to'],msg.as_string())
        print 'sendemail - 3'
        server_ssl.close()
        return 'Email Sent!'
    except Exception, e:
        print 'sendemail exception!'
        return str(e)

def retrieve(pdfurl,filename, paperdir, email):
    '''Download data'''
    os.chdir(paperdir)
    print(os.curdir)
    log= open('paper_log.txt','a')
    dlurl = ''
    try:
        if not os.path.exists(paperdir+filename):
            cmd = ['wget',pdfurl,'-O',filename]
            print(cmd)
            status = subprocess.call(cmd)
            if status !=0:
                log.write(time.strftime('%c',time.localtime())+' wget_Failed: '+filename+' '+pdfurl+'\n')
            else:
                log.write(time.strftime('%c',time.localtime())+' wget_Success: '+filename+' '+pdfurl+'\n')
        else:
            log.write(time.strftime('%c',time.localtime())+' wget_Ignore: '+filename+' '+pdfurl+'\n')
        log.flush()
        #if os.path.basename(pdfurl) != filename:
        #    os.rename(os.path.join(paperdir, os.path.basename(pdfurl)), os.path.join(paperdir,filename))
        dlurl = 'http://hellodata.win:3838/papers/' + filename
    except:
        log.write(time.strftime('%c',time.localtime())+' try_Failed: '+filename+' '+pdfurl+'\n')
    log.close()

    if email == '':
        return dlurl
    elif validateEmail(email) == 0:
        return 'Email Address is Unvalid!'
    else:
        return sendemail(paperdir,filename, email)

def getdoi(doi):
    doi = doi.replace(' ','')
    doi = re.sub('doi:', '', doi, flags=re.IGNORECASE)
    doi = re.sub('^doi', '', doi, flags=re.IGNORECASE)
    return doi

def getpdf(content):
    print content
    email = ''
    try:
        content_split = re.search('(.*)email(.*)', content, flags=re.IGNORECASE)
        doi = content_split.group(1)
        email = content_split.group(2).replace(' ','')
    except:
        doi = content
    print email
    doi = getdoi(doi)
    soup = BeautifulSoup(urllib.urlopen('http://sci-hub.cc/'+doi).read(),'lxml')
    try:
        pdfurl = soup.iframe.get('src')
        if re.match('.*\.pdf$', pdfurl, re.IGNORECASE) == None:
            pdfurl = soup.find(attrs={"name":"citation_pdf_url"})['content']
    except:
        try:
            pdfurl = soup.find(attrs={"name":"citation_pdf_url"})['content']
        except:
            return 'Please check your doi!'
    paperdir = '/root/Weixin/papers/'
    filename = os.path.basename(pdfurl)
    if re.match('.*\.pdf$', filename, re.IGNORECASE) == None:
        filename = os.path.basename(doi)+'.pdf'
    
    print pdfurl
    return retrieve(pdfurl, filename, paperdir,email)

#print getpdf('doi: 10.1038/srep36411')
