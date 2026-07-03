from flask import Flask, request, redirect, url_for, render_template, flash, session,send_file,jsonify
from io import BytesIO
from flask_session import Session
from otp import genotp
from cmail import send_mail
from stoken import endata,dndata
from mysql.connector import (connection)
import re


mydb=connection.MySQLConnection(user='root',password='Admin@23',host='localhost',database='snm29db')
import flask_excel as excel
app = Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
Session(app)
excel.init_excel(app)
app.secret_key='code000'


@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username']
    useremail = request.form['useremail']
    userpassword = request.form['userpassword']
    userphone = request.form['userphone']
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from userdata where useremail=%s',[useremail])
        email_count=cursor.fetchone() [0] #(1,)
        cursor.close()
    except Exception as e:
        print('Mysql error',str(e))
        flash('could not verify email')
        return redirect(url_for('home'))
    else:
        if email_count==0:  
            gotp = genotp()  #calling function
            userdata={'username':username,'useremail':useremail,'userpassword':userpassword,
              'userphone':userphone,'serverotp':gotp}

            subject=f'OTP verfication SNM project'
            body=f"use the given otp{gotp}"
            send_mail(to=useremail,subject=subject,body=body)
            flash('OTP has been sent to given mail')
            return redirect(url_for('otpverify',serverdata=endata(userdata)))
        elif email_count==1:
            flash('user email already existed')
            return redirect(url_for('home'))
        

@app.route('/otpverify/<serverdata>',methods=['GET','POST'])
def otpverify(serverdata):
    if request.method=='POST':
        userotp=request.form['otp']
        try:
            d_data=dndata(serverdata)
            print(d_data)  #{'username':username,'useremail':useremail,'userpassword':userpassword,'userphone':userphone,'serverotp':gotp}

        except Exception as e:
            print(e)
            flash('Could not verify otp')
            return redirect(url_for('otpverify',serverdata=serverdata))    
        if userotp==d_data['serverotp']:
            #mysql cursor defining
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('insert into userdata(username,useremail,password,phone_num)values(%s,%s,%s,%s)',[d_data['username'],d_data['useremail'],d_data['userpassword'],d_data['userphone']])
                mydb.commit()
                cursor.close()
            except Exception as e: 
                print(str(e))
                flash('could not store user details')
                return redirect(url_for('otpverify', serverdata=serverdata))
            else:
                flash('user Registration successfull')
                return redirect(url_for('home'))

            
        else:
            flash('Invalid otp')
            return redirect(url_for('otpverify',serverdata=serverdata))
    return render_template('otpverify.html')

@app.route('/login',methods=['POST'])
def login():
    login_useremail=request.form['useremail']
    login_password=request.form['password']

    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from userdata where useremail=%s',[login_useremail])
        email_count=cursor.fetchone() [0] #(1,),(0,)
        print(email_count)
    except Exception as e:
        print('Mysql error',str(e))
        flash('could not verify email')
        return redirect(url_for('home'))
    else:
        if email_count==1:
            cursor.execute('select password from userdata where useremail=%s',[login_useremail])
            stored_password=cursor.fetchone()[0]
            if stored_password==login_password:
                print(session,'before')
                session['user']=login_useremail
                print(session,'after')
                return redirect(url_for('dashboard'))
            else:
                flash('Invaild password')
                return redirect(url_for('home'))
        elif email_count==0:
            flash('No email registred')
            return redirect(url_for('home'))
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  

@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('insert into notesdata(title,description,userid) values(%s,%s,%s)',[title,description,user_id])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not store notes details')
            return redirect(url_for('addnotes'))
        else:
            flash('Notes addes successfully')
            return redirect(url_for('addnotes'))
    return render_template('addnotes.html')  

@app.route('/viewallnotes')
def viewallnotes():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
  
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,title,created_at from notesdata where userid=%s',[user_id])
        allnotesdata=cursor.fetchall() #[(1,'python','time'),]
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))
           
    return render_template('viewallnotes.html',allnotesdata=allnotesdata)

@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,title,description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        notesdata=cursor.fetchone() #(1,'python','desc',time')
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))
    return render_template('viewnotes.html',notesdata=notesdata)


@app.route('/deletenotes/<nid>')
def deletenotes(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute("delete from notesdata where userid=%s and notesid=%s ",[user_id,nid])
        mydb.commit() 
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('viewallnotes'))
    
@app.route('/updatenotes/<nid>',methods=['GET','POST'])
def updatenotes(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,title,description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        notesdata=cursor.fetchone() #(1,'python','desc',time')
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        updated_title=request.form['title']
        updated_description=request.form['description']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('update notesdata set title=%s,description=%s where userid=%s and notesid=%s',[updated_title,updated_description,user_id,nid])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not update notes details')
            return redirect(url_for('updatenotes',nid=nid))
        else:
            flash('Notes update successfully')
            return redirect(url_for('updatenotes',nid=nid))
    return render_template('updatenotes.html',notesdata=notesdata)  
  
@app.route('/getexceldata',methods=['GET'])
def getexceldata():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,title,description,created_at from notesdata where userid=%s',[user_id])
        allnotesdata=cursor.fetchall()    #[(1,python,time)]
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))    
    else:
        array_data=[list(i) for i in allnotesdata]  #[[1,'python','time'],[2,sql,'date']]
        headings=['Notesid','Title','Description','Created_at']
        array_data.insert(0,headings)
        print(array_data)
        return excel.make_response_from_array(array_data,'xlsx',filename='NotesExcel')
    
@app.route('/uploadfile',methods=['GET','POST'])
def uploadfile():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('home'))
    if request.method=='POST':
        file_info=request.files['file']
        fname=file_info.filename
        fdata=file_info.read()
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('insert into filedata(filename,filedata,userid) values(%s,%s,%s)',[fname,fdata,user_id])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not save file details')
            return redirect(url_for('uploadfile'))
        else:
            flash('File uploaded successfully')
            return redirect(url_for('uploadfile'))

    return render_template('uploadfile.html')


@app.route('/viewallfiles')
def viewallfiles():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select fileid,filename,created_at from filedata where userid=%s',[user_id])
        allfilesdata=cursor.fetchall()    #[(1,python,time)]
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))    
    return render_template('viewallfiles.html',allfilesdata=allfilesdata)
   

@app.route('/deletefile/<fid>')
def deletefile(fid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('delete from filedata where userid=%s and fileid=%s',[user_id,fid])
        mydb.commit()    
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not delete notes details')
        return redirect(url_for('dashboard'))    
    return redirect(url_for('viewallfiles'))


@app.route('/viewfile/<fid>',methods=['GET'])
def viewfile(fid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))

    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',
        [session.get('user')])
        user_id = cursor.fetchone()[0]

        cursor.execute('select fileid, filename,filedata,created_at from filedata where userid=%s and fileid=%s',
        [user_id, fid])
        stored_filedata = cursor.fetchone()
        bytes_data=BytesIO(stored_filedata[2])
        filename=stored_filedata[1]
        return send_file(bytes_data,as_attachment=False, download_name=filename)
       
    except Exception as e:
        print(e)
        flash('could not view file')
        return redirect(url_for('viewallfiles'))
    

@app.route('/downloadfile/<fid>')
def downloadfile(fid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))

    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',
        [session.get('user')])
        user_id = cursor.fetchone()[0]

        cursor.execute('select fileid, filename,filedata,created_at from filedata where userid=%s and fileid=%s',
        [user_id, fid])
        stored_filedata = cursor.fetchone()
        bytes_data=BytesIO(stored_filedata[2])
        filename=stored_filedata[1]
        return send_file(bytes_data,as_attachment=True, download_name=filename)
       
    except Exception as e:
        print(e)
        flash('could not view file')
        return redirect(url_for('viewallfiles'))
    
@app.route('/search',methods=['POST'])
def search():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('home'))
    try:
        user_search=request.form['query']
        strg=['A-Za-z0-9']
        pattern=re.compile(f'^{strg}',re.IGNORECASE)
        if pattern.match(user_search):
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()[0]
                cursor.execute('select notesid,title,description,created_at from notesdata where (notesid like %s or title like %s or created_at like %s) and userid=%s',[user_search+'%',user_search+'%',user_search+'%',user_id])
                allnotesdata=cursor.fetchall() 
                cursor.close()
            except Exception as e:
                print(e)
                flash('could not fetch notes details')
                return redirect(url_for('dashboard'))
            return render_template('viewallnotes.html',allnotesdata=allnotesdata)
        else:
            flash('Invalid search')
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        flash('could not search data')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('home'))
    session.pop('user')
    return redirect(url_for('home'))


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        forgot_email = request.form['useremail']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from userdata where useremail=%s',[forgot_email])
            email_count=cursor.fetchone()[0]
            cursor.close()
            if email_count==1:
                subject=f'Re-set link for Forgot password SNM prj'
                body=f"use the link for forgot password {url_for('newpassword',data=endata(forgot_email),_external=True)}"
                send_mail(to=forgot_email,subject=subject,body=body)
                flash('Reset link has been to given mail')
                return redirect(url_for('forgotpassword'))
            elif email_count==0:
                flash('User not found')
                return redirect(url_for('forgotpassword'))
        except Exception as e:
            print(e)
            flash('could not send the email')
            return redirect(url_for('forgotpassword'))    
    return render_template('forgot.html')

@app.route('/newpassword/<data>',methods=['GET','PUT'])
def newpassword(data):
    try:
        forgot_email=dndata(data)
    except Exception as e:
        print(e)
        flash('could not fetch email')
        return redirect(url_for('password',data=data))  
    else:
        if request.method=='PUT':
            newdata=request.get_json()
            print(newdata)
            npassword=newdata.get('newpassword')
            cpassword=newdata.get('confimpassword')
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update userdata set password=%s where useremail=%s',[npassword,forgot_email])
                mydb.commit()
                cursor.close()
            except Exception as e:
                print(e)
                return jsonify({
                    "status":'failed',
                    "message":f'could not update password {str(e)}'

                })
            else:
                return jsonify({
                    "status":'success',
                    "message":"ok"
                })  

        return render_template('newpassword.html')       

    
   
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)