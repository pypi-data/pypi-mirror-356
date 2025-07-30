#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Standalone Inversion Application for Pyckster

This module provides a PyQt window for loading .sgt files,
running inversions, and visualizing results without using core.py.
"""

import sys
import os
import numpy as np
import pygimli as pg
from pygimli.physics import TravelTimeManager as refrac
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QFileDialog, QGroupBox, QFormLayout,QComboBox,
    QDoubleSpinBox, QSpinBox, QCheckBox, QMessageBox, QSplitter,QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt, QLocale
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Try different import approaches
try:
    # Try relative import first (when part of a package)
    from .visualization_utils import InversionVisualizations
except ImportError:
    try:
        # Try absolute import next (when package is installed)
        from pyckster.visualization_utils import InversionVisualizations
    except ImportError:
        # Finally try direct import (when in same directory)
        from visualization_utils import InversionVisualizations

# Import the tab factory at the top of your file
try:
    from tab_factory import TabFactory
except ImportError:
    try:
        from pyckster.tab_factory import TabFactory
    except ImportError:
        from .tab_factory import TabFactory

# Set the locale globally to English (United States) to use '.' as the decimal separator
QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

import locale
locale.setlocale(locale.LC_NUMERIC, 'C')  # Ensure decimal point is '.'

class StandaloneInversionApp(QMainWindow):
    def __init__(self, picking_data=None, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("PyGIMLI Inversion Tool")
        self.sgt_file = None
        self.refrac_manager = None
        
        # Default inversion parameters
        self.params = {
            'vTop': 300, 'vBottom': 3000, 'secNodes': 2, 'paraDX': 0.33,
            'paraDepth': None, 'balanceDepth': False, 'paraMaxCellSize': None,
            'zWeight': 0.5, 'lam': 30, 'maxIter': 6, 'verbose': True,
        }
        
        self.initUI()

        if picking_data:
            self.load_data_from_pyckster(picking_data)

    def load_data_from_pyckster(self, picking_data):
        """
        Initializes the refraction manager using data passed from Pyckster's core.
        This version correctly handles variable receiver geometry for each shot.
        """
        try:
            # --- Step 1: Extract the coordinate lists ---
            picks = picking_data.get('picks')
            error = picking_data.get('error', 0.05)  # Default error if not provide
            sources_x_list = picking_data.get('source_position')
            sources_z_list = picking_data.get('source_elevation')
            traces_x_lists = picking_data.get('trace_position') # List of lists
            traces_z_lists = picking_data.get('trace_elevation') # List of lists

            if any(v is None for v in [picks, sources_x_list, sources_z_list, traces_x_lists, traces_z_lists]):
                QMessageBox.critical(self, "Error", "Incomplete data received from Pyckster.")
                return

            # --- Step 2: Create a unified list of ALL sensor positions from the entire survey ---
            all_positions_raw = []

            # Add all source positions
            source_pairs = list(zip(sources_x_list, sources_z_list))
            all_positions_raw.extend(source_pairs)

            # Add all receiver positions from every shot's unique geometry
            for i in range(len(traces_x_lists)):
                receiver_pairs_for_shot = list(zip(traces_x_lists[i], traces_z_lists[i]))
                all_positions_raw.extend(receiver_pairs_for_shot)
                
            # Find the unique positions and maintain a sorted order for consistency
            unique_positions_tuples = sorted(list(set(all_positions_raw)))
            all_sensors = np.array(unique_positions_tuples)

            # --- Step 3: Create a mapping from a position to its new, unique index ---
            position_to_index_map = {pos: i for i, pos in enumerate(unique_positions_tuples)}

            # --- Step 4: Build the s, g, and t arrays using the new indices ---
            s_indices, g_indices, t_values, err_values = [], [], [], []
            for shot_idx, shot_picks in enumerate(picks):
                # Get the source position for the current shot
                current_source_pos = (sources_x_list[shot_idx], sources_z_list[shot_idx])
                s_idx = position_to_index_map[current_source_pos]

                # Get the receiver positions for THIS SPECIFIC shot
                current_traces_x = traces_x_lists[shot_idx]
                current_traces_z = traces_z_lists[shot_idx]
                current_traces_err = error if isinstance(error, (int, float)) else error[shot_idx]

                for rec_idx, travel_time in enumerate(shot_picks):
                    if not np.isnan(travel_time):
                        # Get the receiver position for this specific pick
                        current_trace_pos = (current_traces_x[rec_idx], current_traces_z[rec_idx])
                        g_idx = position_to_index_map[current_trace_pos]
                        err =  current_traces_err if isinstance(current_traces_err, (int, float)) else current_traces_err[rec_idx]
                        
                        s_indices.append(s_idx)
                        g_indices.append(g_idx)
                        t_values.append(travel_time)
                        err_values.append(err)

            # --- Step 5: Create the pygimli DataContainer ---
            data = pg.DataContainer()
            data.setSensorPositions(all_sensors)

            # np.array(s_indices, dtype=int) is an array of integers, but data['s'] = np.array(s_indices, dtype=int) gives an array of floats

            data['s'] = np.array(s_indices, dtype=int)  # Sensor indices for sources
            data['g'] = np.array(g_indices, dtype=int)  # Sensor indices for receivers
            data['t'] = np.array(t_values, dtype=float)  # Travel times
            data['err'] = np.array(err_values, dtype=float)  # Errors

            data.registerSensorIndex('s')
            data.registerSensorIndex('g')

            data.markValid(data['s'] > 0)
            data.save('temp.sgt',"g s t err valid")

            self.refrac_manager = refrac(data)

            num_shots = len(np.unique(self.refrac_manager.data['s']))
            num_geo = len(np.unique(self.refrac_manager.data['g']))
            num_picks = len(self.refrac_manager.data['t'])
            self.file_label.setText(f"Data loaded from Pyckster\n"
                                    f"Shots: {num_shots}\n"
                                    f"Receivers: {num_geo}\n"
                                    f"Picks: {num_picks}")

            self.load_file_button.setEnabled(False)
            self.showDataTab()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process data from Pyckster: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def initUI(self):
        # Set locale to use period as decimal separator
        locale = QLocale(QLocale.C)  # C locale uses period as decimal separator
        QLocale.setDefault(locale)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for parameter panel and visualization
        splitter = QSplitter(Qt.Horizontal)
        # Make sure the splitter expands to fill available space
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create left panel for parameters
        param_widget = QWidget()
        param_layout = QVBoxLayout(param_widget)

        # After creating the param_widget
        param_widget = QWidget()
        # Set a minimum width but allow it to be as narrow as possible by default
        param_widget.setMinimumWidth(310)  # Minimum width to ensure controls are usable
        param_layout = QVBoxLayout(param_widget)

        # Add title label at the top of the parameter panel
        title_label = QLabel("<h3>Time picks</h3>")
        title_label.setAlignment(Qt.AlignLeft)  # Center the title
        param_layout.addWidget(title_label)

        # Add Load SGT File button at the top
        self.load_file_button = QPushButton("Load SGT File")
        self.load_file_button.clicked.connect(self.loadSgtFile)
        param_layout.addWidget(self.load_file_button)

        # Add file information label directly below the load button
        self.file_label = QLabel("No SGT file selected")
        self.file_label.setWordWrap(True)  # Allow text to wrap
        param_layout.addWidget(self.file_label)

        # Add horizontal line below the load button
        line = QLabel("<hr>")
        line.setAlignment(Qt.AlignLeft)  # Align the line to the left
        param_layout.addWidget(line)

        # Add title label at the top of the parameter panel
        title_label = QLabel("<h3>Time Correction Parameters</h3>")
        title_label.setAlignment(Qt.AlignLeft)  # Center the title
        param_layout.addWidget(title_label)

        # Create time correction parameter group
        time_correction_group = QGroupBox()
        time_correction_form = QFormLayout()

        # Velocity source selection
        self.velocity_mode_combo = QComboBox()
        self.velocity_mode_combo.addItem("Surface Velocity", "surface")
        self.velocity_mode_combo.addItem("Constant Velocity", "constant")
        time_correction_form.addRow("Velocity Source:", self.velocity_mode_combo)

        # Constant velocity parameter
        self.corr_velocity_spin = QDoubleSpinBox()
        self.corr_velocity_spin.setRange(100, 5000)
        self.corr_velocity_spin.setValue(300)  # Default value
        self.corr_velocity_spin.setSingleStep(50)
        self.corr_velocity_spin.setEnabled(False)  # Initially disabled
        time_correction_form.addRow("Constant Velocity (m/s):", self.corr_velocity_spin)

        # Surface velocity parameters
        self.surf_velocity_smooth_check = QCheckBox()
        self.surf_velocity_smooth_check.setChecked(True)
        self.surf_velocity_smooth_check.setEnabled(True)  # Initially disabled
        time_correction_form.addRow("Smooth Surface Velocity:", self.surf_velocity_smooth_check)

        self.surf_velocity_window_spin = QSpinBox()
        self.surf_velocity_window_spin.setRange(3, 21)
        self.surf_velocity_window_spin.setValue(9)
        self.surf_velocity_window_spin.setSingleStep(2)
        self.surf_velocity_window_spin.setEnabled(True)  # Initially disabled
        time_correction_form.addRow("Smoothing Window:", self.surf_velocity_window_spin)

        # Connect velocity mode combo to enable/disable related controls
        self.velocity_mode_combo.currentIndexChanged.connect(self.updateVelocityControls)

        # Set locale for numeric inputs
        self.corr_velocity_spin.setLocale(locale)

        # Add form to group
        time_correction_group.setLayout(time_correction_form)

        # Add group to param layout (between buttons and inversion parameters)
        param_layout.addWidget(time_correction_group)

        # Add Time Correction button below 
        correct_time_button = QPushButton("Correct Time Picks")
        correct_time_button.clicked.connect(self.correctTimePicks)
        param_layout.addWidget(correct_time_button)

        # Add horizontal line below the load button
        line = QLabel("<hr>")
        line.setAlignment(Qt.AlignLeft)  # Align the line to the left
        param_layout.addWidget(line)

        # Add title label for error parameters
        title_label = QLabel("<h3>Error Parameters</h3>")
        title_label.setAlignment(Qt.AlignLeft)  # Center the title
        param_layout.addWidget(title_label)

        # Create error parameter group
        error_group = QGroupBox()
        error_form = QFormLayout()

        # Create absolute and relative error spinboxes

        self.absolute_error_spin = QDoubleSpinBox()
        self.absolute_error_spin.setRange(0, 1e3)
        self.absolute_error_spin.setValue(0)  # Default value
        self.absolute_error_spin.setSingleStep(0.1)
        self.absolute_error_spin.setLocale(locale)  # Set locale for numeric input
        error_form.addRow("Absolute Error (ms):", self.absolute_error_spin)

        self.relative_error_spin = QDoubleSpinBox()
        self.relative_error_spin.setRange(0, 2.0)
        self.relative_error_spin.setValue(0.05)  # Default value
        self.relative_error_spin.setSingleStep(0.005)
        self.relative_error_spin.setLocale(locale)  # Set locale for numeric input
        error_form.addRow("Relative Error:", self.relative_error_spin)

        self.max_absolute_error_spin = QDoubleSpinBox()
        self.max_absolute_error_spin.setRange(0, 1e3)
        self.max_absolute_error_spin.setValue(1e3)  # Default value
        self.max_absolute_error_spin.setSingleStep(0.1)
        self.max_absolute_error_spin.setLocale(locale)  # Set locale for numeric input
        error_form.addRow("Max Absolute Error (ms):", self.max_absolute_error_spin)

        self.min_absolute_error_spin = QDoubleSpinBox()
        self.min_absolute_error_spin.setRange(0, 1e3)
        self.min_absolute_error_spin.setValue(0)  # Default value
        self.min_absolute_error_spin.setSingleStep(0.1)
        self.min_absolute_error_spin.setLocale(locale)  # Set locale for numeric input
        error_form.addRow("Min Absolute Error (ms):", self.min_absolute_error_spin)

        self.max_relative_error_spin = QDoubleSpinBox()
        self.max_relative_error_spin.setRange(0, 2)
        self.max_relative_error_spin.setValue(0.5)  # Default value
        self.max_relative_error_spin.setSingleStep(0.005)
        self.max_relative_error_spin.setLocale(locale)  # Set locale for numeric input
        error_form.addRow("Max Relative Error:", self.max_relative_error_spin)
        
        # For each QDoubleSpinBox, explicitly set the locale
        self.absolute_error_spin.setLocale(locale)
        self.relative_error_spin.setLocale(locale)
        self.max_absolute_error_spin.setLocale(locale)
        self.min_absolute_error_spin.setLocale(locale)
        self.max_relative_error_spin.setLocale(locale)

        # Add form to group
        error_group.setLayout(error_form)

        # Add group to param layout (between time correction and inversion parameters)
        param_layout.addWidget(error_group)

        # Add Error Parameters button below
        set_error_button = QPushButton("Set Errors")
        set_error_button.clicked.connect(self.setErrors)
        param_layout.addWidget(set_error_button)

        # Add horizontal line below the load button
        line = QLabel("<hr>")
        line.setAlignment(Qt.AlignLeft)  # Align the line to the left
        param_layout.addWidget(line)

        # Add title label for inversion parameters
        title_label = QLabel("<h3>Inversion Parameters</h3>")
        title_label.setAlignment(Qt.AlignLeft)  # Center the title
        param_layout.addWidget(title_label)
        
        # Create parameter group
        param_group = QGroupBox()
        param_form = QFormLayout()
        
        # Create parameter spinboxes
        self.vTop_spin = QDoubleSpinBox()
        self.vTop_spin.setRange(100, 5000)
        self.vTop_spin.setValue(self.params['vTop'])
        self.vTop_spin.setSingleStep(50)
        param_form.addRow("Top Velocity (m/s):", self.vTop_spin)
        
        self.vBottom_spin = QDoubleSpinBox()
        self.vBottom_spin.setRange(500, 10000)
        self.vBottom_spin.setValue(self.params['vBottom'])
        self.vBottom_spin.setSingleStep(100)
        param_form.addRow("Bottom Velocity (m/s):", self.vBottom_spin)
        
        self.secNodes_spin = QSpinBox()
        self.secNodes_spin.setRange(1, 10)
        self.secNodes_spin.setValue(self.params['secNodes'])
        param_form.addRow("Secondary Nodes:", self.secNodes_spin)
        
        self.paraDX_spin = QDoubleSpinBox()
        self.paraDX_spin.setRange(0.1, 2.0)
        self.paraDX_spin.setValue(self.params['paraDX'])
        self.paraDX_spin.setDecimals(2)
        self.paraDX_spin.setSingleStep(0.05)
        param_form.addRow("Para DX (m):", self.paraDX_spin)
        
        self.paraDepth_spin = QDoubleSpinBox()
        self.paraDepth_spin.setRange(0, 100)
        self.paraDepth_spin.setValue(20)  # Default value if None
        self.paraDepth_spin.setSingleStep(1)
        self.paraDepth_spin.setSpecialValueText("Auto")  # 0 means Auto (None)
        param_form.addRow("Para Depth (m):", self.paraDepth_spin)
        
        self.balanceDepth_check = QCheckBox()
        self.balanceDepth_check.setChecked(self.params['balanceDepth'])
        param_form.addRow("Balance Depth:", self.balanceDepth_check)
        
        self.zWeight_spin = QDoubleSpinBox()
        self.zWeight_spin.setRange(0.1, 1.0)
        self.zWeight_spin.setValue(self.params['zWeight'])
        self.zWeight_spin.setDecimals(2)
        self.zWeight_spin.setSingleStep(0.05)
        param_form.addRow("Z Weight:", self.zWeight_spin)
        
        self.lam_spin = QDoubleSpinBox()
        self.lam_spin.setRange(1, 100)
        self.lam_spin.setValue(self.params['lam'])
        self.lam_spin.setSingleStep(1)
        param_form.addRow("Lambda:", self.lam_spin)
        
        self.maxIter_spin = QSpinBox()
        self.maxIter_spin.setRange(1, 20)
        self.maxIter_spin.setValue(self.params['maxIter'])
        param_form.addRow("Max Iterations:", self.maxIter_spin)
        
        self.verbose_check = QCheckBox()
        self.verbose_check.setChecked(self.params['verbose'])
        param_form.addRow("Verbose:", self.verbose_check)

        # For each QDoubleSpinBox, explicitly set the locale
        self.vTop_spin.setLocale(locale)
        self.vBottom_spin.setLocale(locale)
        self.paraDX_spin.setLocale(locale)
        self.paraDepth_spin.setLocale(locale)
        self.zWeight_spin.setLocale(locale)
        self.lam_spin.setLocale(locale)
        
        # Add form to group
        param_group.setLayout(param_form)
        
        # Add group to param layout (now below the buttons)
        param_layout.addWidget(param_group)

        # Add Run Inversion button below
        run_button = QPushButton("Run Inversion")
        run_button.clicked.connect(self.runInversion)
        param_layout.addWidget(run_button)
        
        # Add stretcher to push everything up
        param_layout.addStretch()

        # Wrap the parameter widget in a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Enable resizing
        scroll_area.setWidget(param_widget)  # Set the parameter widget as the scrollable content

        # Add the scroll area to the splitter
        splitter.addWidget(scroll_area)
        
        # First, create the right panel that will hold the tabs
        viz_widget = QWidget()
        viz_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        viz_layout = QVBoxLayout(viz_widget)

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        viz_layout.addWidget(self.tab_widget)

        # Create tabs using the factory
        self.data_tab = TabFactory.create_data_tab(self)
        self.models_tab = TabFactory.create_models_tab(self)
        self.traveltimes_tab = TabFactory.create_traveltimes_tab(self)
        self.source_receiver_tab = TabFactory.create_source_receiver_tab(self)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.data_tab, "Data")
        self.tab_widget.addTab(self.models_tab, "Models")
        self.tab_widget.addTab(self.traveltimes_tab, "Traveltimes")
        self.tab_widget.addTab(self.source_receiver_tab, "Source vs Receiver")

        # Add the viz widget to the main splitter
        splitter.addWidget(viz_widget)
 
        # Set initial sizes for splitter (20% for menu, 80% for figures)
        splitter.setSizes([330, 700])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Set stretch factors to control how extra space is distributed when maximizing
        splitter.setStretchFactor(0, 0)  # Parameter panel (left) should not stretch
        splitter.setStretchFactor(1, 1)  # Visualization panel (right) gets all extra space 
        
        # Set window size
        self.resize(1600, 900)
    
    def loadSgtFile(self):
        """Load a .sgt file using a file dialog"""
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Load SGT File', '', 'SGT Files (*.sgt)')
        
        if fname:
            self.sgt_file = fname
            self.file_label.setText(f"File: {os.path.basename(fname)}")
            
            # Load the file and initialize the refraction manager
            try:
                self.refrac_manager = refrac(fname)

                # Generate mesh and assign it to the manager


                # Print number of shots and picks imported
                num_shots = len(np.unique(self.refrac_manager.data['s']))
                num_geo = len(np.unique(self.refrac_manager.data['g']))
                num_picks = len(self.refrac_manager.data['t'])
                self.file_label.setText(f"File: {os.path.basename(fname)}\n"
                                        f"Shots: {num_shots}\n"
                                        f"Receivers: {num_geo}\n"
                                        f"Picks: {num_picks}")
                
                # After successful loading, display the visualization
                self.showDataTab()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load SGT file: {str(e)}")
                import traceback
                traceback.print_exc()
                self.sgt_file = None
                self.refrac_manager = None
                return
        else:
            self.file_label.setText("No SGT file selected")
            self.sgt_file = None
            self.refrac_manager = None
            
            # Reset parameters to defaults
            self.params = {
                'vTop': 300,
                'vBottom': 3000,
                'secNodes': 2,
                'paraDX': 0.33,
                'paraDepth': None,
                'balanceDepth': False,
                'paraMaxCellSize': None,
                'zWeight': 0.5,
                'lam': 30,
                'maxIter': 6,
                'verbose': True,
            }
            
            # Update the existing tab with empty content
            new_data_tab = TabFactory.create_data_tab(self)
            self.tab_widget.removeTab(0)
            self.tab_widget.insertTab(0, new_data_tab, "Data")
            self.data_tab = new_data_tab
            self.tab_widget.setCurrentIndex(0)

    def setErrors(self):
        """Set errors for the inversion"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "Please load an SGT file first.")
            return
        
        if self.refrac_manager.data['t'].size == 0:
            QMessageBox.warning(self, "Warning", "No travel times available to set errors.")
            return  
        
        # Ensure the 'err' column exists in the data
        if not self.refrac_manager.data.haveData('err'):
            self.refrac_manager.data['err'] = np.zeros_like(self.refrac_manager.data['t'])        
        
        # Get error values from UI controls
        absolute_error = self.absolute_error_spin.value()/1000
        relative_error = self.relative_error_spin.value()
        max_absolute_error = self.max_absolute_error_spin.value()/1000
        min_absolute_error = self.min_absolute_error_spin.value()/1000
        max_relative_error = self.max_relative_error_spin.value()
        
        # Calculate the errors
        for i in range(len(self.refrac_manager.data['t'])):
            pick = self.refrac_manager.data['t'][i]
            if np.isnan(pick):
                continue

            error = pick * relative_error + absolute_error
            if max_absolute_error is not None:
                if error > max_absolute_error:
                    error = max_absolute_error
            if min_absolute_error is not None:
                if error < min_absolute_error:
                    error = min_absolute_error
            if max_relative_error is not None:
                if error > max_relative_error * pick:
                    error = max_relative_error * pick

            self.refrac_manager.data['err'][i] = error
        
        QMessageBox.information(self, "Success", "Errors set successfully.")

    def showDataTab(self):
        """Update visualization in the Data tab"""
        if not self.refrac_manager:
            return
            
        # Create new data tab content
        new_data_tab = TabFactory.create_data_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(0)
        self.tab_widget.insertTab(0, new_data_tab, "Data")
        self.data_tab = new_data_tab  # Update the reference
        
        # Switch to the Data tab
        self.tab_widget.setCurrentIndex(0)

    def showModelTab(self):
        """Update visualization in the Model tab"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        # Create new model tab content
        new_model_tab = TabFactory.create_models_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(1)
        self.tab_widget.insertTab(1, new_model_tab, "Models")
        self.model_tab = new_model_tab  # Update the reference
        
        # Switch to the Models tab
        self.tab_widget.setCurrentIndex(1)

    def showTraveltimesTab(self):
        """Update visualization in the Traveltimes tab"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        # Create new traveltimes tab content
        new_traveltimes_tab = TabFactory.create_traveltimes_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(2)
        self.tab_widget.insertTab(2, new_traveltimes_tab, "Traveltimes")
        self.traveltimes_tab = new_traveltimes_tab

    def showSourceReceiverTab(self):
        """Update visualization in the Source vs Receiver tab"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        # Create new source-receiver tab content
        new_source_receiver_tab = TabFactory.create_source_receiver_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(3)
        self.tab_widget.insertTab(3, new_source_receiver_tab, "Source vs Receiver")
        self.source_receiver_tab = new_source_receiver_tab
        
    def getInversionParams(self):
        """Get inversion parameters from UI controls"""
        self.params['vTop'] = self.vTop_spin.value()
        self.params['vBottom'] = self.vBottom_spin.value()
        self.params['secNodes'] = self.secNodes_spin.value()
        self.params['paraDX'] = self.paraDX_spin.value()
        
        # Handle special value for paraDepth
        paraDepth_value = self.paraDepth_spin.value()
        self.params['paraDepth'] = None if paraDepth_value == 0 else paraDepth_value
        
        self.params['balanceDepth'] = self.balanceDepth_check.isChecked()
        self.params['zWeight'] = self.zWeight_spin.value()
        self.params['lam'] = self.lam_spin.value()
        self.params['maxIter'] = self.maxIter_spin.value()
        self.params['verbose'] = self.verbose_check.isChecked()
        
        return self.params
    
    def runInversion(self):
        """Run the inversion using the current parameters"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "Please load an SGT file first.")
            return
        
        # Get parameters from UI
        params = self.getInversionParams()

        # Check if the parameters are valid
        if np.any(self.refrac_manager.data['t'] < 0):
            # Open a dialog to inform the user about negative times and allow them to proceed with correctTimePicks
            reply = QMessageBox.question(
                self, "Negative Times Detected",
                "Negative times detected in the data. Would you like to correct them before running the inversion?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.correctTimePicks()
                self.showDataTab()
            else:
                return
        
        try:
            # Try to import the inversion manager module
            try:
                from inversion_manager import run_inversion
            except ImportError:
                try:
                    from pyckster.inversion_manager import run_inversion
                except ImportError:
                    QMessageBox.critical(self, "Error", "Could not import inversion_manager module.")
                    return
            
            # Run the inversion
            self.refrac_manager = run_inversion(
                self.refrac_manager,
                params=params
            )
            
            # Display the results
            # self.displayInversionResults()

            self.showModelTab()
            self.showTraveltimesTab()
            self.showSourceReceiverTab()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Inversion failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def displayInversionResults(self):
        """Open the InversionVisualizer to display results"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        try:
            # Try to import the visualizer module
            try:
                from inversion_visualizer import InversionVisualizer
            except ImportError:
                try:
                    from pyckster.inversion_visualizer import InversionVisualizer
                except ImportError:
                    QMessageBox.critical(self, "Error", "Could not import inversion_visualizer module.")
                    return
            
            # Create and show the visualizer window
            visualizer = InversionVisualizer(self.refrac_manager, self.params)
            visualizer.show()
            
            # Keep a reference to prevent garbage collection
            self.visualizer = visualizer
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display results: {str(e)}")
            import traceback
            traceback.print_exc()

    def correctTimePicks(self):
        """Perform time correction on the loaded data"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "Please load an SGT file first.")
            return
        
        try:
            # Try to import the time correction function from inversion_manager
            try:
                from inversion_manager import correct_time_picks
            except ImportError:
                try:
                    from pyckster.inversion_manager import correct_time_picks
                except ImportError:
                    QMessageBox.critical(self, "Error", "Could not import time correction function.")
                    return
            
            # Get parameters from the time correction menu
            min_velocity = self.corr_velocity_spin.value()
            
            # Create a backup of the original data
            original_times = np.copy(self.refrac_manager.data['t'])

            # Apply the time correction with all parameters
            correct_time_picks(
                self.refrac_manager, 
                min_velocity=min_velocity,
            )
            
            # Refresh the visualization
            self.showDataTab()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Time correction failed: {str(e)}")
            import traceback
            traceback.print_exc()

    # Add this method to the StandaloneInversionApp class
    def updateVelocityControls(self):
        """Enable/disable velocity controls based on selected mode"""
        mode = self.velocity_mode_combo.currentData()
        
        # Enable/disable constant velocity control
        self.corr_velocity_spin.setEnabled(mode == "constant")
        
        # Enable/disable surface velocity controls
        self.surf_velocity_smooth_check.setEnabled(mode == "surface")
        self.surf_velocity_window_spin.setEnabled(mode == "surface" and 
                                            self.surf_velocity_smooth_check.isChecked())
        
        # Connect smooth checkbox to window spin state
        self.surf_velocity_smooth_check.stateChanged.connect(
            lambda state: self.surf_velocity_window_spin.setEnabled(
                mode == "surface" and state == Qt.Checked))
        
def launch_inversion_app(picking_data=None, parent_window=None):
    """
    Creates and shows the StandaloneInversionApp window.
    This function does NOT create a QApplication. It assumes one is running.
    """
    # We must store a reference to the window to prevent it from being
    # garbage-collected. Attaching it to the parent is the safest way.
    if parent_window:
        # This is the code path used by Pyckster
        parent_window.inversion_win = StandaloneInversionApp(picking_data, parent=parent_window)
        parent_window.inversion_win.show()
    else:
        # This path is for standalone testing where no parent is provided.
        global standalone_inversion_win
        standalone_inversion_win = StandaloneInversionApp(picking_data)
        standalone_inversion_win.show()

def main():
    """Main function to run the standalone application"""
    app = QApplication(sys.argv)
    # Launch in standalone mode (no data passed)
    launch_inversion_app()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()