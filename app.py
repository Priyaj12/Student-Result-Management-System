from flask import Flask,render_template,request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__) 
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'priyaj@123'
app.config['MYSQL_DB'] = 'resultdb'

app.secret_key = "your app is trash"  
#Home Page 
@app.route('/')
def landing():
    return render_template('/Index.html')

@app.route('/home')
def home():
    return render_template('/Index.html')

@app.route('/about')
def about():
    return render_template('/About.html')

#Admin
@app.route('/admin')
def admin():
    return render_template('/admin.html')

@app.route('/selectsem')
def selectsem():
    return render_template('/selectsem.html')

#Admin Login
@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST' :
        name = request.form['User']
        password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE name = % s AND password = % s', (name, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['name'] = account['name']
            msg = 'Logged in successfully !'
            return render_template('/admin.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('/AdminLogin.html', msg=msg)


#Add Teacher
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST' :
        name = request.form['name']
        gender= request.form['gender']
        password = request.form['password']

        cur = mysql.connection.cursor()
     # Execute query
        cur.execute("INSERT INTO teachers (name, gender, password) VALUES (%s, %s, %s)", (name, gender, password))

        mysql.connection.commit()
        cur.close()
        return render_template('/AddTeacher.html')
    return render_template('/AddTeacher.html')

#------------------------------------------------------------------------------------------------------

#Teacher Login
@app.route('/teacherlogin', methods =['GET', 'POST'])
def teacherlogin():
    msg = ''
    if request.method == 'POST' :
        name = request.form['User']
        password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teachers WHERE name = % s AND password = % s', (name, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['name'] = account['name']
            msg = 'Logged in successfully !'
            # return redirect(url_for('home'))
            #return "login succesfull"
            return render_template('/selectsem.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('/TeacherLogin.html', msg=msg)

#-----------------------------------------------------------------------------------------#
#select semester
#Add Student
#add result sem I
@app.route('/sem1', methods =['GET', 'POST'])
def sem1():
    msg = ""
    grade=""
    if request.method == 'POST' :
        sname = request.form['sname']
        rollnum = request.form['rollnum']
        gender= request.form['gender']
        ip = int(request.form['ip'])
        ippract = int(request.form['ippract'])
        ipint = int(request.form['ipint'])
        de = int(request.form['de'])
        depract = int(request.form['depract'])
        deint = int(request.form['deint'])
        os = int(request.form['os'])
        ospract = int(request.form['ospract'])
        osint = int(request.form['osint'])
        dm = int(request.form['dm'])
        dmpract = int(request.form['dmpract'])
        dmint = int(request.form['dmint'])
        cs = int(request.form['cs'])
        cspract = int(request.form['cspract'])
        csint = int(request.form['csint'])

        # Calculate the total and percentage
        total =  ip + ippract + ipint + de + depract + deint + os + ospract + osint + dm + dmpract + dmint + cs + cspract + csint
        percentage = (total/750)*100

        if ip > 75 or de > 75 or os > 75 or dm > 75 or cs > 75 :
            msg="Please enter practical marks below 75"
            return render_template('/IT_sem1_Add.html',msg=msg)
        elif ippract > 50 or depract > 50 or ospract > 50 or dmpract > 50 or cspract > 50 :
            msg="Please enter practical marks below 50"
            return render_template('/IT_sem1_Add.html',msg=msg)
        elif ipint > 25 or deint > 25 or osint > 25 or dmint > 25 or csint > 25 :
            msg="Please enter practical marks below 25"
            return render_template('/IT_sem1_Add.html',msg=msg)
        else: 
            if ip < 30 or de < 30 or os < 30 or dm < 30 or cs < 30 :
                grade = "Fail"
            if ippract < 20 or depract < 20 or ospract <20 or dmpract < 20 or cspract < 20 :
                grade = "Fail"
            if ipint < 10 or deint < 10 or osint < 10 or dmint < 10 or csint < 10 :
                grade = "Fail"
            if grade !="Fail":
                if percentage >= 80:
                    grade="O"
                elif percentage >=70 and percentage < 80:
                    grade="A+"
                elif percentage >=60 and percentage < 70:
                    grade="A"
                elif percentage >=55 and percentage < 60:
                    grade="B+"
                elif percentage >=50 and percentage < 55:
                    grade="B"
                elif percentage >=45 and percentage < 50:
                    grade="C"
                elif percentage >=40 and percentage < 45:
                    grade="D"
                elif percentage < 45:
                    grade="Fail"
        percentage = "{:.2f}".format(percentage) 
        try:  
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute query
            cur.execute("INSERT INTO itsemfirst (sname, rollnum, gender, ip, ippract,ipint, de, depract,deint, os, ospract,osint, dm, dmpract,dmint, cs, cspract,csint, total, percentage, grade) VALUES (%s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sname,rollnum,gender,ip,ippract,ipint,de,depract,deint,os,ospract,osint,dm,dmpract,dmint,cs,cspract,csint,total, percentage, grade))

            mysql.connection.commit()
            # cur.close()
            # return render_template('/IT_sem1_Add.html',percentage=percentage)
            return redirect(url_for('viewsem1'))
        except:
            msg='Sorry, you cannot enter a roll number that has already been entered. Please try again with a different roll number.'
            return render_template('IT_sem1_Add.html',msg=msg)
    return render_template('/IT_sem1_Add.html')


#add result sem II

@app.route('/sem2', methods =['GET', 'POST'])
def sem2():
    msg = ""
    grade=""
    if request.method == 'POST' :
        sname = request.form['sname']
        rollnum = request.form['rollnum']
        gender= request.form['gender']
        oop= int(request.form['oop'])
        ooppract = int(request.form['ooppract'])
        oopint = int(request.form['oopint'])
        ma = int(request.form['ma'])
        mapract = int(request.form['mapract'])
        maint = int(request.form['maint'])
        wp = int(request.form['wp'])
        wppract = int(request.form['wppract'])
        wpint = int(request.form['wpint'])
        nsm = int(request.form['nsm'])
        nsmpract = int(request.form['nsmpract'])
        nsmint = int(request.form['nsmint'])
        gc = int(request.form['gc'])
        gcpract = int(request.form['gcpract'])
        gcint = int(request.form['gcint'])

        # Calculate the total and percentage
        total =  oop + ooppract + oopint + ma + mapract + maint + wp + wppract + wpint + nsm + nsmpract + nsmint + gc + gcpract + gcint
        percentage = (total/750)*100

        #Error msg 
        if oop > 75 or ma > 75 or wp > 75 or nsm > 75 or gc > 75 :
            msg="Please enter practical marks below 75"
            return render_template('/IT_sem2_Add.html',msg=msg)
        elif ooppract > 50 or mapract > 50 or wppract > 50 or nsmpract > 50 or gcpract > 50 :
            msg="Please enter practical marks below 50"
            return render_template('/IT_sem2_Add.html',msg=msg)
        elif oopint > 25 or maint > 25 or wpint > 25 or nsmint > 25 or gcint > 25 :
            msg="Please enter practical marks below 25"
            return render_template('/IT_sem2_Add.html',msg=msg)
        else: 
            if oop < 30 or ma < 30 or wp < 30 or nsm < 30 or gc < 30 :
                grade = "Fail"
            if ooppract < 20 or mapract < 20 or wppract <20 or nsmpract < 20 or gcpract < 20 :
                grade = "Fail"
            if oopint < 10 or maint < 10 or wpint < 10 or nsmint < 10 or gcint < 10 :
                grade = "Fail"
            if grade !="Fail":
                if percentage >= 80:
                    grade="O"
                elif percentage >=70 and percentage < 80:
                    grade="A+"
                elif percentage >=60 and percentage < 70:
                    grade="A"
                elif percentage >=55 and percentage < 60:
                    grade="B+"
                elif percentage >=50 and percentage < 55:
                    grade="B"
                elif percentage >=45 and percentage < 50:
                    grade="C"
                elif percentage >=40 and percentage < 45:
                    grade="D"
                elif percentage < 45:
                    grade="Fail"
        percentage = "{:.2f}".format(percentage)   
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute query
            cur.execute("INSERT INTO itsemsecond (sname, rollnum, gender, oop, ooppract,oopint, ma, mapract,maint, wp, wppract,wpint, nsm, nsmpract,nsmint, gc, gcpract,gcint, total, percentage, grade) VALUES (%s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sname,rollnum,gender,oop,ooppract,oopint,ma,mapract,maint,wp,wppract,wpint,nsm,nsmpract,nsmint,gc,gcpract,gcint,total, percentage, grade))

            mysql.connection.commit()
            #cur.close()
            # return render_template('/IT_sem1_Add.html',percentage=percentage)
            return redirect(url_for('viewsem2'))
        except:
            msg="Sorry, you cannot enter a roll number that has already been entered. Please try again with a different roll number."
            return render_template('IT_sem2_Add.html',msg=msg)
    return render_template('/IT_sem2_Add.html')


@app.route('/sem3', methods =['GET', 'POST'])
def sem3():
    msg = ""
    grade=""
    if request.method == 'POST' :
        sname = request.form['sname']
        rollnum = request.form['rollnum']
        gender= request.form['gender']
        py= int(request.form['py'])
        pypract = int(request.form['pypract'])
        pyint = int(request.form['pyint'])
        ds = int(request.form['ds'])
        dspract = int(request.form['dspract'])
        dsint = int(request.form['dsint'])
        cn = int(request.form['cn'])
        cnpract = int(request.form['cnpract'])
        cnint = int(request.form['cnint'])
        dbms = int(request.form['dbms'])
        dbmspract = int(request.form['dbmspract'])
        dbmsint = int(request.form['dbmsint'])
        am = int(request.form['am'])
        mppract = int(request.form['mppract'])
        amint = int(request.form['amint'])

        # Calculate the total and percentage
        total =  py + pypract + pyint + ds + dspract + dsint + cn + cnpract + cnint + dbms + dbmspract + dbmsint + am + mppract + amint
        percentage = (total/750)*100

        #Error msg 
        if py > 75 or ds > 75 or cn > 75 or dbms > 75 or am > 75 :
            msg="Please enter practical marks below 75"
            return render_template('/IT_sem3_Add.html',msg=msg)
        elif pypract > 50 or dspract > 50 or cnpract > 50 or dbmspract > 50 or mppract > 50 :
            msg="Please enter practical marks below 50"
            return render_template('/IT_sem3_Add.html',msg=msg)
        elif pyint > 25 or dsint > 25 or cnint > 25 or dbmsint > 25 or amint > 25 :
            msg="Please enter practical marks below 25"
            return render_template('/IT_sem3_Add.html',msg=msg)
        else: 
            if py < 30 or ds < 30 or cn < 30 or dbms < 30 or am < 30 :
                grade = "Fail"
            if pypract < 20 or dspract < 20 or cnpract <20 or dbmspract < 20 or mppract < 20 :
                grade = "Fail"
            if pyint < 10 or dsint < 10 or cnint < 10 or dbmsint < 10 or amint < 10 :
                grade = "Fail"
            if grade != "Fail":
                if percentage >= 80:
                    grade="O"
                elif percentage >=70 and percentage < 80:
                    grade="A+"
                elif percentage >=60 and percentage < 70:
                    grade="A"
                elif percentage >=55 and percentage < 60:
                    grade="B+"
                elif percentage >=50 and percentage < 55:
                    grade="B"
                elif percentage >=45 and percentage < 50:
                    grade="C"
                elif percentage >=40 and percentage < 45:
                    grade="D"
                elif percentage < 45:
                    grade="Fail"
        percentage = "{:.2f}".format(percentage)   
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Execute query
            cur.execute("INSERT INTO itsemthird (sname, rollnum, gender, py, pypract,pyint, ds, dspract,dsint, cn, cnpract,cnint, dbms, dbmspract,dbmsint, am, mppract,amint, total, percentage, grade) VALUES (%s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sname,rollnum,gender,py, pypract,pyint, ds, dspract,dsint, cn, cnpract,cnint, dbms, dbmspract,dbmsint, am, mppract,amint,total, percentage, grade))

            mysql.connection.commit()
            #cur.close()
            # return render_template('/IT_sem1_Add.html',percentage=percentage)
            return redirect(url_for('viewsem3'))
        except:
            msg = "Sorry, you cannot enter a roll number that has already been entered. Please try again with a different roll number."
            return render_template('IT_sem3_Add.html',msg=msg)
    return render_template('/IT_sem3_Add.html')

@app.route('/sem4', methods =['GET', 'POST'])
def sem4():
    msg = ""
    grade = ""
    if request.method == 'POST' :
        sname = request.form['sname']
        rollnum = request.form['rollnum']
        gender= request.form['gender']
        cj= int(request.form['cj'])
        cjpract = int(request.form['cjpract'])
        cjint = int(request.form['cjint'])
        ies = int(request.form['ies'])
        iespract = int(request.form['iespract'])
        iesint = int(request.form['iesint'])
        cost = int(request.form['cost'])
        costpract = int(request.form['costpract'])
        costint = int(request.form['costint'])
        se = int(request.form['se'])
        sepract = int(request.form['sepract'])
        seint = int(request.form['seint'])
        cga = int(request.form['cga'])
        cgapract = int(request.form['cgapract'])
        cgaint = int(request.form['cgaint'])

        # Calculate the total and percentage
        total =  cj + cjpract + cjint + ies + iespract + iesint + cost + costpract + costint + se + sepract + seint + cga + cgapract + cgaint
        percentage = (total/750)*100

        #Error msg 
        if cj > 75 or ies > 75 or cost > 75 or se > 75 or cga > 75 :
            msg="Please enter practical marks below 75"
            return render_template('/IT_sem4_Add.html',msg=msg)
        elif cjpract > 50 or iespract > 50 or costpract > 50 or sepract > 50 or cgapract > 50 :
            msg="Please enter practical marks below 50"
            return render_template('/IT_sem4_Add.html',msg=msg)
        elif cjint > 25 or iesint > 25 or costint > 25 or seint > 25 or cgaint > 25 :
            msg="Please enter practical marks below 25"
            return render_template('/IT_sem4_Add.html',msg=msg)
        else: 
            if cj < 30 or ies < 30 or cost < 30 or se < 30 or cga < 30 :
                grade = "Fail"
            if cjpract < 20 or iespract < 20 or costpract <20 or sepract < 20 or cgapract < 20 :
                grade = "Fail"
            if cjint < 10 or iesint < 10 or costint < 10 or seint < 10 or cgaint < 10 :
                grade = "Fail"
            if grade != "Fail":
                if percentage >= 80:
                    grade="O"
                elif percentage >=70 and percentage < 80:
                    grade="A+"
                elif percentage >=60 and percentage < 70:
                    grade="A"
                elif percentage >=55 and percentage < 60:
                    grade="B+"
                elif percentage >=50 and percentage < 55:
                    grade="B"
                elif percentage >=45 and percentage < 50:
                    grade="C"
                elif percentage >=40 and percentage < 45:
                    grade="D"
                elif percentage < 45:
                    grade="Fail"
        percentage = "{:.2f}".format(percentage)   
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute query
            cur.execute("INSERT INTO itsemfourth (sname, rollnum, gender, cj, cjpract,cjint, ies, iespract,iesint, cost, costpract,costint, se, sepract,seint, cga, cgapract,cgaint, total, percentage, grade) VALUES (%s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sname,rollnum,gender, cj, cjpract,cjint, ies, iespract,iesint, cost, costpract,costint, se, sepract,seint, cga, cgapract,cgaint,total, percentage, grade))

            mysql.connection.commit()
            # cur.close()
            # return render_template('/IT_sem1_Add.html',percentage=percentage)
            return redirect(url_for('viewsem4'))
        except:
            msg="Sorry, you cannot enter a roll number that has already been entered. Please try again with a different roll number."
            return render_template('IT_sem4_Add.html',msg=msg)
    return render_template('/IT_sem4_Add.html')

@app.route('/sem5', methods =['GET', 'POST'])
def sem5():
    msg = ""
    grade = ""
    if request.method == 'POST' :
        sname = request.form['sname']
        rollnum = request.form['rollnum']
        gender= request.form['gender']
        spm= int(request.form['spm'])
        pdpract = int(request.form['pdpract'])
        spmint = int(request.form['spmint'])
        iot = int(request.form['iot'])
        iotpract = int(request.form['iotpract'])
        iotint = int(request.form['iotint'])
        awp = int(request.form['awp'])
        awppract = int(request.form['awppract'])
        awpint = int(request.form['awpint'])
        lsa = int(request.form['lsa'])
        lsapract = int(request.form['lsapract'])
        lsaint = int(request.form['lsaint'])
        ej = int(request.form['ej'])
        ejpract = int(request.form['ejpract'])
        ejint = int(request.form['ejint'])

        # Calculate the total and percentage
        total =  spm + pdpract + spmint + iot + iotpract + iotint + awp + awppract + awpint + lsa + lsapract + lsaint + ej + ejpract + ejint
        percentage = (total/750)*100

        #Error msg 
        if spm > 75 or iot > 75 or awp > 75 or lsa > 75 or ej > 75 :
            msg="Please enter practical marks below 75"
            return render_template('/IT_sem5_Add.html',msg=msg)
        elif pdpract > 50 or iotpract > 50 or awppract > 50 or lsapract > 50 or ejpract > 50 :
            msg="Please enter practical marks below 50"
            return render_template('/IT_sem5_Add.html',msg=msg)
        elif spmint > 25 or iotint > 25 or awpint > 25 or lsaint > 25 or ejint > 25 :
            msg="Please enter practical marks below 25"
            return render_template('/IT_sem5_Add.html',msg=msg)
        else: 
            if spm < 30 or iot < 30 or awp < 30 or lsa < 30 or ej < 30 :
                grade = "Fail"
            if pdpract < 20 or iotpract < 20 or awppract <20 or lsapract < 20 or ejpract < 20 :
                grade = "Fail"
            if spmint < 10 or iotint < 10 or awpint < 10 or lsaint < 10 or ejint < 10 :
                grade = "Fail"
            if grade != "Fail":
                if percentage >= 80:
                    grade="O"
                elif percentage >=70 and percentage < 80:
                    grade="A+"
                elif percentage >=60 and percentage < 70:
                    grade="A"
                elif percentage >=55 and percentage < 60:
                    grade="B+"
                elif percentage >=50 and percentage < 55:
                    grade="B"
                elif percentage >=45 and percentage < 50:
                    grade="C"
                elif percentage >=40 and percentage < 45:
                    grade="D"
                elif percentage < 45:
                    grade="Fail"
        percentage = "{:.2f}".format(percentage)   
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute query
            cur.execute("INSERT INTO itsemfifth (sname, rollnum, gender, spm, pdpract,spmint, iot, iotpract,iotint, awp, awppract,awpint, lsa, lsapract,lsaint, ej, ejpract,ejint, total, percentage, grade) VALUES (%s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sname,rollnum,gender, spm, pdpract,spmint, iot, iotpract,iotint, awp, awppract,awpint, lsa, lsapract,lsaint, ej, ejpract,ejint, total, percentage, grade))

            mysql.connection.commit()
            # cur.close()
            # return render_template('/IT_sem1_Add.html',percentage=percentage)
            return redirect(url_for('viewsem5'))
        except:
            msg="Sorry, you cannot enter a roll number that has already been entered. Please try again with a different roll number."
            return render_template('IT_sem5_Add.html',msg=msg)
    return render_template('/IT_sem5_Add.html')

@app.route('/sem6', methods =['GET', 'POST'])
def sem6():
    msg = ""
    grade = ""
    if request.method == 'POST' :
        sname = request.form['sname']
        rollnum = request.form['rollnum']
        gender= request.form['gender']
        sqa= int(request.form['sqa'])
        pi = int(request.form['pi'])
        sqaint = int(request.form['sqaint'])
        sic = int(request.form['sic'])
        sicpract = int(request.form['sicpract'])
        sicint = int(request.form['sicint'])
        bi = int(request.form['bi'])
        bipract = int(request.form['bipract'])
        biint = int(request.form['biint'])
        gis = int(request.form['gis'])
        gispract = int(request.form['gispract'])
        gisint = int(request.form['gisint'])
        cl = int(request.form['cl'])
        amppract = int(request.form['amppract'])
        clint = int(request.form['clint'])

        # Calculate the total and percentage
        total =  sqa + pi + sqaint + sic + sicpract + sicint + bi + bipract + biint + gis + gispract + gisint + cl + amppract + clint
        percentage = (total/750)*100

        #Error msg 
        if sqa > 75 or sic > 75 or bi > 75 or gis > 75 or cl > 75 :
            msg="Please enter practical marks below 75"
            return render_template('/IT_sem6_Add.html',msg=msg)
        elif pi > 50 or sicpract > 50 or bipract > 50 or gispract > 50 or amppract > 50 :
            msg="Please enter practical marks below 50"
            return render_template('/IT_sem6_Add.html',msg=msg)
        elif sqaint > 25 or sicint > 25 or biint > 25 or gisint > 25 or clint > 25 :
            msg="Please enter practical marks below 25"
            return render_template('/IT_sem6_Add.html',msg=msg)
        else: 
            if sqa < 30 or sic < 30 or bi < 30 or gis < 30 or cl < 30 :
                grade = "Fail"
            if pi < 20 or sicpract < 20 or bipract <20 or gispract < 20 or amppract < 20 :
                grade = "Fail"
            if sqaint < 10 or sicint < 10 or biint < 10 or gisint < 10 or clint < 10 :
                grade = "Fail"
            if grade != "Fail":
                if percentage >= 80:
                    grade="O"
                elif percentage >=70 and percentage < 80:
                    grade="A+"
                elif percentage >=60 and percentage < 70:
                    grade="A"
                elif percentage >=55 and percentage < 60:
                    grade="B+"
                elif percentage >=50 and percentage < 55:
                    grade="B"
                elif percentage >=45 and percentage < 50:
                    grade="C"
                elif percentage >=40 and percentage < 45:
                    grade="D"
                elif percentage < 45:
                    grade="Fail"
        percentage = "{:.2f}".format(percentage)   
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute query
            cur.execute("INSERT INTO itsemsix (sname, rollnum, gender, sqa, pi,sqaint, sic, sicpract,sicint, bi, bipract,biint, gis, gispract,gisint, cl, amppract,clint, total, percentage, grade) VALUES (%s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sname,rollnum,gender, sqa, pi,sqaint, sic, sicpract,sicint, bi, bipract,biint, gis, gispract,gisint, cl, amppract,clint, total, percentage, grade))

            mysql.connection.commit()
            # cur.close()
            # return render_template('/IT_sem1_Add.html',percentage=percentage)
            return redirect(url_for('viewsem6'))
        except:
            msg="Sorry, you cannot enter a roll number that has already been entered. Please try again with a different roll number."
            return render_template('IT_sem6_Add.html',msg=msg)
    return render_template('/IT_sem6_Add.html')

#-----------------------------------------------------------------------------

# View result
#sem1
@app.route('/viewsem1')
def viewsem1():
    username = session.get('name', None)
    if username != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM itsemfirst')
        rows = cursor.fetchall()
    else:
        return redirect(url_for('teacherlogin'))
    return render_template('/view_record_s1.html',rows=rows)
    
#sem2
@app.route('/viewsem2')
def viewsem2():
    username = session.get('name', None)
    if username != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM itsemsecond')
        rows = cursor.fetchall()
    else:
        return redirect(url_for('teacherlogin'))
    return render_template('/view_record_s2.html',rows=rows)

#sem3
@app.route('/viewsem3')
def viewsem3():
    username = session.get('name', None)
    if username != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM itsemthird')
        rows = cursor.fetchall()
    else:
        return redirect(url_for('teacherlogin'))
    return render_template('/view_record_s3.html',rows=rows)

#sem4
@app.route('/viewsem4')
def viewsem4():
    username = session.get('name', None)
    if username != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM itsemfourth')
        rows = cursor.fetchall()
    else:
        return redirect(url_for('teacherlogin'))
    return render_template('/view_record_s4.html',rows=rows)

#sem5
@app.route('/viewsem5')
def viewsem5():
    username = session.get('name', None)
    if username != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM itsemfifth')
        rows = cursor.fetchall()
    else:
        return redirect(url_for('teacherlogin'))
    return render_template('/view_record_s5.html',rows=rows)

#sem6
@app.route('/viewsem6')
def viewsem6():
    username = session.get('name', None)
    if username != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM itsemsix')
        rows = cursor.fetchall()
    else:
        return redirect(url_for('teacherlogin'))
    return render_template('/view_record_s6.html',rows=rows)

#--------------------------------------------------------------------------------------------------------
#Student Login
@app.route('/studentlogin',methods=['GET','POST'])
def studentlogin():
    roll_no = request.form.get('roll_no')
    if request.method =='POST':
        sem_select = request.form["sem_select"]
        if sem_select == "itsemfirst":
            template = "result_sem1.html"
        elif sem_select == "itsemsecond":
            template = "result_sem2.html"
        elif sem_select == "itsemthird":
            template = "result_sem3.html"
        elif sem_select == "itsemfourth":
            template = "result_sem4.html"
        elif sem_select == "itsemfifth":
            template = "result_sem5.html"
        elif sem_select == "itsemsix":
            template = "result_sem6.html"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM {sem_select} where rollnum="{roll_no}"')
        rows = cursor.fetchall()
        if rows == ():
            msg="Enter Valid Roll Number"
            return render_template('student.html',msg=msg)
        return render_template(f'{template}',roll_no=roll_no,sem_select=sem_select,rows=rows)
    return render_template('/student.html')

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('teacherlogin'))

if __name__=="__main__":
    app.run(debug=True)