"""
Contains the class definition for Config objects.

@license: Apache License 2.0
"""
"""
Copyright (c) Members of the EGEE Collaboration. 2004.
See http://www.eu-egee.org/partners/ for details on the copyright holders.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
"""
Modified by zojeda for mapero project
"""
import os

from ConfigParser import SafeConfigParser
from ConfigParser import ParsingError

class Config(object):
    """
    Class definition for a dashboard Config object.
    
    Current version looks for the config file in ''.
    
    @author: Ricardo Rocha <ricardo.rocha@cern.ch>
    @version: $Id: Config.py,v 1.4 2007/05/04 17:27:00 rocha Exp $
    """
    
    """
    Class static logger object.
    """
#    _logger = logging.getLogger("dashboard.dao.Config")

    """
    Holds the singleton reference.
    """
    _instance = None
    
    """
    Service configuration objects.
    """
    _configs = {}

    def __new__(cls):
        """
        Invoked on every class instance creation.
        
        Makes sure that only one instance of this class ever exists.
        
        @return: A reference to the class singleton
        """
        if not cls._instance:
            cls._instance = object.__new__(cls)
#            cls._logger.debug("Created new Config instance.")            
        return cls._instance

    def __init__(self):
        """
        Object constructor.
        
        As this is a singleton, nothing is put in here (otherwise it would
        be constantly called).
        """
        pass
    
    def getConfig(self, packageName):
        """
        Returns a reference to the configuration object for the given package.
        
        @param packageName: The name of the package for which to retrieve the configuration
        
        @return: A reference to the config object of the requested package
        """
        # Return the config immediately if we already have one for this package
        if not self._configs.has_key(packageName):
            
            # Parse the env configured mapero home directories
            maperoHome = os.environ.get("MAPERO_HOME")
            maperoHomeDirs = []
            if maperoHome is not None:
                maperoHomeDirs = maperoHome.split(":")
                
            configFiles = []
            
            # Load the system config files
            configFiles.extend(["/opt/mapero/etc/mapero.cfg",
                                "/opt/mapero/etc/%s/%s.cfg" % (packageName, packageName)])
            
            # Load the user config files
            configFiles.extend([os.path.expanduser("~/.mapero/etc/mapero.cfg"),
                                os.path.expanduser("~/.mapero/etc/%s/%s.cfg" 
                                                   % (packageName, packageName))])
            
            # Load the environment set config files
            for i in range(0, len(maperoHomeDirs)):
                configFiles.extend(["%s/etc/mapero.cfg" % maperoHomeDirs[len(maperoHomeDirs)-i-1],
                                    "%s/etc/%s/%s.cfg" % (maperoHomeDirs[len(maperoHomeDirs)-i-1], 
                                                          packageName, packageName)])
                
            config = SafeConfigParser()
            try:
                config.read(configFiles)
                self._configs[packageName] = config
            except ParsingError, msg:
                # TODO: We need to log the exception somewhere
                # Problem is without loading the config we have no logger
                return None

        return self._configs[packageName]