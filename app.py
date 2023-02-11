from flask import Flask,redirect,send_file,request
import os
import traceback
from werkzeug.utils import secure_filename

app=Flask(__name__)


@app.route('/upload', methods = ['POST'])
def upload():
    try:
        file = request.files['form_file'] 
        filename = secure_filename(file.filename)
        file.save(os.path.join("./files", filename))
    except:
        traceback.print_exc()

    return redirect('/')

@app.route('/files')
def list_files():
    files = os.listdir("./files")
    jpg_files=[]
    for file in files:
        if file.lower().endswith(".jpg"):
            jpg_files.append(file)
    return jpg_files

@app.route('/files/<filename>')
def get_file(filename):
    #log
    print("GET /files/"+filename)

    return send_file('./files/'+filename)

@app.route('/')
def index(): 
    index_html ="""
                <form method="post" enctype="multipart/form-data" action="/upload" method="post">
                    <div>
                        <label for="file">Choose file to upload</label>
                        <input type="file" id="file" name="form_file" accept="image/jpeg"/>
                    </div>
                    <div>
                        <button>Submit</button>
                    </div>
                </form>
                """

    for file in list_files():
        index_html += "<li><a href=\"/files/" + file + "\">" + file + "</a></li>"
   
    return index_html

if __name__=='__main__':
    app.run()