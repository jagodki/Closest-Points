# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ClosestPoints
                                 A QGIS plugin
 This plugin extracts the closests points.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-10-27
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Christoph Jung
        email                : jagodki.cj@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.core import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .closest_points_dialog import ClosestPointsDialog
import os.path
import processing

#import own classes
from .processing_provider import *


class ClosestPoints:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ClosestPoints_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Closest Points')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        
        #declare additional instance vars
        self.provider = ClosestPointsProvider()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ClosestPoints', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        # self.add_action(
            # icon_path,
            # text=self.tr(u'Find closest point for each feature'),
            # callback=self.runFindClosestPoint,
            # parent=self.iface.mainWindow(),
            # add_to_toolbar = False)
            
        #create actions
        icon_closest_point = QIcon(':/plugins/closest_points/icons/closest_point_icon.png')
        action_closest_point = QAction(icon_closest_point, 'Find closest point for each feature', self.iface.mainWindow())
        action_closest_point.setObjectName('find_closest_point')
        action_closest_point.triggered.connect(self.runFindClosestPoint)
        self.actions.append(action_closest_point)
        self.iface.addPluginToVectorMenu(self.menu, action_closest_point)
        
        icon_closest_point = QIcon(':/plugins/closest_points/icons/all_closest_points_icon.png')
        action_all_closest_points = QAction(icon_closest_point, 'Find all closest points for each feature', self.iface.mainWindow())
        action_all_closest_points.setObjectName('find_all_closest_points')
        action_all_closest_points.triggered.connect(self.runFindAllClosestPoints)
        self.actions.append(action_all_closest_points)
        self.iface.addPluginToVectorMenu(self.menu, action_all_closest_points)

        # will be set False in run()
        self.first_start = True
        
        #add the processing provider
        QgsApplication.processingRegistry().addProvider(self.provider)

    def runFindClosestPoint(self):
        processing.execAlgorithmDialog('find_closest_points:find_closest_point', {})

    def runFindAllClosestPoints(self):
        processing.execAlgorithmDialog('find_closest_points:find_all_closest_points', {})
    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(self.menu, action)
            #self.iface.removeToolBarIcon(action)
        
        #remove the processing provider
        QgsApplication.processingRegistry().removeProvider(self.provider)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ClosestPointsDialog()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
