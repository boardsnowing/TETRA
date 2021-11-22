from tkinter import messagebox

class TestCase:
    def __init__(self, no):
        self.no = no
        self.abstruct = ""
        self.prosedure = ""
        self.expect = ""
        
        
        

class Test:
    def __init__(self, no, test_name):
        self.no = no
        self.test_name = test_name
        self.prerequisites = ""
        self.test_case_list = []

    ## テストケースの挿入
    def insert(self, case_no, abstruct, prosedure, expect):
        test_case = TestCase(case_no, abstruct, prosedure, expect)
        self.test_case_list.insert(case_no, test_case)
        self.arrange()

    ## テストケースの追加
    def add(self):
        case_no = len(self.test_case_list) + 1
        test_case = TestCase(case_no)
        self.test_case_list.append(test_case)

    ## テストケースの削除
    def remove(self, case_no):
        self.test_case_list.pop(case_no)
        self.arrange()

    ## 並び替えを行う
    def arrange(self):
        case_no = 1
        for case in self.test_case_list:
            case.no = case_no
            case_no += 1

    
    ## 事前準備を追加する
    def set_prerequisites(self, prerequisites):
        self.prerequisites = prerequisites
        
        
class TestList:
    def __init__(self):
        self.test_list = []
    
    ## 新規テスト作成
    def create_new_test(self, test_no, test_name):
        if self.find(test_no) != None:
            return False
        
        # 見つからなければ新規追加
        test = Test(test_no, test_name)
        self.test_list.append(test)
        print("append comp.", test_no, test_name)
        return True
    
    ## テスト削除
    def remove(self, test_no):
        test = self.find(test_no)
        
        if(test != None):
            self.test_list.remove(test)
        
    def get_test_table(self):
        table = []
        for test in self.test_list:
            print(test.no, test.test_name)
            row = test.no, test.test_name
            table.append(row)
        return table

    ## 検索    
    def find(self, test_no):
        for test in self.test_list:
            if test.no == test_no:
                return test
            
        return None


        