import datetime
import os
import subprocess
import time
import sublime
import sublime_plugin

settings = sublime.load_settings('pman.sublime-settings')

class Pref:
    @staticmethod
    def load():
        Pref.show_debug = settings.get('show_debug', False)
        Pref.pman_executable_path = settings.get('pman_executable_path', 'pman')
        Pref.pman_col_executable_path = settings.get('pman_col_executable_path', 'col')

Pref.load()

[settings.add_on_change(setting, Pref.load) for setting in [
    'show_debug',
    'pman_executable_path',
    'pman_col_executable_path']]


def debug_message(msg):
    """Debug functionality"""
    if Pref.show_debug == True:
        print "[pman] " + msg


class PmanCommand():
    """Class to represent the wrapper around pman command line application"""
    def __init__(self, entity):
        self.entity = entity

    def execute(self):
        pmanCmd = [Pref.pman_executable_path]
        pmanCmd.append(self.entity)
        colCmd = [Pref.pman_col_executable_path]
        colCmd.append('-b')

        debug_message(' '.join(pmanCmd))
        debug_message(' '.join(colCmd))

        pman = subprocess.Popen(pmanCmd, stdout=subprocess.PIPE)
        col = subprocess.Popen(colCmd, stdout=subprocess.PIPE, stdin=pman.stdout)

        data = None
        if col.stdout:
            data = col.communicate()[0]

        return data


class BasePman(sublime_plugin.TextCommand):
    """Base class for pman functionality"""
    def execute(self, keyword):
        data = PmanCommand(keyword).execute()

        if data == '':
            sublime.error_message('There is no manual entry for "' + keyword + '"')
        else:
            self.render(keyword, data)

    def render(self, keyword, output):
        try:
            output = output.decode('utf-8')
        except UnicodeDecodeError:
            output = output.decode(sublime.active_window().active_view().settings().get('fallback_encoding'))

        self.output_view = sublime.active_window().get_output_panel("pman")
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        region = sublime.Region(0, self.output_view.size())
        self.output_view.erase(edit, region)
        self.output_view.insert(edit, 0, output)
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)
        sublime.active_window().run_command("show_panel", {"panel": "output.pman"})


class PmanManualForKeywordCommand(BasePman):
    """Command to take entered input and run through pman"""
    def run(self, args):
        sublime.active_window().show_input_panel('Keyword', '', self.execute, None, None)


class PmanManualForSelectionCommand(BasePman):
    """Command to take the selection and run through pman"""
    def run(self, args):
        for region in self.view.sel():
            word = self.view.word(region)
            if not word.empty():
                keyword = self.view.substr(word)
                self.execute(keyword)
