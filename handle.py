# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
import re
import scihub
import subprocess
import os

mc = {}
retry = 0
#paperdir = '/root/paperBot/papers/' # for paperBot
paperdir = '/root/Weixin/papers/' # for Wexin

def get_paperpath(pdfurl):
    return paperdir+os.path.basename(pdfurl)

def content_process(content, db):
    try:
        return scihub.getpdf(re.search('^paper(.*)',' '.join(content.split()), flags=re.IGNORECASE).group(1), db)
    except:
        return None

def paper_reply(content):
    pdfurl = content_process(content, 'sci-hub.cc')
    if pdfurl == None:
        return 'Error: cannot get paper, please check doi or contact @Hazard!'
    elif os.path.exists(get_paperpath(pdfurl)):
        if os.path.getsize(get_paperpath(pdfurl)):
            return pdfurl
        else:
            try:
                return content_process(content, 'dx.doi.org') # try another db
            except:
                return 'Error: file is null, please contact @Hazard'
    else:
        return pdfurl

class Handle(object):
    def POST(self):
    	global mc, retry
        try:
            webData = web.data()
            print "Handle Post webdata is \n", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                msgId = str(recMsg.MsgId)
                if msgId in mc.keys():
                    retry = retry + 1
                    if retry < 3:
                        subprocess.call(['sleep','5'])
                    else:
                        return reply.TextMsg(toUser, fromUser, mc[msgId]).send()
                else:
                    mc[msgId] = 'Please try later.'
                    retry = 1
                    if re.match('^paper', ' '.join(recMsg.Content.split()), flags=re.IGNORECASE) == None:
                        #itchat.send(tuling123(msg.text), toUserName=msg.fromUserName)
                        content = 'text "paper doi:10.1038/nature17997" to get dowload_url.\nNotice "paper" is necessary!'
                    else:
                        content = paper_reply(' '.join(recMsg.Content.split()))
                        mc[msgId] = content
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    #del mc[msgId]
                    return replyMsg.send()
            else:
                print "bypassing"
                return "success"
        except Exception, Argment:
            return Argment
