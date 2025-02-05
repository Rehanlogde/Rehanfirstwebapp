from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import pymysql as db
import qrcode
import pyotp
import smtplib

dbconnection = db.connect(host='localhost', user='root', password='Rehanmysql.com',database='bhai_website1database', port = 3305)

class users :
    def __init__(self, username, age, email, password, gender, fullname):
        self.username = username
        self.age = age
        self.email = email
        self.password = password
        self.gender = gender
        self.fullname = fullname
        self.totp = None
class userauthentication :
    def __init__(self) : 
        self.key = None
        self.totp = None
        self.uri = None
        self.QR = None
    def qr_code_generation_for_super_user(self, firstname,lastname, email, gender, password, username,DOB) : 
        self.key = pyotp.random_base32()
        self.totp = pyotp.TOTP(self.key)
        fullname = firstname + ' ' + lastname
        self.uri = self.totp.provisioning_uri(name= fullname, issuer_name= 'MFA website')
        self.QR = qrcode.make(self.uri)
        self.QR.save("Superuser.png")

        query_for_insertion = query_for_insertion = f"INSERT INTO USERS VALUES ('{firstname}', '{lastname}', '{username}', '{password}', '{email}', '{DOB}','{gender}', '{self.key}', 'superuser')"
        dbcursor = dbconnection.cursor()
        dbcursor.execute(query_for_insertion)
        dbconnection.commit()
    
    def qr_generation_for_new_user(self, fullname) :
        
        self.key = pyotp.random_base32()
        self.totp = pyotp.TOTP(self.key)
        self.uri = self.totp.provisioning_uri(name = fullname,  issuer_name= 'MFA website')
        
        directory = "C:\\Users\\rehan\\bhaiproject\\bhaiwebsite1\\static files\\newuser.png"
        self.QR = qrcode.make(self.uri) 
        self.QR.save(directory)

        newuser_keyfile = open('newuserkeyfile.txt', 'w')
        newuser_keyfile.write(self.key)

    def databaseinputs(self, firstname, lastname, email, DOB, username, password,gender) : 

        file = open('newuserkeyfile.txt', 'r')
        u_mfa_key = file.read()
        query_for_insertion = f"INSERT INTO USERS VALUES ('{firstname}', '{lastname}', '{username}', '{password}', '{email}', '{DOB}','{gender}', '{u_mfa_key}', 'normaluser')"
        dbcursor = dbconnection.cursor()
        dbcursor.execute(query_for_insertion)
        dbconnection.commit()
 
class exchanging : 
    def __init__(self) :
        self.usernameinput = None
        self.user = None
        self.userpassinput = None
    def get1(self,usernameinput) : 
        self.usernameinput = usernameinput
    def get2(self,userpassinput) : 
        self.userpassinput = userpassinput
    def return1(self) : 
        return self.usernameinput
    def return2(self) :
        return self.userpassinput  
    def userexhangeget(self,webuser) : 
        self.user = webuser
    def userexchangereturn(self) : 
        return self.user
    
w = exchanging()
ua = userauthentication()

def home(request) : 
    #ua.qr_code_generation_for_super_user('Rehan', 'logde', 'rehanlogde862@gmail.com', 'male', 'rehan123', 'rehan', '2008-08-10')
    return render(request, 'homepage.html')

def verify(request) : 

    usernameinput = request.GET.get('username', 'invaliduser')
    userpassinput = request.GET.get('password', 'invalidpassword')
    w.get1(usernameinput)
    w.get2(userpassinput)

    websiteuser = authenticate(username = usernameinput, password = userpassinput)
    w.userexhangeget(websiteuser)
    if websiteuser is not None : 
        return render(request, 'check.html')
    
    else : 
        return HttpResponse('<h1>Invalid credentails</h1>')


def userhome(request) : 

    usernameinput = w.return1()
    userpassinput = w.return2()
    usermfa = request.GET.get('userTOTP', 'invalidkey')

    print(usernameinput)
    print(usermfa)
    dbcursor = dbconnection.cursor()
    query_for_searching = f"SELECT user_mfa_key FROM users WHERE username = '{usernameinput}'"
    dbcursor.execute(query_for_searching)
    result = dbcursor.fetchall()
    totp = pyotp.TOTP(result[0][0])
    websiteuser = w.userexchangereturn() #it will return the websiteuser name. ex : rehan

    if websiteuser is not None : 
        if usermfa == totp.now() :    
            login(request, websiteuser)
            DMZ_restriction = request.user.groups.filter(name = 'Restricted_users_to_see_DMZ').exists()
            Hyperconverged_restriction = request.user.groups.filter(name = 'Restricted_users_to_see_hyperconverged_&_server_farm').exists()
            Backup_restriction = request.user.groups.filter(name = 'Restricted_users_to_see_backup_&Disaster_recovery').exists()             
            customizationbuttonpermission = request.user.groups.filter(name= 'customizationbuttontosuperuser').exists()
            databasecusrsor = dbconnection.cursor()
            query = f"SELECT * FROM urls"

            databasecusrsor.execute(query)
            
            urls= databasecusrsor.fetchall()
            
            url1 = urls[0][1]
            url2 = urls[1][1]
            url3 = urls[2][1]
            url4 = urls[3][1]
            url5 = urls[4][1]
            url6 = urls[5][1]
            url7 = urls[6][1]
            url8 = urls[7][1]
            url9 = urls[8][1]
            url10 = urls[9][1]
            url11 = urls[10][1]
            url12 = urls[11][1]
            url13 = urls[12][1]
            url14 = urls[13][1]
            url15 = urls[14][1]
            url16 = urls[15][1]

            parametersdictionary = {
                'username' : usernameinput,
                'customizeoption' : customizationbuttonpermission,
                'dmz_restrict' : DMZ_restriction,
                'hyperconverged_restrict' : Hyperconverged_restriction,
                'backup_restrict' : Backup_restriction,
                'pfurl' : url1, 
                'dfurl' : url2, 
                'dwfurl' : url3,
                'wafurl' : url4, 
                'nacpmurl' : url5, 
                'nacgurl' : url6, 
                'nacourl': url7, 
                'naciurl' : url8, 
                'edresurl' : url9, 
                'pdcurl' : url10, 
                'drdcurl' : url11, 
                'pdpeurl' : url12,
                'pdpcurl': url13, 
                'pra1url' : url14, 
                'pra2url' : url15, 
                'bdrurl' :url16 
            }
            return render(request, 'Mainhomepage.html', parametersdictionary)
        else : 
                return HttpResponse("<h1>Invalid MFA pin</h1>")
    else : 
            return HttpResponse("<h1>Invalid MFA pin</h1>")


def register(request):
    return render(request, 'registration.html')

def registrationresult(request) : 
    firstname = request.GET.get('firstname', 'none')
    lastname = request.GET.get('lastname', 'none')
    usernamein = request.GET.get('username', 'none')
    passwordin = request.GET.get('password', 'none')
    DOB = request.GET.get('DOB', 'none')
    emailin = request.GET.get('emailid', 'none')
    genderM = request.GET.get('malegender','none')
    genderF = request.GET.get('femalegender', 'none')
    genderR = request.GET.get('RNSg', 'none')
    gender = None

    fullname= firstname+' '+lastname
    newuser = User.objects.create_user(username=usernamein, email= emailin, password=passwordin)
    newuser.first_name = firstname
    newuser.last_name = lastname
    newuser.save()

    if genderM == 'on' : 
        gender = 'Male'

    elif genderF == 'on' : 
        gender = 'Female'

    elif genderR == 'on' : 
        gender = 'Rather not say'
    else : 
        gender = None
    
    ua.qr_generation_for_new_user(fullname)
    ua.databaseinputs(firstname, lastname,emailin, DOB, usernamein, passwordin,gender)

    return render(request, 'registrationresult.html')

def loggingout(request) :

    logout(request)

    return HttpResponse('<h1>Logged out !</h1>')

def mfarecovery(request) : 
    websiteuser = w.userexchangereturn()
    username = w.return1()

    queryforemail = f"SELECT email FROM users WHERE username = '{username}'"
    queryforkey = f"SELECT user_mfa_key FROM users WHERE username = '{username}'"
    sender_email = 'rehan17641@gmail.com'
    password = 'ryxcrmjcyoeeltoh'   
    dbcursor = dbconnection.cursor()
    dbcursor.execute(queryforemail)
    emailresult = dbcursor.fetchall()

    dbcursor.execute(queryforkey)
    keyresult = dbcursor.fetchall()
    receiver_email = emailresult[0][0]
    key = keyresult[0][0]

    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.starttls()
    smtpserver.login(sender_email, password)
    smtpserver.sendmail(sender_email, receiver_email, key)

    return render(request, 'mfarecovery.html')

def customize(request) : 
    
    databasecusrsor = dbconnection.cursor()
    query = f"SELECT * FROM urls"

    databasecusrsor.execute(query)
    
    urls= databasecusrsor.fetchall()
    
    url1 = urls[0][1]
    url2 = urls[1][1]
    url3 = urls[2][1]
    url4 = urls[3][1]
    url5 = urls[4][1]
    url6 = urls[5][1]
    url7 = urls[6][1]
    url8 = urls[7][1]
    url9 = urls[8][1]
    url10 = urls[9][1]
    url11 = urls[10][1]
    url12 = urls[11][1]
    url13 = urls[12][1]
    url14 = urls[13][1]
    url15 = urls[14][1]
    url16 = urls[15][1]
    return render(request, 'customization.html', {'url1' : url1, 'url2' : url2, 'url3' : url3, 'url4' : url4, 'url5' : url5, 'url6' : url6, 'url7': url7, 'url8' : url8, 'url9' : url9, 'url10' : url10, 'url11' : url11, 'url12' : url12,'url13': url13, 'url14' : url14, 'url15' : url15, 'url16' : url16})

def result(request) : 

    fieldname = request.GET.get('fieldname' ,'None')
    newurl = request.GET.get('newurl', 'None')

    query_for_updating = f"UPDATE urls SET actualurls = '{newurl}' WHERE name = '{fieldname}';"
    dbcursor = dbconnection.cursor()
    dbcursor.execute(query_for_updating)
    dbconnection.commit()
    return render(request,'result.html')

def invalidwebpage(request) : 
    return render(request, 'error404.html')