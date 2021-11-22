from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

class EditFrame:
    def __init__(self, frame, test):
        self.test = test
        self.edit_frame = frame
        self.edit_frame.title("Edit")
        self.edit_frame.geometry("1280x640")
        self.is_editing = False

        self.edit_frame.protocol("WM_DELETE_WINDOW", self.close_edit_dialog)
        
        self.construct_menu()
        
        self.frame = tk.Frame(self.edit_frame)
        self.frame.pack()
        self.construct_frame(self.frame)
        
    
    ## メニューの構築
    def construct_menu(self):
        self.menuBar = Menu()
        self.editMenu = Menu()
        
        ## 編集メニュー
        self.menuBar.add_cascade(menu=self.editMenu, label="編集(E)", underline=3)
        self.editMenu.add_command(label="保存(S)", underline=3, command=self.save)
        
        self.edit_frame["menu"] = self.menuBar

    ## 画面の基礎を構築
    def construct_frame(self, frame):
        # 前提条件
        prerequisites_frame = tk.Frame(frame)
        prerequisites_frame.grid(row=0)
        prerequisites_button = tk.Button(prerequisites_frame, text="前提条件をコピー")
        prerequisites_button.grid()
        prerequisites_edit = ScrolledText(prerequisites_frame)
        prerequisites_edit.grid(row=1)
        
        test_add_button = tk.Button(prerequisites_frame, text="テストケース追加", command=self.add_test_case)
        test_add_button.grid(row=2, column=0)
        test_remove_button = tk.Button(prerequisites_frame, text="テストケース削除", command=self.remove_test_case)
        test_remove_button.grid(row=2, column=1)
        
        # 実際のテスト
        test_frame = tk.Frame(frame)
        test_frame.grid(row=1)
        scroll = tk.Scrollbar(test_frame, orient=tk.VERTICAL)
        
        
        index = 0
        for test_case in self.test.test_case_list:
            no_label = tk.Label(test_frame, text=test_case.no)
            no_label.grid(row=index, column=0)
            abst_str = ScrolledText(test_frame)
            abst_str.grid(row=index, column=1)
            proc_str = ScrolledText(test_frame)
            proc_str.grid(row=index, column=2)
            expect_str = ScrolledText(test_frame)
            expect_str.grid(row=index, column=3)
            index += 1
        
        
        
        
    def add_test_case(self):
        self.test.add()
        
        children = self.frame.winfo_children()
        for child in children:
            child.destroy()
        self.construct_frame(self.frame)
    
    def remove_test_case(self):
        pass
        
    
    def save(self):
        pass
    
    def close_edit_dialog(self):
        
        # TODO 保存処理をちゃんと作る
        if self.is_editing == True:
            messagebox.showinfo("confirm", "変更があります。保存しますか？")
        
        self.edit_frame.destroy()