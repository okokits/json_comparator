import json
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.messagebox import showinfo, askyesno

class AppWind(tk.Canvas):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.first_tab()

    def first_tab(self):
        self.window.configure(bg='#f7f7f7')
        self.window.geometry("610x595")
        self.window.resizable(width=False, height=False)

        self.first_path = ""
        self.second_path = ""

        select_paths_label = tk.Label(self.window, text = "Select paths to new and old json files", bg="#f7f7f7", fg="#013332", font=('Helvetica 18 bold'))
        select_paths_label.grid(row = 0, column = 0, pady=80, sticky=tk.EW)
        
        first_path_label = tk.Label(window, text = "Path to new json:", bg="#f7f7f7", fg="#013332", font=('Helvetica 16 bold'))
        first_path_label.grid(row = 1, column = 0, sticky=tk.W, padx=15)

        self.first_file = tk.Button(window, bg="white", fg="black", font=('Helvetica 13'), width=35, anchor='w', command=self.selected_first_file)
        self.first_file.grid(row = 2, padx=10, pady=0, ipady=3, ipadx=132,  column = 0, sticky=tk.W)
        first_file_button = tk.Button(window, text = 'Select File', width=12, bg="#013332", fg="#f7f2f5", font=('Helvetica 13'), command=self.selected_first_file)
        first_file_button.grid(row = 2, column = 0, padx=10, ipady=3, sticky=tk.E)
        
        none_label = tk.Label(window, text = "", bg="#f7f7f7", fg="#013332", font=('Helvetica 16 bold'))
        none_label.grid(row = 3, column = 0, sticky=tk.W, padx=20, pady=10)

        second_path_label = tk.Label(window, text = "Path to old json:", bg="#f7f7f7", fg="#013332", font=('Helvetica 16 bold'))
        second_path_label.grid(row = 4, column = 0, sticky=tk.SW, padx=15)
        
        self.second_file = tk.Button(window, bg="white", fg="black", font=('Helvetica 13'), width=35, anchor='w', command=self.selected_second_file)
        self.second_file.grid(row = 5, padx=10, pady=0, ipady=3, ipadx=132, column = 0, sticky=tk.W)
        second_file_button = tk.Button(window, text = 'Select File', width=12, bg="#013332", fg="#f7f2f5", font=('Helvetica 13'), command=self.selected_second_file)
        second_file_button.grid(row = 5, column = 0, padx=10, ipady=3, sticky=tk.E)

        self.button_next = tk.Button(window, text = 'Next', bg="#013332", fg="#f7f2f5", font=('Helvetica 13'), command=self.json_import, width=12)
        self.button_next.grid(row = 6, column = 0, padx=10, pady=160, ipady=3, sticky=tk.E)
        self.button_next.config(state=DISABLED)

    def selected_first_file(self):
        self.first_path = self.return_path(self.first_file)
        self.enable_next_button()

    def selected_second_file(self):
        self.second_path = self.return_path(self.second_file)
        self.enable_next_button()

    def return_path(self, field_ui):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("json files", "*.json*"), ("all files", "*.*")))
        max_width = 69
        if len(file_path) > max_width:
            path_ui = file_path[:max_width-3] + '...'
        else:
            path_ui = file_path
        field_ui.configure(text=path_ui)
        return file_path

    def enable_next_button(self):
        if self.first_path and self.second_path:
            self.button_next.config(state=NORMAL)
        else:
            self.button_next.config(state=DISABLED)

    def json_import(self):
        self.new_json_path = self.first_path
        self.old_json_path = self.second_path
        try:
            with open(self.new_json_path, 'r') as js1:
                self.js1 = json.load(js1)
            with open(self.old_json_path, 'r') as js2:
                self.js2 = json.load(js2)
                self.second_tab()
        except:
            label_error = tk.Label(window, text = "Please, select valid json files", bg="#f7f7f7", fg="#013332", font=('Helvetica 14 bold'))
            label_error.grid(row = 5, column = 0, columnspan=3, sticky=tk.EW)
        
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
                    self.differences_output.insert("end", f'{self.add1} was added to new json\n')
                    self.found_diff = True
                elif key in value2:
                    self.rem1 = new_path
                    self.differences_output.insert("end", f'{self.rem1} was removed from new json\n')
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
                    self.differences_output.insert("end", f'{self.add2} was added to new json\n')
                    self.found_diff = True
                else:
                    self.rem2 = new_path
                    self.differences_output.insert("end", f'{self.rem2} was removed from new json\n')
                    self.found_diff = True
        #elif value1 != value2:
            #self.differences_output.insert("end", f"{path} has different values: new json has {value1}, old json has {value2}\n")
            #self.found_diff = True

    def identical_check(self):
        self.found_diff = False
        self.check_diff(self.js1, self.js2) 
        if self.found_diff:
            self.enable_apply_changes_button()
            self.scrollbar_listbox(self.differences_output, 11, 1, 5, 75)
        else:
            self.differences_output.insert("end", "There are no differences in json files")

    def iterate_jsons(self, js1, js2):

        changes_from_user = self.input_from_user.get("1.0", tk.END)
        self.listofchangesfromuser = changes_from_user.replace('\n', " ").replace(",", "").split()

        for path in self.listofchangesfromuser:
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
        self.enable_next2_button()
        self.scrollbar_listbox(self.applied_changes,5,6,5,24)

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
                nested_data[(last_key - len(nested_data) + 1)] = value
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
        elif isinstance(nested_data, list) and isinstance(last_key, int):
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

        differences_output_label = tk.Label(window, text="Differences in json files:", bg="#f7f7f7", fg="#013332", font=('Helvetica 14 bold'))
        differences_output_label.grid(row=0, column=0, padx=10, sticky=tk.NW)

        self.differences_output = tk.Listbox(window, height=10, font=('Helvetica 13'), selectbackground="#4b6665", borderwidth=3, highlightthickness=0)
        self.differences_output.bind('<Double-Button-1>', self.callback)
        self.differences_output.grid(row=1, column=0, sticky="ew", padx=10, columnspan=6)

        input_from_user_label = tk.Label(window, text="Which sections do you want to add to/remove from old json?", bg="#f7f7f7", fg="#013332", font=('Helvetica 14 bold'))
        input_from_user_label.grid(row=2, column=0, pady=5, padx=10, sticky=tk.W, columnspan=6)
        
        self.input_from_user = tk.Text(window, height=5, width=48, font=('Helvetica 13'), borderwidth=3, selectbackground="#4b6665")
        self.input_from_user.grid(row=3, column=0, pady=5, padx=10, columnspan=3, sticky=tk.EW)
        self.input_from_user.bind('<FocusOut>', self.stolen_focus)

        self.apply_changes_button = tk.Button(window, text='Apply changes', bg="#013332", fg="#f7f2f5", font=('Helvetica 13'), width=14, command=lambda: self.iterate_jsons(self.js1, self.js2))
        self.apply_changes_button.grid(row=3, column=3, columnspan=3, ipady=5, sticky=tk.W)
        self.apply_changes_button.config(state=DISABLED)

        applied_changes_label = tk.Label(window, text="Applied changes:", bg="#f7f7f7", fg="#013332", font=('Helvetica 14 bold'))
        applied_changes_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.applied_changes = tk.Listbox(window, height=5, width=65, font=('Helvetica 13'), borderwidth=3, selectbackground="#4b6665", highlightthickness=0)
        self.applied_changes.grid(row=6, column=0, padx=10, sticky=tk.W, columnspan=6)

        self.button_next2 = tk.Button(window, text='Next', bg="#013332", fg="#f7f7f7", font=('Helvetica 13'), command=self.third_tab, width=12)
        self.button_next2.grid(row=7, column=4, pady=10, padx=10, ipady=3, sticky=tk.E, columnspan=2)
        self.button_next2.config(state=DISABLED)

        self.identical_check()

    def enable_apply_changes_button(self):
        user_input = self.input_from_user.get("1.0", tk.END).strip()
        if user_input:
            self.apply_changes_button.config(state=NORMAL)
        else:
            self.apply_changes_button.config(state=DISABLED)

    def callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index).split()
            self.input_from_user.insert(tk.END, f'{data[0]} \n')
            self.enable_apply_changes_button()
            self.scrollbar_text(self.input_from_user, 6, 3, 2, 23)
        else:
            pass

    def stolen_focus(self, event):
        self.enable_apply_changes_button()
        self.scrollbar_text(self.input_from_user, 6, 3, 2, 23)

    def scrollbar_text(self, field, sizew, row, column, ipady):
        changesfromuserlist = field.get("1.0", tk.END).splitlines()
        if len(changesfromuserlist) > sizew:
            if not hasattr(self, "field"):
                scrollbar = tk.Scrollbar(window, orient="vertical", command=field.yview)
                scrollbar.grid(row=row, column=column, pady=4, padx=13, ipady=ipady, sticky=tk.E)
                field["yscrollcommand"] = scrollbar.set
        else:
            if hasattr(self, "field"):
                scrollbar.grid_forget()

    def scrollbar_listbox(self, listb, sizew, row, column, ipady):
        if listb.size() > sizew:
            if not hasattr(self, "field"):
                scrollbar = tk.Scrollbar(window, orient="vertical", command=listb.yview, borderwidth=0)
                scrollbar.grid(row=row, column=column, pady=4, ipady=ipady, sticky=tk.E, padx=13)
                listb["yscrollcommand"] = scrollbar.set
        else:
            if hasattr(self, "field"):
                scrollbar.grid_forget()

    def enable_next2_button(self):
        if self.applied_changes.size() > 0:
            self.button_next2.config(state=NORMAL)
        else:
            self.button_next2.config(state=DISABLED)  
    
    def third_tab(self):
        for widget in window.winfo_children():
            widget.destroy()

        json_preview_label = tk.Label(window, text = "JSON preview:", bg="#f7f7f7", fg="#013332", font=('Helvetica 14 bold'))
        json_preview_label.grid(row = 0, column = 0, padx=10, pady=10, sticky=tk.NW)

        json_preview = tk.Text(window, width=65, height=25, font=('Helvetica 13'), borderwidth=3, selectbackground="#4b6665")
        json_preview.grid(row = 1, column = 0, padx=10, sticky=tk.NW)
        pretty_json = json.dumps(self.js2, indent=1)
        json_preview.insert("end", pretty_json)
        self.scrollbar_text(json_preview, 26, 1, 0, 213)

        done_button = tk.Button(window, text = 'Done', bg="#013332", fg="#f7f2f5", font=('Helvetica 13'), command=self.warning_before_closing, width=12)
        done_button.grid(row = 2, column = 0, sticky=tk.SE, ipady=3, padx=10, pady=10)

        back_button = tk.Button(window, text = 'Back', bg="#013332", fg="#f7f2f5", font=('Helvetica 13'),  command=self.second_tab, width=12)
        back_button.grid(row = 2, column = 0, sticky=tk.SW, ipady=3, padx=10, pady=10)

    def warning_before_closing(self):
        result = askyesno(title="Operatiom confirmation", message="Confirm operation?")
        if result: 
            self.applying_changes()
        else: 
            self.third_tab()
        
    def applying_changes(self):    
        try:
            with open(self.old_json_path, 'w') as b:
                json.dump(self.js2, b, indent=1)
        except:
            pass
        window.destroy()

window = tk.Tk()
window.title("JSON Comparator")
comparator = AppWind(window)
window.mainloop()
