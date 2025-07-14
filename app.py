
from flask import Flask, render_template, request, flash
import os
import csv

app = Flask(__name__)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = 'uploaded_cvs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_cv():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        file = request.files.get('cv')

        if not name or not email or not file:
            flash('⚠️ All fields are required.', 'danger')
            return render_template('upload.html')

        if not allowed_file(file.filename):
            flash('❌ Invalid file type. Only PDF, DOC, DOCX allowed.', 'danger')
            return render_template('upload.html')

        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save data to CSV
        with open('data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, filename])

        flash('✅ CV uploaded successfully!', 'success')
    return render_template('upload.html')
    if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)