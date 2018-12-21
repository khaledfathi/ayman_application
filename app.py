########################################
#Description : flask main file for ayman_database web Application
#Created : 10/12/2018
#Last Update : 20/12/2018
#Author : khaledfathi@protonmail.com
#PGP Fingerprint : FC8C B81A 70AE 4998 EB62  6F1A 202C 2C62 E64C 0367 
########################################

from os import path
from flask import Flask , render_template , url_for,request,redirect,flash,send_file
from werkzeug.utils  import secure_filename
import actions

UPLOAD_FOLDER=actions.main_path+"static/upload_files/"

app=Flask(__name__)
app.secret_key=b'60\8\f7\6f\f6\df\b9\5a\da\86\44\7c\f8\bd\15\98'
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

##################################
########## Flask pages ###########
##################################

############################################################
@app.route('/')
def index ():
    return render_template('index.html')

############################################################
@app.route('/data_entry',methods=["GET","POST"])
def data_entry():
    if request.method=="POST":
        data={}
        for i in actions.data_entry_form_names:
            get_this = request.form.get(i)
            data[i]=get_this
        if  actions.insert_in_db(data):
            flash("تم الحفظ بنجاح")
            return redirect(url_for('data_entry'))
        else:
            error="خطأ فى الوصول الى قاعدة البيانات"
            return render_template("data_entry.html",error=error)
    else:
        new_id= actions.new_id()
        return render_template("data_entry.html",new_id=new_id)

############################################################
@app.route("/query" ,methods=["GET","POST"])
def query ():
    edit_status = request.args.get("update_delete_status") 
    edit_id = request.args.get("update_delete_id")
    data={}
    for i in actions.query_form_names:
        get_this = request.args.get(i)
        data[i]=get_this
    if data["search"] or data["search_from"] or data['search_to']:
        query = actions.send_to_query(data)
        html_query=actions.query_to_tabel(query)
        if not query :
            nothing ="لا يوجد نتائج لهذا البحث"
            return render_template("query.html",nothing=nothing)
        return render_template("query.html",query=html_query)
    if edit_status and edit_id:
        if edit_status=="DELETE":
            try :
                actions.database.sql("DELETE FROM orders WHERE id={}".format(edit_id))
                flash ("تم حذف السجل بنجاح")
                return redirect(url_for("query"))
            except:
                ids = actions.get_numbers(edit_id)
                for i in ids :
                    actions.database.sql("DELETE FROM orders WHERE id={}".format(i))
                return redirect(url_for("query"))
        elif edit_status == "UPDATE":
            target_id=int(edit_id)
            query=actions.database.query("SELECT * FROM orders WHERE id={}".format(target_id))
            if request.method=="POST":
                if request.form.get("delete_on")=="DELETE":
                    id_=request.form.get("id")
                    actions.database.sql("DELETE FROM orders WHERE id={}" .format(id_))
                    flash("تم حذف السجل بنجاح")
                    return redirect(url_for("query"))
                data={}
                for i in actions.update_form_names:
                    get_this = request.form.get(i)
                    data[i]=get_this
                    actions.update(data)
                    flash("تم التعديل بنجاح")
                return redirect(url_for("query"))
            
            return render_template('update.html',query=query)
    else:
        return render_template("query.html")


############################################################
@app.route('/help', methods=["GET","POST"])
def help():
    if request.method=="POST":
        data={}
        for i in actions.help_form_names:
            get_this=request.form.get(i)
            data[i]=get_this
        if data["action_type"]=="EXPORT_SQL":
            actions.db_backup()
            return send_file("Backup_SQL.sql",as_attachment=True,attachment_filename="Backup_sql.sql")
        elif data["action_type"]=="EXPORT_HTML":
            actions.html_export()
            return send_file("export_html.html",as_attachment=True,attachment_filename="backup_html.html")
        elif data["action_type"]=="EXECUTE":
            ALLOWD_EXTENTIONS= set(["sql"])
            if "import_file" not in request.files:
                flash("لم يتم اختيار ملف")
                return redirect(url_for('help'))
            f=request.files['import_file']
            if actions.extenstion_allowed(f.filename,ALLOWD_EXTENTIONS):
                f.save(path.join(app.config["UPLOAD_FOLDER"],secure_filename(f.filename)))
                actions.restore_database(UPLOAD_FOLDER + secure_filename(f.filename))
                flash("تم استعادة قاعدة البيانات بنجاح")
                return redirect(url_for('help'))
            else:
                return ("EXTENSTION NOT ALLOWED")
            return ("file saved")
        elif data["action_type"]=="DESTROY":
            return render_template('destroy.html')
    destroy_db= request.args.get("confirm_destroy")
    if destroy_db:
        actions.destroy_database()
        actions.create_empty_table()
        flash ('تم حذف جميع السجلات ')
        return redirect(url_for("help"))

    return render_template("help.html")

