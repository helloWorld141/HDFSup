from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json, os, subprocess
from utils import parseConfig

# defining constant
UPLOAD_FOLDER = "temp"
ALLOWED_EXTENSIONS = set(["csv", "txt"])
##### bootstraping app ####
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
config = parseConfig()
#### define functions ####

def allowed_file(filename): # filename is a string
    return "." in filename and filename.split(".")[1].lower() in ALLOWED_EXTENSIONS

#### handle requests ####
@app.route("/")
@app.route("/index")
def index():
    return render_template("main.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            print("No file part")
            return redirect(url_for("index"), code=302)
        else:
            print("Upload request: " + request.form['upload_file'])
            myfile = request.files['file']
            if myfile.filename == "":
                print("No selected file")
                return "no selected file"
            else:
                print(myfile.filename)
                filename = secure_filename(myfile.filename)
                save_dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
                filepath = os.path.join(save_dir, filename)
                if os.path.exists(filepath):
                    return "file already uploaded"
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir, exist_ok=True)
                print("Saving file to " + filepath)
                myfile.save(filepath)
                ### TODO: saving to hdfs ###
                subprocess.run(["hdfs" ,"dfs", "-put", filepath, "/user/ubuntu/data"], stdout=subprocess.PIPE)
                return "received POST"
    else:
        return redirect(url_for("index"), code=302)

if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=True)
