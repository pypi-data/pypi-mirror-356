from datetime import datetime
from zipfile import ZipFile
import os, shutil, urllib.parse
from flask import request, current_app, render_template, redirect, url_for

def ENABLE_STATIC(app, edits):

    @edits.route('/'+app.config.get('APP_STATIC_FOLDER'))
    @edits.route('/'+app.config.get('APP_STATIC_FOLDER')+'/<path:page>')
    def retrive_static(page=None):
        if page:
            page = urllib.parse.unquote(page)
        STATIC_PATH = os.path.join(current_app.config['FILE_PATH'],app.config.get('APP_STATIC_FOLDER'))
        if not os.path.exists(STATIC_PATH):
            os.mkdir(STATIC_PATH)
        if page:
            folder_location = app.config.get('APP_STATIC_FOLDER')+'/'+page
            FolderPath = STATIC_PATH + '/'+page
        else:
            folder_location = app.config.get('APP_STATIC_FOLDER')
            FolderPath = STATIC_PATH
        contents = {}
        for root, folders, files in os.walk(FolderPath):
            if root == FolderPath: 
                for folder in folders:
                    relative_location = os.path.relpath(os.path.join(root, folder), STATIC_PATH)
                    folder_path = os.path.join(root, folder)
                    folder_stats = os.stat(folder_path)
                    contents[folder] = {
                        "type": "folder",
                        "name": folder,
                        "location": '/'+app.config.get('APP_STATIC_FOLDER')+'/'+relative_location,
                        "last_modified": datetime.fromtimestamp(folder_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "size": str(round(folder_stats.st_size / 1024, 2))+" KiB",
                    }
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_location = os.path.relpath(file_path, STATIC_PATH)
                    file_stats = os.stat(file_path)  # Get file stats
                    filename, extension = os.path.splitext(file)
                    contents[file] = {
                        "type": "file",
                        "name": filename+extension,
                        "extension": extension,
                        "location": '/'+app.config.get('APP_STATIC_FOLDER')+'/'+relative_location,
                        "last_modified": datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "size": str(round(file_stats.st_size / 1024, 2))+" KiB",
                    }
        return render_template('static.html', contents=contents, folder_location=folder_location) 
    
def EDITABLE_STATIC(app, edits):
    @edits.route('/'+app.config.get('APP_STATIC_FOLDER')+'-edit/<path:page>', methods=['POST'])
    def static_edit(page=None):
        location = request.form.get('location')
        if page == 'upload':
            files = request.files['file']
            files.save(os.path.join(current_app.config['FILE_PATH'],location, request.form.get('file_name')))
        elif page == 'create_folder':
            new_folder_path = os.path.join(current_app.config['FILE_PATH'], location, request.form.get('folder_name'))
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
        elif page == 'unzip':
            location = request.form.get('detail_location')
            location = current_app.config['FILE_PATH']+location
            new_folder_path, _ = os.path.splitext(location)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            with ZipFile(location, 'r') as zObject: 
                zObject.extractall(path=new_folder_path) 
        elif page == 'delete':
            location = request.form.get('detail_location')
            location = current_app.config['FILE_PATH']+location
            if os.path.exists(location):
                if os.path.isfile(location):
                    os.remove(location)
                elif os.path.isdir(location):
                    shutil.rmtree(location)  
        elif page == 'back':
            parts = location.split('/')
            parent_directory = '/'.join(parts[1:-1])  # Join parts starting from index 1 to the second-to-last index
            if parent_directory == '':
                return redirect(url_for('edits.retrive_static', page=None))
            return redirect(url_for('edits.retrive_static', page=parent_directory))
        elif page == 'rename':
            location = location+'/'+request.form.get('name')
            if os.path.exists(location):
                if os.path.isfile(location):
                    directory = os.path.dirname(location)
                    new_name = request.form.get('file_folder_name')
                    base_name = new_name
                    extension = os.path.splitext(location)[1]
                    if new_name.find('.') != -1:
                        base_name, extension = os.path.splitext(new_name)
                    new_location = os.path.join(directory, base_name + extension)
                    os.rename(location, new_location)
                elif os.path.isdir(location):  # If it's a directory
                    new_name = request.form.get('file_folder_name')
                    new_location = os.path.join(os.path.dirname(location), new_name)
                    os.rename(location, new_location)
        elif page == 'search':
            folder_path = current_app.config['FILE_PATH']+'/'+location
            search_input = request.form.get('searchInput')
            search_input = search_input.lower()
            contents = {}
            for root, folders, files in os.walk(folder_path):
                for folder in folders:
                    if search_input in folder.lower():  # Compare in lowercase
                        relative_location = os.path.relpath(os.path.join(root, folder), folder_path)
                        folder_stats = os.stat(os.path.join(root, folder))
                        contents[folder] = {
                            "type": "folder",
                            "name": folder,
                            "location": '/'+app.config.get('APP_STATIC_FOLDER')+'/'+relative_location,
                            "last_modified": datetime.fromtimestamp(folder_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                            "size": str(round(folder_stats.st_size / 1024, 2))+" KiB",
                        }
                for file in files:
                    if search_input in file.lower():  # Compare in lowercase
                        file_path = os.path.join(root, file)
                        relative_location = os.path.relpath(file_path, folder_path)
                        file_stats = os.stat(file_path)  # Get file stats
                        filename, extension = os.path.splitext(file)
                        contents[file] = {
                            "type": "file",
                            "name": filename+extension,
                            "extension": extension,
                            "location": '/'+app.config.get('APP_STATIC_FOLDER')+'/'+relative_location,
                            "last_modified": datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                            "size": str(round(file_stats.st_size / 1024, 2))+" KiB",
                        }
            return render_template('static.html', contents=contents, searched_location=folder_path) 
        location = request.form.get('location')
        parts = location.split('/')
        if len(parts) == 1:
            location=None
        else:
            location = '/'.join(parts[-1:])
        return redirect(url_for('edits.retrive_static', page=location))