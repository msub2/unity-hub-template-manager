'''
The GUI for Unity Hub Template Manager
'''
from PyQt5.QtWidgets import *
from pathlib import Path
from os import listdir
import uhtm


def display():
    # Initialize window and basic layout
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    # Editor Path Header
    editor_header = QLabel()
    editor_header.setText('Editor Path')
    layout.addWidget(editor_header)

    # Editor Row Setup
    editor_row = QWidget()
    editor_row_layout = QHBoxLayout()

    # Editor Folder Path
    editor_folder = QLineEdit()
    editor_folder.setText(uhtm.get_default_path())
    editor_folder.setFixedWidth(256)
    editor_folder.editingFinished.connect(
        lambda: update_unity_versions(unity_versions, Path(editor_folder.text())))

    # Editor Browse Button
    editor_browse = QPushButton()
    editor_browse.setText('Browse...')
    editor_browse.clicked.connect(lambda: set_path(editor_folder))

    # Editor Row Construction
    editor_row_layout.addWidget(editor_folder)
    editor_row_layout.addWidget(editor_browse)
    editor_row.setLayout(editor_row_layout)
    layout.addWidget(editor_row)

    # Unity Versions Selector
    unity_versions_header = QLabel()
    unity_versions_header.setText('Unity Version')
    unity_versions = QComboBox()
    layout.addWidget(unity_versions_header)
    layout.addWidget(unity_versions)

    # Project Path Header
    project_header = QLabel()
    project_header.setText('Project Path')
    layout.addWidget(project_header)

    # Project Row Setup
    project_row = QWidget()
    project_row_layout = QHBoxLayout()

    # Project Folder Path
    project_folder = QLineEdit()
    project_folder.setFixedWidth(256)

    # Project Folder Browse Button
    project_folder_browse = QPushButton()
    project_folder_browse.setText('Browse...')
    project_folder_browse.clicked.connect(lambda: set_path(project_folder))

    # Project Row Construction
    project_row_layout.addWidget(project_folder)
    project_row_layout.addWidget(project_folder_browse)
    project_row.setLayout(project_row_layout)
    layout.addWidget(project_row)

    # package.json fields
    name_header = QLabel()
    name_header.setText('Filename')
    name = QLineEdit()

    displayname_header = QLabel()
    displayname_header.setText('Display Name')
    displayname = QLineEdit()

    version_header = QLabel()
    version_header.setText('Version')
    version = QLineEdit()

    description_header = QLabel()
    description_header.setText('Description')
    description = QLineEdit()

    layout.addWidget(name_header)
    layout.addWidget(name)
    layout.addWidget(displayname_header)
    layout.addWidget(displayname)
    layout.addWidget(version_header)
    layout.addWidget(version)
    layout.addWidget(description_header)
    layout.addWidget(description)

    # Create Template Button
    create_template_button = QPushButton()
    create_template_button.setText('Create Template')
    create_template_button.clicked.connect(
        lambda: create_template(project_folder.text(), editor_folder.text(),
                                name.text(), displayname.text(), version.text(),
                                description.text(), unity_versions.currentText()))
    layout.addWidget(create_template_button)

    window.setLayout(layout)
    window.setWindowTitle('Unity Hub Template Manager')
    window.show()
    app.exec_()


def set_path(folder_path):
    folder_path.setText(str(QFileDialog.getExistingDirectory()))


def create_template(project_path, editor_path, name, displayname, version, description, unity_version):
    package = [
        name,
        displayname,
        version,
        description
    ]
    if uhtm.verify_paths(project_path, editor_path):
        uhtm.create_template(editor_path, package, unity_version)


def update_unity_versions(version_list, editor_path):
    if editor_path and Path.is_dir(editor_path):
        for f in listdir(editor_path):
            version_list.addItem(f)
