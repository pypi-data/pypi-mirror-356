import os
import io
import tempfile
import subprocess
import zipfile
import shutil
import IPython

import crtomo

import numpy as np
import ipywidgets as widgets
from IPython.display import display
import shapely
import shapely.plotting
import matplotlib.pyplot as plt


class crtomo_mesh_mgr(object):
    def __init__(self, electrode_positions, local_tmp,
                 dgps_manager_instance, output=None):
        """
        Parameters
        ----------
        electrode_positions: numpy.ndarray (Nx2)
            The electrode positions in 2D.
        local_tmp: str (optional, default: None)
            Certain actions require temporary directories accessible from the
            jupyter interface.
        output: ipywidgets.widgets.Output (Optional)
            If provided, output widgets into this output widget.

        """
        self.electrode_positions = electrode_positions
        self.local_tmp = local_tmp
        self.dgps_manager_instance = dgps_manager_instance

        # compute a few parameters
        self.distance_x = np.abs(
            self.electrode_positions[:, 0].max(
            ) - self.electrode_positions[:, 0].min()
        )
        self.distance_z = np.abs(
            self.electrode_positions[:, 1].max(
            ) - self.electrode_positions[:, 1].min()
        )
        self.distances = np.sqrt(
            (self.electrode_positions[1:, 0] -
             self.electrode_positions[:-1, 0]) ** 2 +
            (self.electrode_positions[1:, 1] -
             self.electrode_positions[:-1, 1]) ** 2
        )

        self.eldist_min = self.distances.min()
        self.eldist_max = self.distances.max()

        self.mesh = None
        self.gui = []

        if output is None:
            self.output = widgets.Output()
        else:
            self.output = output

        # used to plot the geometry
        self.output_geometry = widgets.Output()
        # used to plot the mesh
        self.output_mesh = widgets.Output()
        self.output_links = widgets.Output()

        self._build_widgets()

    def on_widget_changed(self, change):
        self.plot_geometry()

    def _build_widgets(self):

        offset_x = self.distance_x / 3.0
        offset_z = self.distance_x / 2.0

        loc_precision = 3
        self.widgets = {
            'but_gen_mesh': widgets.Button(
                description='Generate Mesh',
                style={'description_width': 'initial'},
            ),
            'upper_left_x': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[0, 0] - offset_x,
                    loc_precision,
                ),
                step=0.5,
                description='Upper left corner (X):',
                style={'description_width': 'initial'},
            ),
            'upper_left_z': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[0, 1],
                    loc_precision,
                ),
                step=0.5,
                description='Upper left corner (Z):',
                style={'description_width': 'initial'},
            ),
            'lower_left_x': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[0, 0] - offset_x,
                    loc_precision,
                ),
                step=0.5,
                description='Lower left corner (X):',
                style={'description_width': 'initial'},
            ),
            'lower_left_z': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[:, 0].min() - offset_z,
                    loc_precision,
                ),
                step=0.5,
                description='Lower left corner (Z):',
                style={'description_width': 'initial'},
            ),
            'upper_right_x': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[-1, 0] + offset_x,
                    loc_precision,
                ),
                step=0.5,
                description='Upper right corner (X):',
                style={'description_width': 'initial'},
            ),
            'upper_right_z': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[-1, 1],
                    loc_precision,
                ),
                step=0.5,
                description='Upper right corner (Z):',
                style={'description_width': 'initial'},
            ),
            'lower_right_x': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[-1, 0] + offset_x,
                    loc_precision,
                ),
                step=0.5,
                description='Lower right corner (X):',
                style={'description_width': 'initial'},
            ),
            'lower_right_z': widgets.FloatText(
                value=np.round(
                    self.electrode_positions[:, 0].min() - offset_z,
                    loc_precision,
                ),
                step=0.5,
                description='Lower right corner (Z):',
                style={'description_width': 'initial'},
            ),
            'char_length_1': widgets.FloatText(
                value=np.round(self.eldist_min / 3.0, 4),
                step=0.1,
                description='Size at electrodes:',
                style={'description_width': 'initial'},
            ),
            'char_length_2': widgets.FloatText(
                value=np.round(self.eldist_min, 4),
                step=0.1,
                description='Size at boundaries:',
                style={'description_width': 'initial'},
            ),
        }
        self.widgets['but_gen_mesh'].on_click(self.generate_mesh)

        self.widgets['upper_left_x'].observe(
            self.on_widget_changed, names='value')
        self.widgets['upper_left_z'].observe(
            self.on_widget_changed, names='value')
        self.widgets['lower_left_x'].observe(
            self.on_widget_changed, names='value')
        self.widgets['lower_left_z'].observe(
            self.on_widget_changed, names='value')

        self.widgets['upper_right_x'].observe(
            self.on_widget_changed, names='value')
        self.widgets['upper_right_z'].observe(
            self.on_widget_changed, names='value')
        self.widgets['lower_right_x'].observe(
            self.on_widget_changed, names='value')
        self.widgets['lower_right_z'].observe(
            self.on_widget_changed, names='value')

        gui = widgets.VBox([
            widgets.HBox([
                widgets.VBox(
                    [
                        widgets.HBox([
                            self.widgets['upper_left_x'],
                            self.widgets['upper_left_z'],
                        ]),
                        widgets.HBox([
                            self.widgets['lower_left_x'],
                            self.widgets['lower_left_z'],
                        ]),
                        widgets.HBox([
                            self.widgets['upper_right_x'],
                            self.widgets['upper_right_z'],
                        ]),
                        widgets.HBox([
                            self.widgets['lower_right_x'],
                            self.widgets['lower_right_z'],
                        ]),
                        widgets.HBox([
                            self.widgets['char_length_1'],
                            self.widgets['char_length_2'],
                        ]),
                        self.widgets['but_gen_mesh'],
                    ]
                ),
                self.output_geometry,
            ]),
            self.output_mesh,
            self.output_links,
        ])
        self.gui = gui

    def show(self):
        self.output.clear_output()
        with self.output:
            display(self.gui)
        display(self.output)
        self.plot_geometry()

    def plot_geometry(self):
        with plt.ioff():
            fig, ax = plt.subplots()

            points_all = [
                [self.widgets[
                    'upper_left_x'].value, self.widgets['upper_left_z'].value],
            ]
            for electrode in self.electrode_positions:
                points_all += [electrode]

            points_all += [
                [self.widgets['upper_right_x'].value,
                 self.widgets['upper_right_z'].value],
                [self.widgets['lower_right_x'].value,
                 self.widgets['lower_right_z'].value],
                [self.widgets['lower_left_x'].value,
                 self.widgets['lower_left_z'].value],
            ]
            polygon = shapely.geometry.Polygon(points_all)
            self.polygon = polygon

            shapely.plotting.plot_polygon(polygon, ax=ax, linestyle='-')
            if polygon.is_simple:
                ax.set_title('Geometry looks valid!', loc='left')

            ax.scatter(
                self.electrode_positions[:, 0],
                self.electrode_positions[:, 1],
                label='electrodes',
                s=200,
                color='k',
            )
            # outer mesh corners
            ax.scatter(
                self.widgets['upper_left_x'].value,
                self.widgets['upper_left_z'].value,
                label='upper left',
                s=200,
            )
            ax.scatter(
                self.widgets['lower_left_x'].value,
                self.widgets['lower_left_z'].value,
                label='lower left',
                s=200,
            )
            ax.scatter(
                self.widgets['upper_right_x'].value,
                self.widgets['upper_right_z'].value,
                label='upper right',
                s=200,
            )
            ax.scatter(
                self.widgets['lower_right_x'].value,
                self.widgets['lower_right_z'].value,
                label='lower right',
            )

            ax.legend()
            ax.grid()
            self.output_geometry.clear_output()
            with self.output_geometry:
                display(fig)
            del (fig)

    def generate_mesh(self, button):
        print('Generating mesh')
        self.widgets[
            'but_gen_mesh'
        ].description = 'Generating mesh...please wait'

        # here we create the mesh
        tempdir = tempfile.mkdtemp(
            prefix='dgps_manager_tmp_meshdir_'
        )
        # tempdir = 'tmp'
        print('PWD', os.getcwd())
        np.savetxt(
            tempdir + os.sep + 'electrodes.dat',
            self.electrode_positions, fmt='%.4f %.4f'
        )

        # generate simple boundaries with Neumann (type 12) boundaries at the
        # top and mixed-boundaries (type 11) at the remaining three sides
        with open(tempdir + os.sep + 'boundaries.dat', 'w') as fid:
            fid.write('{:.4f} {:.4f} {}\n'.format(
                self.widgets['upper_left_x'].value,
                self.widgets['upper_left_z'].value,
                12
            ))
            for electrode in self.electrode_positions:
                fid.write('{:.4f} {:.4f} {}\n'.format(
                    *electrode, 12
                ))
            fid.write('{:.4f} {:.4f} {}\n'.format(
                self.widgets['upper_right_x'].value,
                self.widgets['upper_right_z'].value,
                11
            ))
            fid.write('{:.4f} {:.4f} {}\n'.format(
                self.widgets['lower_right_x'].value,
                self.widgets['lower_right_z'].value,
                11
            ))
            fid.write('{:.4f} {:.4f} {}\n'.format(
                self.widgets['lower_left_x'].value,
                self.widgets['lower_left_z'].value,
                11
            ))

        with open(tempdir + os.sep + 'char_length.dat', 'w') as fid:
            fid.write('{:.4f}\n'.format(
                self.widgets['char_length_1'].value
            ))
            fid.write('{:.4f}\n'.format(
                self.widgets['char_length_2'].value
            ))
            # repeat the previous values two times for extra lines and nodes,
            # which we do not use here
            fid.write('{:.4f}\n'.format(
                self.widgets['char_length_2'].value
            ))
            fid.write('{:.4f}\n'.format(
                self.widgets['char_length_2'].value
            ))

        pwd = os.getcwd()
        print('PWD1', pwd)
        os.chdir(tempdir)
        try:
            subprocess.call('cr_trig_create grid', shell=True)
        except Exception:
            print('Caught an exception while calling cr_trig_create')
            os.chdir(pwd)
            return
        os.chdir('grid')
        self.mesh = crtomo.crt_grid()
        os.chdir(pwd)
        self.plot_mesh()

        # now we generate a zip file of the directory
        filenames = []
        for root, dirs, files in os.walk(tempdir):
            # level = root.replace('.', '').count(os.sep)
            filenames += [root + os.sep + file for file in files]
        buffer = io.BytesIO()
        nzip = zipfile.ZipFile(buffer, mode='w')
        for filename in filenames:
            nzip.write(filename)
        nzip.close()
        buffer.seek(0)
        self.mesh_dir_zip = buffer

        self.output_links.clear_output()

        # juypter does not allow us to directly link to the temporary directory
        # (most probably somewhere in /tmp)
        # We therefore create a new tmp directory in an accessible location
        # We call this the 'local_tmp' directory

        tmp_dir_2 = tempfile.mkdtemp(
            prefix='dgps_manager_dl_',
            dir=self.local_tmp
        )
        with self.output_links:
            display(
                widgets.HTML(
                    ''.join((
                        'Created temporary directory: {} '.format(tmp_dir_2),
                        '<br />',
                        'This directory is used to provide downloadable files',
                        '<br />',
                        'After downloading, you can delete this directory',
                        '<br />',
                        '<h3>For download, use the middle mouse button to ',
                        'open the link in a new tab! </h3>',
                    ))
                )
            )

        # save the zip blob
        zip_blob = tmp_dir_2 + os.sep + 'cr_trig_create_directory.zip'
        with open(zip_blob, 'wb') as fid:
            fid.write(buffer.read())

        file_list = [
            tempdir + os.sep + 'grid' + os.sep + 'elem.dat',
            tempdir + os.sep + 'grid' + os.sep + 'elec.dat',
            zip_blob,
        ]

        # save logs/coordinates
        filename = tmp_dir_2 + os.sep + 'gps_processing_log.log'
        with open(filename, 'w') as fid:
            fid.write(self.dgps_manager_instance._get_activity_log_as_str())
        file_list += [filename]

        filename = tmp_dir_2 + os.sep + 'gps_coordinates.dat'
        with open(filename, 'w') as fid:
            fid.write(
                self.dgps_manager_instance.get_active_gps_coordinates_as_str()
            )
        file_list += [filename]

        filename = tmp_dir_2 + os.sep + 'electrode_processing.log'
        with open(filename, 'w') as fid:
            el_manager = self.dgps_manager_instance.el_manager
            fid.write(
                el_manager.log_handler.get_str_formatting()
            )
        file_list += [filename]

        filename = tmp_dir_2 + os.sep + 'electrode_coords.dat'
        with open(filename, 'w') as fid:
            el_manager = self.dgps_manager_instance.el_manager
            fid.write(
                el_manager._get_elec_coords_str()
            )
        file_list += [filename]

        # get element count
        with open(file_list[0], 'r') as fid:
            # ignore first line
            fid.readline()
            _, self.triangle_count, _ = np.fromstring(
                fid.readline().strip(),
                sep=' ',
                dtype=int,
            )
            with self.output_links:
                print('The resulting mesh has {} triangles.\n'.format(
                    self.triangle_count
                ))

        with open(file_list[1], 'r') as fid:
            self.electrode_count = int(fid.readline().strip())
            with self.output_links:
                print('The resulting mesh has {} electrodes.\n'.format(
                    self.electrode_count
                ))

        for file in file_list:
            filename = file
            if os.path.isfile(filename):
                target_file = tmp_dir_2 + os.sep + os.path.basename(file)
                if not os.path.isfile(target_file):
                    # copy only if the target file is not already present
                    shutil.copy(filename, target_file)
                with self.output_links:
                    display(
                         IPython.display.FileLink(
                             os.path.relpath(
                                target_file,
                                os.getcwd()
                             )
                         )
                    )
            else:
                print('TARGET does not exist:', filename)

        with self.output_links:
            display(
                widgets.HTML(
                    ''.join((
                        '<h3>Make sure to also save the logs/coordinates ' +
                        'along the electrical raw data, and add required ' +
                        'information to the metadata.ini file(s)!</h3>'
                    ))
                )
            )
        self.widgets[
            'but_gen_mesh'
        ].description = 'Generate new mesh'

    def plot_mesh(self):
        if self.mesh is None:
            return
        with plt.ioff():
            fig, ax = plt.subplots()
            self.mesh.plot_grid_to_ax(ax)
        with self.output_mesh:
            self.output_mesh.clear_output()
            display(fig)
