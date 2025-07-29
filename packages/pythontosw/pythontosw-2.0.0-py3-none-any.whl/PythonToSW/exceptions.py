"""
----------------------------------------------
PythonToSW: A Python package that allows you to make Stormworks addons with Python.
https://github.com/Cuh4/PythonToSW
----------------------------------------------

Copyright (C) 2025 Cuh4

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# // Main
class PTSException(Exception):
    """
    Base class for all exceptions in PythonToSW.
    """

    def __init__(self, message: str):
        """
        Initializes a new instance of the `PTSException` class.
        
        Args:
            message (str): The error message for the exception.
        """

        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Returns a string representation of the exception.
        """

        return f"PythonToSW Exception: {self.message}"
    
    def __repr__(self):
        """
        Returns a string representation of the exception for debugging.
        """

        return f"PTSException(message={self.message})"