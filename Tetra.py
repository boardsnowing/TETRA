from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter as tk

import TestList, EditFrame

import os, sys

class Tetra:
    def __init__(self, root) -> None:
        root.title("Tetra")
        windowWidth  = 320
        windowHeight = 300
        root.protocol("WM_DELETE_WINDOW", self.exitMenu)
        
        root.geometry(str(windowWidth) + "x" + str(windowHeight))
        
        # tearOffを無効化
        root.option_add("*tearOff", FALSE)

        # テストを生成
        self.test = TestList.TestList()
        
        # メニューバー表示
        self.construct_menu(root)
        
        # 画面作成
        self.mainframe = ttk.Frame(root)
        self.mainframe.pack(fill=tk.BOTH)
        self.construct_frame()
        
        # 各種画面を構築
        self.edit_frame = None
        

    
    ## menuファイル生成
    def construct_menu(self, root):
        self.menuBar = Menu()
        self.fileMenu = Menu()
        self.helpMenu = Menu()
        self.editMenu = Menu()

        ## ファイルメニュー
        self.menuBar.add_cascade(menu=self.fileMenu, label="ファイル(F)", underline=5)
        self.fileMenu.add_command(label="テスト読み込み(R)", underline=8, command=self.load)

        ## 編集メニュー
        self.menuBar.add_cascade(menu=self.editMenu, label="編集(E)", underline=3)
        self.editMenu.add_command(label="新規テスト作成(N)", underline=8, command=self.create_new_test)

        ## ヘルプメニュー
        self.menuBar.add_cascade(menu=self.helpMenu, label="ヘルプ(H)", underline=4)
        self.helpMenu.add_command(label="バージョン情報(V)", underline=8, command=self.show_version)
        self.helpMenu.add_command(label="終了(X)", underline=3, command=self.exitMenu)

        root["menu"] = self.menuBar

    ## メイン画面の構築
    def construct_frame(self):
        # ツリービューの設定
        tree = ttk.Treeview(self.mainframe)
        tree["columns"] = list(range(0, 2))
        tree["show"] = "headings"
        tree.column(0, width=10)
        tree.column(0, width=50)
        # 表のヘッダ
        tree.heading(0, text="No.")
        tree.heading(1, text="テスト名")
        # 画面上にセット
        self.tree = tree
        self.tree.grid(row=0)
        # イベントリスナをセット、クリック時に反応する
        self.tree.bind("<<TreeviewSelect>>", self.onSelectTest)
        self.displayTreeView()
        
        frame = tk.Frame(self.mainframe)
        frame.grid(row=1)
        new_create_button = tk.Button(frame, text="新規テスト作成", command=self.create_new_test)
        new_create_button.grid(row=0, column=0)
        
        edit_label = tk.Label(frame, text="No.")
        edit_label.grid(row=0, column=1)
        self.edit_string = StringVar()
        self.edit_entry = tk.Entry(frame, textvariable=self.edit_string, width=5)
        self.edit_entry.grid(row=0, column=2)
        edit_button = tk.Button(frame, text="編集", command=self.edit_test)
        edit_button.grid(row=0, column=3)
        
    
    ## 表のアイテムがクリックされたときのリスナー
    def onSelectTest(self, event):
        # 既に値の入っているものはリセット

        # 選択されている一番上の項目のみ適応
        for id in self.tree.selection():
            item = self.tree.set(id)
            self.edit_entry.insert(tk.END, item["0"])
            break
        
    ## プロセス定義の表示
    def displayTreeView(self):
        # 一度全要素を削除
        for i in self.tree.get_children():
            self.tree.delete(i)

        # 値を入れ直す
        
        record = self.test.get_test_table()
        for rec in record:
            self.tree.insert("", "end", values=rec)
        
    
    ## テストの読み込み
    def load(self):
        pass
    
    ## 新規テスト作成
    def create_new_test(self):
        self.create_dialog = tk.Toplevel(self.mainframe)
        self.create_dialog.title("Create Test")
        self.create_dialog.geometry("400x100")
        self.create_dialog.protocol("WM_DELETE_WINDOW", self.close_new_test_dialog)
        
        # 新規テスト項目を入力
        blank_label = tk.Label(self.create_dialog, text="")
        blank_label.grid(row=0, column=0)
        pipe_no_label = tk.Label(self.create_dialog, text="Pipeline No")
        pipe_no_label.grid(row=1, column=0)
        self.pipe_no_string = tk.StringVar()
        pipe_no_entry = tk.Entry(self.create_dialog, textvariable=self.pipe_no_string, width=3)
        pipe_no_entry.grid(row=1,column=1)
        test_name_label = tk.Label(self.create_dialog, text="テスト名")
        test_name_label.grid(row=1, column=2)
        self.test_name_string = StringVar()
        test_name_entry = tk.Entry(self.create_dialog, textvariable=self.test_name_string, width=30)
        test_name_entry.grid(row=1, column=3)
        dialog_confirm_button = tk.Button(self.create_dialog, text="決定", command=self.close_new_test_dialog)
        dialog_confirm_button.grid(row=1, column=4)
        
        self.create_dialog.grab_set()
        self.create_dialog.focus_set()
        self.create_dialog.transient(self.mainframe)
        self.mainframe.wait_window()
        
        
        
        
            
    ## 新規テストのダイアログを閉じる際の後処理
    def close_new_test_dialog(self):
        pipe_no = 0
        input_result = True
        try:
            pipe_no = int(self.pipe_no_string.get())
        except:
            pipe_no = -1
            messagebox.showwarning("warning", "数字を入力してください")
            input_result = False
        
        if pipe_no == 0:
            messagebox.showwarning("warning", "数字を入力してください")
            input_result = False
        
        if len(self.test_name_string.get()) == 0:
            messagebox.showwarning("warning", "名称を入力してください")
            input_result = False
            
        # テスト追加
        if input_result == True:
            if self.test.create_new_test(pipe_no, self.test_name_string.get()) == False:
                errormessage = "新規テスト生成に失敗しました\nTest No: " +  pipe_no.__str__()
                messagebox.showwarning("warning", errormessage)
        
        self.create_dialog.destroy()
        
        self.displayTreeView()
        
        #Edit画面へ進む
        if input_result == True:
            self.edit_entry.insert(tk.END, pipe_no)
            self.edit_test()

        
    
    def edit_test(self):
        # シナリオNoの数値化とオブジェクト取得
        pipe_no = 0
        input_result = True
        try:
            pipe_no = int(self.edit_entry.get())
        except:
            pipe_no = -1
            messagebox.showwarning("warning", "数字を入力してください")
            input_result = False
        
        
        target = self.test.find(pipe_no)
        if target == None:
            messagebox.showwarning("warning", "テストがありません。新規作成をしてください。")
            input_result = False
            
        
                
        if input_result == True:
            self.edit_dialog = tk.Toplevel(self.mainframe)
            # ほかの画面生成
            self.edit_frame =EditFrame.EditFrame(self.edit_dialog, target)
        
        
    def delete_test(self):
        pass
    
    def executeTest(self):
        pass
    
    def viewTestResult(self):
        pass
    
    ## バージョン表示
    def show_version(self):
        ver = "Tetra"
        ver += " Version (2021/11/20)\n"
        ver += " ©Yuya.Eguchi All rights reserved.\n"
        ver += " Python ver. " + sys.version
        messagebox.showinfo("Tetra", ver)
    

        
    ## 終了
    def exitMenu(self):
        langueage = "EN"
        # if R.langType == R.LangType.JP:
        #     langueage = "JP"

        ## 終了する前にiniファイルに設定書き出し
        # cp = configparser.ConfigParser()
        # cp["main"] = {
        #     "dirpath": self.directoryName,
        #     "language": langueage,
        #     "width": root.winfo_width(),
        #     "height": root.winfo_height()
        # }
        # with open(CONFIGURATION_FILE, "w") as f:
        #     cp.write(f)

        root.destroy()
    

root = tk.Tk()

tetra = Tetra(root)

root.mainloop()