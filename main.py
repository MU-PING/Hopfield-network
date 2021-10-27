# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 22:53:56 2020
@author: Mu-Ping
"""
import os
import tkinter as tk
import numpy as np
import random
from tkinter import ttk
from tkinter import messagebox

def create_grid(c, col, row, data=None, color=True): #https://www.coder.work/article/4933449
    zeor_color = '#D0D0D0' if color else "white"
    one_color = '#9D9D9D'  if color else "black"
    file = data.copy() #對傳入的陣列做修改會更改到原本的資料，因此需要copy
    c.delete('all')
    for y in range(row):
        for x in range(col):
            pixel = file.pop(0)
            if(pixel==-1):
                c.create_rectangle((7*x+2, 7*y+2, 7*x+9, 7*y+9), fill = zeor_color) #pixel起始x=2 ；y=2
            elif(pixel==1):
                c.create_rectangle((7*x+2, 7*y+2, 7*x+9, 7*y+9), fill = one_color)
                
def focus(event):
    for i in range(109):
        if(event.widget.itemcget(i ,'fill')=='#9D9D9D'):  #取得舊有屬性
            event.widget.itemconfig(i, fill='black')
        elif(event.widget.itemcget(i ,'fill')=='#D0D0D0'):
            event.widget.itemconfig(i, fill='white')
def unfocus(event):
    for i in range(109):
        if(event.widget.itemcget(i ,'fill')=='black'):  #取得舊有屬性
            event.widget.itemconfig(i, fill='#9D9D9D')
        elif(event.widget.itemcget(i ,'fill')=='white'):
            event.widget.itemconfig(i, fill='#D0D0D0')    
            
def readdata():           
    basic=["Basic_Training.txt", "Basic_Testing.txt"]
    bonus=["Bonus_Training.txt", "Bonus_Testing.txt"]
    data_format_tuple = [(basic, 12, basic_word),(bonus, 10, bonus_word)]
    for data_format in data_format_tuple:
        for file_name in data_format[0]:
            with open(os.getcwd()+'/DataSet/'+ file_name, 'r', encoding='UTF-8') as file:
                eachfile_data=[]
                eachdata=""
                row=0
                for j in file.readlines():
                    if(row==data_format[1]): #取出一個字後參數重設定
                        eachfile_data.append([int(i)-1 for i in eachdata])
                        eachdata=""
                        row=0
                    else:
                        eachdata+=j.replace(" ","0").replace("\n","").replace("1","2")
                        row+=1
            data_format[2].append(eachfile_data)
# basic_word[0] Basic_Training、basic_word[1] Basic_Testing  
# bonus_word[0] Bonus_Training、bonus_word[1] Bonus_Testing
def choose_test(event):
    global test_data, test_row, test_col
    test_data = []
    test_len = 0
    
    for i in range(109):
       if(event.widget.itemcget(i ,'fill')=='black'):  #取得舊有屬性
           test_data.append(1)
       elif(event.widget.itemcget(i ,'fill')=='white'):
           test_data.append(-1)
    
    if(len(test_data)%9==0): #反推canvas大小。也可以透過更改Canvas原始碼將資訊存進物件
        test_row = 12
        test_col = 9
    else:
        test_row = 10
        test_col = 10
        
    create_grid(test_canvas, test_col, test_row, test_data, False)
    
def add_noise(test_data):
    if(test_data==None):        
        messagebox.showwarning("Warning","請先從左方選擇測試資料")
    else:
        for i in np.random.randint(0, test_col*test_row, random.randint(3, 5)): #產生隨機幾個噪點
            test_data[i] = -1 if test_data[i]==1 else 1 #-1 1 互換
            
        create_grid(test_canvas, test_col, test_row, test_data, False)
                
def learning():
    global W, B, binded_canvas
    if(data_combobox.current()==0):
        d = 108
        dataset = basic_word[0] 
        infor = "Basic完成訓練"
        for i in binded_canvas: 
            i.unbind("<Enter>")
            i.unbind("<Leave>")
            i.unbind("<Button-1>")
        binded_canvas = []
        for i in basic_canvas:
            for c in i:
                binded_canvas.append(c)
                c.bind("<Enter>", focus)
                c.bind("<Leave>", unfocus)
                c.bind("<Button-1>", choose_test)

    elif(data_combobox.current()==1):
        d = 100
        dataset = bonus_word[0][(bonus_combobox.current()*3): (3+bonus_combobox.current()*3)]
        infor = "Bonus-"+str(bonus_combobox.current()+1)+"完成訓練"
        for i in binded_canvas: 
            i.unbind("<Enter>")
            i.unbind("<Leave>")
            i.unbind("<Button-1>") 
        binded_canvas = []
        for i in bonus_canvas:
            for c in i[(bonus_combobox.current()*3): (3+bonus_combobox.current()*3)]:
                binded_canvas.append(c)
                c.bind("<Enter>", focus)
                c.bind("<Leave>", unfocus)
                c.bind("<Button-1>", choose_test)
    
    learned_data.set(infor)
    
    W = np.zeros((d, d))
    B = np.zeros((d,1))
    train_data = np.array(dataset)
    for i in train_data:
        W += i.reshape(-1,1).dot(i.reshape(1,-1))
    W -= np.diag(np.diag(W)) #對角線取0
    for i in range(d):
        B+=W[i].reshape(-1,1)
        
def associate():
    iteration_n = np.array(test_data).reshape(-1,1)
    iternum = 0 #避免不收斂
    while(1):
        iteration_n1 = W.dot(iteration_n)-B
        for i in range(len(iteration_n1)):
            if(iteration_n1[i]>0):
                iteration_n1[i]=1
            elif(iteration_n1[i]<0):
                iteration_n1[i]=-1
            else:
                iteration_n1[i]=iteration_n[i]
            
        if((iteration_n1==iteration_n).all()):
            break
        iteration_n = iteration_n1
    create_grid(val_canvas, test_col, test_row, list(iteration_n1), False)
    
def GUI():
    global test_canvas, val_canvas, data_combobox, bonus_combobox
    def state_change(event):
        if(event.widget.current()==0):
            bonus_combobox["state"] = tk.DISABLED
        elif(event.widget.current()==1):
            bonus_combobox["state"] = "readonly"
            
    plt_basic_train = tk.Frame(window)
    plt_basic_train.grid(row=0, column=0)
    plt_basic_test = tk.Frame(window)
    plt_basic_test.grid(row=0, column=1)
    plt_basic = [plt_basic_train, plt_basic_test]
    tk.Label(plt_basic_train, font=("微軟正黑體", 12, "bold"), text="Basic_Training").grid(row=0, column=0, columnspan=3)
    tk.Label(plt_basic_test, font=("微軟正黑體", 12, "bold"), text="Basic_Testing").grid(row=0, column=0, columnspan=3)
    for i in range(2):
        temp = []
        for j in range(3):
            c = tk.Canvas(plt_basic[i], height=85, width=75)
            c.grid(row=1,column=j)
            create_grid(c, 9, 12, basic_word[i][j]) #Basic資料集為9x12
            temp.append(c)
        basic_canvas.append(temp)

#--------------------------------------------------
    plt_bonus_train = tk.Frame(window)
    plt_bonus_train.grid(row=1, column=0, padx=20)
    plt_bonus_test = tk.Frame(window)
    plt_bonus_test.grid(row=1, column=1)
    plt_bonus=[plt_bonus_train, plt_bonus_test]
    tk.Label(plt_bonus_train, font=("微軟正黑體", 12, "bold"), text="Bonus_Training").grid(row=0, column=0, columnspan=3)
    tk.Label(plt_bonus_test, font=("微軟正黑體", 12, "bold"), text="Bonus_Testing").grid(row=0, column=0, columnspan=3)
    for i in range(2):
        rowindex=0
        index = 0
        temp = []
        for j in range(15):
            if(j%3==0): 
                index+=1
                tk.Label(plt_bonus[i], font=("微軟正黑體", 10, "bold"), text="Bonus-"+str(index)).grid(row=rowindex+1, column=0, columnspan=3)
                rowindex+=2
            c = tk.Canvas(plt_bonus[i], height=75, width=75)
            c.grid(row=rowindex, column=j%3)
            create_grid(c, 10, 10, bonus_word[i][j]) #Bonus資料集為10x10
            temp.append(c)
        bonus_canvas.append(temp)

#--------------------------------------------------
    action_bar_1 = tk.Frame(window)
    action_bar_1.grid(row=0, column=2, padx=25)
    tk.Label(action_bar_1, font=("微軟正黑體", 12, "bold"), text="選擇訓練資料集").grid(row=0, column=0, pady=10)
    data_combobox = ttk.Combobox(action_bar_1, value=["Basic_Training","Bonus_Training"], state="readonly", width=15) #readonly為只可讀狀態
    data_combobox.grid(row=1, column=0, sticky=tk.W)
    data_combobox.current(0) #預設Combobox為index0
    data_combobox.bind("<<ComboboxSelected>>", state_change)
    bonus_combobox = ttk.Combobox(action_bar_1, value=["Bonus-1", "Bonus-2", "Bonus-3", "Bonus-4", "Bonus-5"], state="readonly", width=15) #readonly為只可讀狀態
    bonus_combobox.grid(row=2, column=0, sticky=tk.W, pady=5)
    bonus_combobox.current(0) #預設Combobox為index0
    bonus_combobox["state"] = tk.DISABLED
    btn = tk.Button(action_bar_1, text='訓練', command=learning)
    btn.grid(row=3, sticky=tk.E+tk.W, pady=5)
    tk.Label(action_bar_1, font=("微軟正黑體", 10, "bold"), textvariable=learned_data).grid(row=4, column=0)
    
    action_bar_2 = tk.Frame(window)
    action_bar_2.grid(row=1, column=2, padx=25, pady=25, sticky=tk.N)
    tk.Label(action_bar_2, font=("微軟正黑體", 12, "bold"), text="選擇測試資料").grid(row=0, column=0)
    test_canvas = tk.Canvas(action_bar_2, height=85, width=75)
    test_canvas.grid(row=1, column=0)
    btn1 = tk.Button(action_bar_2, text='加入雜訊', command=lambda: add_noise(test_data))
    btn1.grid(row=2, sticky=tk.E+tk.W, pady=5)
    btn2 = tk.Button(action_bar_2, text='驗證', command=associate)
    btn2.grid(row=3, sticky=tk.E+tk.W, pady=5)
    tk.Label(action_bar_2, font=("微軟正黑體", 12, "bold"), text="驗證結果").grid(row=4, column=0)
    val_canvas = tk.Canvas(action_bar_2, height=85, width=75)
    val_canvas.grid(row=5, column=0)

basic_word = []
bonus_word = []
basic_canvas = []
bonus_canvas = []
binded_canvas = []
data_combobox = None
bonus_combobox = None
test_canvas = None
val_canvas = None
test_data = None
test_row = 0
test_col = 0
W = None
B = None

window = tk.Tk()
window.geometry("720x710")
window.resizable(False, False)
window.title("Hopfield")
learned_data = tk.StringVar()#學習率
readdata()
GUI()

window.mainloop()
