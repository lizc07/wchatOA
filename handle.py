# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
import re
import scihub
import subprocess

mc = {}
retry = 0
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
                    mc[msgId] = 'Try again in a few seconds.'
                    retry = 1
                    try:
                        content = scihub.getpdf(re.search('^paper(.*)',' '.join(recMsg.Content.split()), flags=re.IGNORECASE).group(1))
                        mc[msgId] = content
                    except:
                        content = 'texting "paper doi:10.1038/nature17997" to get dowload_url.\nNotice "paper" is necessary!'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    #del mc[msgId]
                    return replyMsg.send()
            else:
                print "bypassing"
                return "success"
        except Exception, Argment:
            return Argment
