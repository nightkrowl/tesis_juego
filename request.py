#!/usr/bin/env python

import urllib2
url="file:///home/ubuntu/Desktop/repositorio/tesis_juego/request/index.html"
data="subject=Alice-subject&addbbcode18=%23444444&addbbcode20=0&helpbox=Close+all+open+bbCode+tags&message=alice-body&poll_title=&add_poll_option_text=&poll_length=&mode=newtopic&sid=5b2e663a3d724cc873053e7ca0f59bd0&f=1&post=Submit"
cookie = {"Cookie" : "phpbb2mysql_data=a%3A2%3A%7Bs%3A11%3A%22autologinid%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22userid%22%3Bs%3A1%3A%223%22%3B%7D"}#creating HTTP Req
req = urllib2.Request(url,data,cookie)

f = urllib2.urlopen(req)
print f.read()