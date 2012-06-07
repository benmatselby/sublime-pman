Sublime Pman (PHP Manual) Plugin
================================

This plugin adds context menus for consulting the php manual from within the editor (pman)

Installation
------------

Use Sublime Text 2's [Package Control](http://wbond.net/sublime_packages/package_control) (Preferences -> Package Control -> Install Package -> Pman) to install this plugin.

Or

Simply checkout the git repo into “~/Library/Application Support/Sublime Text 2/Packages/Pman or the equivalent folder on Windows or Linux.


Overview
--------

This plugin adds support for running pman from within the editor

You can do this from:

* The Command Palette ('Pman')
* Right-click in the editor
* F1 on the keyboard (configurable)

It enables you to:

* Run the pman command for the selected word or the word where the cursor is currently pointing
* Ask the user for input to then run through the pman command


Configuration
-------------

You can configure:

* show_debug - Do you want the debug information to be sent to the console?
* bash_executable_path - The path to the bash executable. If empty string, use PATH to find it
* pman_executable_path - The path to the pman executable. If empty string, use PATH to find it
* pman_additional_args - This is the extra information you want to pass to the pman command.
* use_output_panel - Show manual in an output panel instead of a scratch buffer


Requirements
------------

Requirements for this plugin:

* pman installed
* Python 2.6
* Linux/Mac OS X

