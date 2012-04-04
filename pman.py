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
        Pref.bash_executable_path = settings.get('bash_executable_path', 'sh')
        Pref.pman_executable_path = settings.get('pman_executable_path', 'pman')
        Pref.pman_additional_args = settings.get('pman_additional_args', {})

Pref.load()

[settings.add_on_change(setting, Pref.load) for setting in [
    'show_debug',
    'bash_executable_path',
    'pman_additional_args',
    'pman_executable_path']]


def debug_message(msg):
    """Debug functionality"""
    if Pref.show_debug == True:
        print "[pman] " + msg


class PmanCommand():
    """Class to represent the wrapper around pman command line application"""
    def __init__(self, entity):
        self.entity = entity

    def execute(self):
        cmd = [Pref.bash_executable_path]
        cmd.append('-c')
        cmd.append(Pref.pman_executable_path + ' ' + self.entity + ' | ' + 'col -b')

        for key, value in Pref.pman_additional_args.items():
            arg = key
            if value != "":
                arg += "=" + value
            cmd.append(arg)

        debug_message(' '.join(cmd))

        shell = sublime.platform() == "windows"
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)

        data = None
        if proc.stdout:
            data = proc.communicate()[0]

        return data


class PmanManualCommand(sublime_plugin.TextCommand):
    """Consult the manual command from the editor"""
    def run(self, args):
        for region in self.view.sel():
            word = self.view.word(region)
            if not word.empty():
                keyword = self.view.substr(word)
                data = PmanCommand(keyword).execute()
                self.render(keyword, data)

    def render(self, keyword, output):
        try:
            output = output.decode('utf-8')
        except UnicodeDecodeError:
            output = output.decode(sublime.active_window().active_view().settings().get('fallback_encoding'))

        scratch_file = sublime.active_window().new_file()
        scratch_file.set_name('PHP Manual - ' + keyword)
        scratch_file.set_scratch(True)
        edit = scratch_file.begin_edit()
        scratch_file.insert(edit, 0, output)
        scratch_file.end_edit(edit)
        scratch_file.set_read_only(True)