import json
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog

class AppWind(tk.Canvas):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.first_tab()

    def first_tab(self):
        self.window.configure(bg='#f7f7f7')
        self.window.geometry("650x400")
        self.window.resizable(width=False, height=False)

        select_paths_label = tk.Label(self.window, text = "Select paths to new and old json files", bg="#f7f7f7", fg="#4f0131", font=('Helvetica 18 bold'))
        select_paths_label.grid(row = 0, column = 0, columnspan=3, ipady=57, ipadx=100, sticky=tk.EW)
        
        first_path_label = tk.Label(window, text = "Path to new json:", bg="#f7f7f7", fg="#4f0131", font=('Helvetica 14'))
        second_path_label = tk.Label(window, text = "  Path to old json:", bg="#f7f7f7", fg="#4f0131", font=('Helvetica 14'))
        first_path_label.grid(row = 1, column = 0, sticky=tk.E)
        second_path_label.grid(row = 2, column = 0, pady=20, sticky=tk.E)

        self.first_path = tk.Button(window, bg="white", fg="black", font=('Helvetica 13'), width=35, anchor='w', command=lambda: self.return_path(self.first_path))
        self.second_path = tk.Button(window, bg="white", fg="black", font=('Helvetica 13'), width=35, anchor='w', command=lambda: self.return_path(self.second_path))
        self.first_path.grid(row = 1, column = 1, sticky=tk.EW)
        self.second_path.grid(row = 2, column = 1, sticky=tk.EW, pady=20)

        first_path_button = tk.Button(window, text = 'Select File', bg="#4f0131", fg="#f7f2f5", font=('Helvetica 13'), command=lambda: self.return_path(self.first_path))
        second_path_button = tk.Button(window, text = 'Select File', bg="#4f0131", fg="#f7f2f5", font=('Helvetica 13'), command=lambda: self.return_path(self.second_path))
        first_path_button.grid(row = 1, column = 2, sticky=tk.EW)
        second_path_button.grid(row = 2, column = 2, pady=20, sticky=tk.EW)

        self.button_next = tk.Button(window, text = 'Next', bg="#4f0131", fg="#f7f2f5", font=('Helvetica 13'), command=self.json_import, width=12)
        self.button_next.place(x=521,y=355)
        self.button_next.config(state=DISABLED)

    def path_to_file(self, file, text):
        max_width = 42
        if len(text) > max_width:
            text = text[:max_width-3] + '...'
        file.configure(text=text)
        self.enable_next_button()

    def return_path(self, file):
        self.file_path = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("json files", "*.json*"), ("all files", "*.*")))
        self.path_to_file(file, self.file_path)

    def enable_next_button(self):
        if self.first_path.cget("text") and self.second_path.cget("text"):
            self.button_next.config(state=NORMAL)
        else:
            self.button_next.config(state=DISABLED)

    def json_import(self):
        self.new_json_path = self.first_path.cget("text")
        self.old_json_path = self.second_path.cget("text")
        try:
            with open(self.new_json_path, 'r') as js1:
                self.js1 = json.load(js1)
            with open(self.old_json_path, 'r') as js2:
                self.js2 = json.load(js2)
                self.second_tab()
        except:
            label_error = tk.Label(window, text = "Please, select valid json files", bg="white smoke", fg="#3b0137", font=('Helvetica 14'))
            label_error.grid(row = 3, column = 0, columnspan=3, sticky=tk.EW)

    def sorted_list(self, value):
        if all(isinstance(x, (int, str)) for x in value):
            value = sorted(value)
        else:
            value = value
        return value

    def check_diff(self, value1, value2, path=''):
        if isinstance(value1, dict) and isinstance(value2, dict):
            all_keys = set(value1.keys()).union(set(value2.keys()))
            for key in all_keys:
                if path:
                    new_path = f"{path}.{key}"
                else:
                    new_path = key
                if key in value1 and key in value2:
                    self.check_diff(value1[key], value2[key], new_path)
                elif key in value1:
                    self.add1 = new_path
                    self.differences_output.insert("end", f'{self.add1} was added to new json \n')
                    self.found_diff = True
                elif key in value2:
                    self.rem1 = new_path
                    self.differences_output.insert("end", f'{self.rem1} was removed from new json \n')
                    self.found_diff = True
        elif isinstance(value1, list) and isinstance(value2, list):
            value1 = self.sorted_list(value1)
            value2 = self.sorted_list(value2)
            len1, len2 = len(value1), len(value2)
            max_len = max(len1, len2)
            for index in range(max_len):
                new_path = f"{path}.{index}"
                if index < len1 and index < len2:
                    self.check_diff(value1[index], value2[index], new_path)
                elif index < len1:
                    self.add2 = new_path
                    self.differences_output.insert("end", f'{self.add2} was added to new json \n')
                    self.found_diff = True
                else:
                    self.rem2 = new_path
                    self.differences_output.insert("end", f'{self.rem2} was removed from new json \n')
                    self.found_diff = True
        elif value1 != value2:
            self.differences_output.insert("end", f"Different values in {path}: new json has {value1}, old json has {value2} \n")
            self.found_diff = True

    def identical_check(self):
        self.found_diff = False
        self.check_diff(self.js1, self.js2) 
        if self.found_diff:
            self.apply_changes_button.config(state=NORMAL)
        else:
            self.differences_output.insert("end", "There are no differences in json files")
            self.apply_changes_button.config(state=DISABLED)

    def iterate_jsons(self, js1, js2):

        changes_from_user = self.input_from_user.get("1.0", tk.END)
        changes_from_user = changes_from_user.split()

        for path in changes_from_user:
            path = path.strip()
            if not path:
                continue
            value_from_js1 = self.get_nested_item(js1, path)
            value_from_js2 = self.get_nested_item(js2, path)

            if value_from_js1 is not None and value_from_js2 is None:
                self.adding_sections(self.js2, path, value_from_js1)
                self.applied_changes.insert("end", f"Added section: {path}")
            elif value_from_js1 is None and value_from_js2 is not None:
                self.removing_sections(self.js2, path)
                self.applied_changes.insert("end", f"Removed section: {path}")
            elif value_from_js1 is not None and value_from_js2 is not None:
                self.applied_changes.insert("end", f"{path} exists in both jsons")
            elif value_from_js1 is None and value_from_js2 is None:
                self.applied_changes.insert("end", f"{path} doesn't exist in both jsons")
                
        self.applying_changes()

    def int_key(self, key):
        if key.isdigit():
            key = int(key)
        else:
            key = key
        return key

    def get_nested_item(self, data, path):
        keys = path.split('.')
        for key in keys:
            key = self.int_key(key)
            if isinstance(data, dict):
                data = data.get(key, None)
            elif isinstance(data, list) and isinstance(key, int):
                if 0 <= key < len(data):
                    data = data[key]
                else:
                    return None
            else:
                return None
        return data

    def keys_processing(self, data, path):
        keys = path.split('.')
        nested_data = data
        for key in keys:
            key = self.int_key(key)
            if isinstance(nested_data, dict):
                if key not in nested_data:
                    if isinstance(key, (dict, list)):
                        nested_data[key] = {}  
                    else:
                        nested_data[key] = []
                nested_data = nested_data[key]
            elif isinstance(nested_data, list) and isinstance(key, int):
                while len(nested_data) <= key:
                    nested_data.append(None)
                nested_data = nested_data[key]
            else:
                raise ValueError(f"Invalid path or type mismatch at key: {key}")

    def adding_sections(self, data, path, value):
        self.keys_processing(data, path)
        nested_data = data
        keys = path.split('.')
        last_key = keys.pop()
        last_key = self.int_key(last_key)
        for key in keys:
            key = self.int_key(key)
            nested_data = nested_data[key] 

        if isinstance(nested_data, dict):
            nested_data[last_key] = value
        elif isinstance(nested_data, list) and isinstance(last_key, int):
            if last_key < len(nested_data):
                nested_data[last_key] = value
            else:
                nested_data.extend([None] * (last_key - len(nested_data) + 1))
                nested_data[last_key] = value
        else:
            raise ValueError("Invalid path or type mismatch at last key")
    
    def removing_sections(self, data, path):
        self.keys_processing(data, path)
        nested_data = data
        keys = path.split('.')
        last_key = keys.pop()
        last_key = self.int_key(last_key)
        for key in keys:
            key = self.int_key(key)
            nested_data = nested_data[key] 
        if isinstance(nested_data, dict):
            if last_key in nested_data:
                del nested_data[last_key]
        elif isinstance(nested_data, list) and last_key.isdigit():
            last_key = int(last_key)
            if 0 <= last_key < len(nested_data):
                del nested_data[last_key]
            else:
                del nested_data[last_key]       
        else:
            raise ValueError("Invalid path or type mismatch at last key")


    def second_tab(self):
        for widget in window.winfo_children():
            widget.destroy()
        window.geometry("650x500")
        differences_output_label = tk.Label(window, text = "Differences in json files:", bg="#f7f7f7", fg="#4f0131", font=('Helvetica 14 bold'))
        differences_output_label.grid(row = 0, column = 0, padx=10, pady=10, sticky=tk.NW)
        
        self.differences_output = tk.Text(window, width=60, height=10, font=('Helvetica 13'), borderwidth=2)
        self.differences_output.grid(row = 1, column = 0, columnspan=3, padx=10, sticky=tk.EW)
        
        input_from_user_label = tk.Label(window, text = "Which sections do you want to add to old json?", bg="#f7f7f7", fg="#4f0131", font=('Helvetica 14 bold'))
        input_from_user_label.grid(row = 2, column = 0, pady=5, padx=10, sticky=tk.NW)
        
        self.input_from_user = tk.Text(window, height=3, width=54, font=('Helvetica 13'), borderwidth=2)
        self.input_from_user.grid(row = 3, column = 0, pady=5, padx=10, sticky=tk.EW)

        self.apply_changes_button = tk.Button(window, text = 'Apply \n changes', bg="#4f0131", fg="#f7f2f5", font=('Helvetica 13'), width=12, height=2, command=lambda: self.iterate_jsons(self.js1, self.js2))
        self.apply_changes_button.grid(row = 3, column = 1, sticky=tk.EW, ipady=3, padx=10)

        applied_changes_label = tk.Label(window, text = "Applied changes:", bg="#f7f7f7", fg="#4f0131", font=('Helvetica 14 bold'))
        applied_changes_label.grid(row = 5, column = 0, columnspan=2, padx=10, pady=5, sticky=tk.NW)
        self.applied_changes = tk.Listbox(window, width=60, height=4, font=('Helvetica 13'), borderwidth=2)
        self.applied_changes.grid(row = 6, column = 0, padx=10, columnspan=3, sticky=tk.EW)

        self.identical_check()
        self.differences_output.config(state="disabled")

        self.iterate_jsons(self.js1, self.js2)

        
    def applying_changes(self):    
        try:
            with open(self.old_json_path, 'w') as b:
                json.dump(self.js2, b, indent=4)
        except (FileNotFoundError, NameError):
            pass

window = tk.Tk()
window.title("JSON Comparator")
comparator = AppWind(window)
window.mainloop()



 
