from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_session import Session
from forms import GFDCInputs, UploadForm
import os
import uuid
import base64
import glob
from algorithm import dev_alg, cp_alg, final_class
from main import grading

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback_default_key') 

app.config['UPLOAD_PATH'] = os.path.normpath(os.path.join(app.root_path, 'uploads')) 
app.config["SESSION_FILE_DIR"] = os.path.normpath(os.path.join(app.root_path, 'sessions')) 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

def safe_delete(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        
        # Check if the file has a .png extension
        if file_path.lower().endswith('.png'):
            try:
                os.remove(file_path)
                print(f'Successfully deleted {file_path}')
            except Exception as e:
                print(f'Error deleting {file_path}. Reason: {e}')
        else:
            print(f'The file {file_path} is not a .png file')
    else:
        print(f'The file {file_path} does not exist')


@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])

def index():
    if 'image_uploaded' in session:
        if session['image_uploaded'] == True:
            session['image_uploaded'] = False
        else:
            session.clear()
    else:
        session.clear()
            
    if not 'name' in session:
        session['name'] = str(uuid.uuid4())
    
    session['final_classification'] = 'ERROR'
    session['dev_class'] = 'ERROR'
    session['cp_class'] = 'ERROR'
    session['plot_class'] = 'ERROR'
    uploadform = UploadForm()

    form = GFDCInputs()

    if form.submit.data:
        if glob.glob(os.path.join(app.config['UPLOAD_PATH'], session['name'] + ".*")):
            print('validated and submitted form')
            session['dev'] = form.dev.data
            session['cp1'] = form.central_point_1.data
            session['cp2'] = form.central_point_2.data
            session['cp3'] = form.central_point_3.data
            session['cp4'] = form.central_point_4.data

            return redirect(url_for('analysis'))
        else:
            flash(f'Please upload an image before proceeding with analysis!', 'danger')

    return render_template('import_analysis.html', form=form, uploadform=uploadform)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/upload_image', methods=['GET','POST'])
def upload_image():
    data = request.json['image_data']
    try:
        image_data = base64.b64decode(data.split(",")[1])
        
        
        # Generate a unique filename based on the session name
        filename = f"{session['name']}.png"
        
        # Save the image in the uploads folder
        image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        with open(image_path, 'wb') as f:
            f.write(image_data)

        session['image_uploaded'] = True
        return 'Image uploaded successfully!'

    except Exception as e:
        return 'Error uploading image!'

@app.route('/run_analysis', methods=['GET', 'POST'])
def run_analysis():
    session['process_ran']= 'True'
    
    print(os.path.join(app.config['UPLOAD_PATH'], session['name']+'.png'))
    session['dev_class'] = dev_alg(session['dev'])
    session['cp_class'] = cp_alg(session['cp1'],session['cp2'],session['cp3'],session['cp4'])
    print(os.path.join(app.root_path, app.config['UPLOAD_PATH'], session['name']+'.png'))
    session['plot_class'] = grading(os.path.join(app.root_path, app.config['UPLOAD_PATH'], session['name']+'.png'))

    session['final_classification'] = final_class(session['dev_class'], session['cp_class'],session['plot_class'])

    safe_delete(os.path.join(app.root_path, app.config['UPLOAD_PATH'], session['name']+'.png'))
    return("Analysis complete")

@app.route('/output', methods=['GET', 'POST'])
def analysis_complete():
    if 'process_ran' in session:
        output_class = session['final_classification']
        dev_class = session['dev_class']
        cp_class = session['cp_class']
        plot_class = session['plot_class']

        print(plot_class)
        if plot_class is None:
            return render_template('failed.html')
        else:
            return render_template('output.html', output_class=output_class, dev_class=dev_class, cp_class=cp_class, plot_class=plot_class)
    else:
        return redirect(url_for('index')) 


if __name__ == '__main__':
    app.run()
