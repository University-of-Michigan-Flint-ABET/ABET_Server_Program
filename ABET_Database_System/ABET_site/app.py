import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Route to render the HTML template with folder names
@app.route('/')
def index():
    folder_path = 'static/images'  # Path to your top-level image folders
    folder_names = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    return render_template('index.html', folder_names=folder_names)

# Route to fetch top-level folders
@app.route('/get_folders')
def get_folders():
    folder_path = 'static/images'  # Path to your top-level image folders
    folders = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    return jsonify(folders)

# Route to fetch subfolders within a folder
@app.route('/get_subfolders')
def get_subfolders():
    folder_name = request.args.get('folder', '')
    if folder_name:
        folder_path = os.path.join('static/images', folder_name)
        subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
        return jsonify(subfolders)
    return 'Folder not found', 404


# Route to fetch subfolders within a folder
@app.route('/get_subsubfolders')
def get_subsubfolders():
    folder_name = request.args.get('folder', '')
    subfolder_name = request.args.get('subfolder', '')
    if folder_name:
        folder_path = os.path.join('static/images', folder_name, subfolder_name)
        subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
        return jsonify(subfolders)
    return 'Folder not found', 404

# Route to fetch images from a folder and subfolder
@app.route('/get_images')
def get_images():
    folder_name = request.args.get('folder', '')
    subfolder_name = request.args.get('subfolder', '')
    subsubfolder_name = request.args.get('subsubfolder','')
    if folder_name and subfolder_name and subsubfolder_name:
        folder_path = os.path.join('static/images', folder_name, subfolder_name, subsubfolder_name)
        if os.path.isdir(folder_path):
            images = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
            return jsonify(images)
        else:
            return jsonify([])  # Return an empty array if the folder doesn't exist
    return 'Folder or subfolder not specified', 400

if __name__ == '__main__':
    app.run(debug=True)
