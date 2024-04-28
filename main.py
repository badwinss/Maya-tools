# -*- coding: utf-8 -*-
import maya.cmds as cmds
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import os

class PluginWindow(QDialog):
    def __init__(self):
        super(PluginWindow, self).__init__()

        self.setWindowTitle("Previz Pipeline Tool")
        self.setFixedSize(500, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.model_list = QListWidget()
        self.model_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.camera_list = QListWidget()
        self.camera_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.create_widgets()
        self.create_layout()

        # Load previously saved paths
        self.load_saved_paths()

    def create_widgets(self):
        self.model_path_label = QLabel("Objects")
        self.model_path_label.setFixedWidth(80)
        self.model_path_edit = QLineEdit()
        self.model_path_edit.setReadOnly(True)
        self.model_path_button = QPushButton("Path of Object Library")
        self.model_path_button.clicked.connect(self.browse_model_path)

        self.camera_path_label = QLabel("Cameras")
        self.camera_path_label.setFixedWidth(80)
        self.camera_path_edit = QLineEdit()
        self.camera_path_edit.setReadOnly(True)
        self.camera_path_button = QPushButton("Path of Camera Library")
        self.camera_path_button.clicked.connect(self.browse_camera_path)

        self.model_list_label = QLabel("Object List")
        self.camera_list_label = QLabel("Camera List")

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate)

    def create_layout(self):
        layout = QVBoxLayout()

        # Model path row layout
        model_path_layout = QHBoxLayout()
        model_path_layout.addWidget(self.model_path_label)
        model_path_layout.addWidget(self.model_path_edit)
        model_path_layout.addWidget(self.model_path_button)

        # Camera path row layout
        camera_path_layout = QHBoxLayout()
        camera_path_layout.addWidget(self.camera_path_label)
        camera_path_layout.addWidget(self.camera_path_edit)
        camera_path_layout.addWidget(self.camera_path_button)

        # Add model path row and camera path row to main layout
        layout.addLayout(model_path_layout)
        layout.addLayout(camera_path_layout)

        # Model list row layout
        model_list_layout = QVBoxLayout()
        model_list_layout.addWidget(self.model_list_label)
        model_list_layout.addWidget(self.model_list)

        # Camera list row layout
        camera_list_layout = QVBoxLayout()
        camera_list_layout.addWidget(self.camera_list_label)
        camera_list_layout.addWidget(self.camera_list)

        # Add model list row and camera list row to main layout
        list_layout = QHBoxLayout()
        list_layout.addLayout(model_list_layout)
        list_layout.addLayout(camera_list_layout)
        layout.addLayout(list_layout)

        # Generate button row layout
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def browse_model_path(self):
        path = QFileDialog.getExistingDirectory(self, "Path of Object Library", self.model_path_edit.text() if self.model_path_edit.text() else QDir.homePath())
        if path:
            self.model_path_edit.setText(path)
            self.populate_model_list(path)
            # Save selected path
            cmds.optionVar(stringValue=("ModelPath", path))

    def browse_camera_path(self):
        path = QFileDialog.getExistingDirectory(self, "Path of Camera Library", self.camera_path_edit.text() if self.camera_path_edit.text() else QDir.homePath())
        if path:
            self.camera_path_edit.setText(path)
            self.populate_camera_list(path)
            # Save selected path
            cmds.optionVar(stringValue=("CameraPath", path))

    def load_saved_paths(self):
        model_path = cmds.optionVar(query="ModelPath")
        camera_path = cmds.optionVar(query="CameraPath")

        if model_path:
            self.model_path_edit.setText(model_path)
            self.populate_model_list(model_path)

        if camera_path:
            self.camera_path_edit.setText(camera_path)
            self.populate_camera_list(camera_path)

    def populate_model_list(self, path):
        self.model_list.clear()
        files = [file for file in os.listdir(path) if file.endswith(('.mb', '.ma'))]  # Getting files in .mb and .ma formats
        for file in files:
            self.model_list.addItem(file)

    def populate_camera_list(self, path):
        self.camera_list.clear()
        files = [file for file in os.listdir(path) if file.endswith(('.mb', '.ma'))]  # Getting files in .mb and .ma formats
        for file in files:
            self.camera_list.addItem(file)

    def generate(self):
        selected_models = self.model_list.selectedItems()
        selected_cameras = self.camera_list.selectedItems()

        if not selected_models:
            cmds.warning("Please choose at least one object!")
            return

        if not selected_cameras:
            cmds.warning("Please choose at least one camera!")
            return

        model_path = self.model_path_edit.text()
        camera_path = self.camera_path_edit.text()

        for selected_model in selected_models:
            model_file = selected_model.text()
            model_full_path = os.path.join(model_path, model_file)
            if os.path.exists(model_full_path):
                namespace = os.path.splitext(model_file)[0]  # Using filenames as namespaces
                cmds.file(model_full_path, i=True, namespace=namespace)
            else:
                cmds.warning(f"Doc '{model_full_path}' is not exist!")

        for selected_camera in selected_cameras:
            camera_file = selected_camera.text()
            camera_full_path = os.path.join(camera_path, camera_file)
            if os.path.exists(camera_full_path):
                namespace = os.path.splitext(camera_file)[0]  # Using filenames as namespaces
                cmds.file(camera_full_path, i=True, namespace=namespace)
            else:
                cmds.warning(f"Doc '{camera_full_path}' is not exist!")

if __name__ == "__main__":
    try:
        cmds.deleteUI("Previz Pipeline Tool")
    except:
        pass

    dialog = PluginWindow()
    dialog.show()
