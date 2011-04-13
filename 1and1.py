#!/usr/bin/env python2.6
"""
TODO:
Figure out the cookies and session strings that 1and1 uses, so that it doesn't have to load every page to get to the Domain Update page.
Make this a module for ipcheck.py and pull out all of the configuration variables.
"""
import mechanize

host = 'https://my.1and1.com:443'
url = host + '/xml/config/Login'
domainUrl = host + '/xml/config/DomainOverview'
User = '*********'
Pass = '*********'
br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(url)

br.select_form(nr=0)
br.form['login.User'] = User
br.form['login.Pass'] = Pass

print br.geturl()

br.submit()

#This is a crappy way to do this, but I haven't figured out how the cookies need to be set yet.
#
print br.geturl()
#sessionString = ';' + br.geturl().split(';')[1]
#response = br.open(domainUrl + sessionString)
req = br.click_link(text='1&1 Home Linux')
br.open(req)
print br.geturl()

req = br.click_link(text='Domains')
br.open(req)
print br.geturl()

br.select_form(nr=0)
checkbox = br.find_control(name="domainOverview.DomainIds")
checkbox.value = ["354497579"]

br.submit(name="__SBMT:d0e12845d0:")
#br.click(name="__SBMT:d0e12845d0:")
#x = br.find_control(name="__SBMT:d0e12845d0:")
print br.geturl()

br.select_form(nr=0)


ip0 = br.find_control(name="ipMxUpdate.IP0")
ip1 = br.find_control(name="ipMxUpdate.IP1")
ip2 = br.find_control(name="ipMxUpdate.IP2")
ip3 = br.find_control(name="ipMxUpdate.IP3")

ip0.value = "69"
ip0.value = "208"
ip0.value = "70"
ip0.value = "150"

br.submit(name="__SBMT:d0e9983d0:")
#Confirm submission

br.close()


"""
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

#<POST https://my.1and1.com:443/xml/config/MCCommit;jsessionid=2674F3E3D313C993F8CAE5A0A21530BD.TCpfix10b application/x-www-form-urlencoded
try:

    response = opener.open(url)
    sessionID = ';' + response.geturl().split(';')[1]   

    response = opener.open(urlPost + sessionID, params)
    the_page = response.read()
    response.close()

    print the_page

except Exception, detail:
    print "Err ", detail
 
"""
