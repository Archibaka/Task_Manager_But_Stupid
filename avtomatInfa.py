import datetime
import json
import os
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog

procs = []
goodchars = "-+=//\\.%^&*()#@!"
src = os.path.dirname(os.path.abspath(__file__))


def getProcs():
    divid = False
    os.system('cmd /c {com}'.format(
        com="wmic process get Name, ProcessId, SessionId, ExecutablePath /FORMAT:LIST > {path}\\servs.txt".format(
            path=src)))
    junk = [{'Name=': '', 'ExecutablePath=': '', 'ProcessId=': '', 'SessionId=': ''}, {}]
    with open("{path}\\servs.txt".format(path=src), 'r') as servs:
        buf = {}
        servs.readline()
        for a in servs.readlines():
            line = "".join([x for x in a if x.isalpha() or x.isdigit() or x in goodchars])
            if line != "" and line != "\n":
                if "=" in line:
                    ky = line[:line.find("=") + 1]
                    if ky not in buf.keys():
                        buf[ky] = ""
                for i in buf:
                    if i in line:
                        buf[i] = line.replace(i, "").replace("\n", "").replace("\r", "")
                        break
                divid = False
            else:
                if divid and all(buf != i for i in junk):
                    procs.append(buf.copy())
                    for i in buf:
                        buf[i] = ""
                    divid = False
                else:
                    divid = True
    return procs


def OutputAsCSV(package):
    if len(package[-1]) != 0:
        with open("{path}\\{name}.csv".format(path=src, name="".join([i for i in package[0] if i.isdigit()])),
                  "w") as idk:
            idk.write("System time was: " + package[0] + ",\n\n")
            for i in package[-1][0].keys():
                idk.write(i.replace("=", ","))
            idk.write("\n")
            for proc in package[-1]:
                for el in proc:
                    idk.write(proc[el] + ",")
                idk.write("\n")


def OutputAsJson(package):
    if len(package[-1]) != 0:
        with open("{path}\\{name}.json".format(path=src, name="".join([i for i in package[0] if i.isdigit()])),
                  "w") as iHateThisFormat:
            iHateThisFormat.write(json.dumps({"time": package[0]}, indent=4) + "\n")
            for i in package[-1]:
                iHateThisFormat.write(json.dumps(i, indent=4) + "\n")


def fileHandle(file):
    if file is not None:
        ext = os.path.splitext(file.name)[-1]
        arr = []
        if ext == ".csv":
            arr.append({"time": file.readline().split(": ")[-1].replace(",", "").replace("\n", "")})
            buf = {}
            kys = []
            file.readline()
            for i in [e for e in file.readline().replace("\n", "").split(",") if e != ""]:
                buf[i + "="] = ""
                kys.append(i + "=")
            for line in file.readlines():
                if line != "\n":
                    sp = line.replace("\n", "").split(",")
                    for j in range(len(kys)):
                        buf[kys[j]] = sp[j]
                    arr.append(buf.copy())
                    for k in kys:
                        buf[k] = ""
        elif ext == ".json":
            buf = ""
            for i in file.readlines():
                buf += i
                if i.replace("\n", "") == "}" and buf[0] == "{":
                    arr.append(json.loads(buf))
                    buf = ""
        else:
            return None
        return arr
    else:
        return file


def compare():
    win = Tk()
    win.iconbitmap("{}\\src\\".format(src) + "3dcat.ico")
    win.geometry("1069x369")
    win.title("In process...")
    currdir = os.getcwd()
    ar1 = fileHandle(filedialog.askopenfile(mode='r', parent=win, initialdir=currdir, title='Select the first '
                                                                                            'file to compare'))
    ar2 = fileHandle(filedialog.askopenfile(mode='r', parent=win, initialdir=currdir, title='Select the second '
                                                                                            'file to compare'))
    if all(i is not None and i != [] for i in [ar1, ar2]):
        diff = Listbox(win)
        sc = Scrollbar(diff)
        diff.pack(side=LEFT, fill=BOTH, expand=YES)
        diff.configure(background='yellow')
        sc.pack(side=RIGHT, fill=BOTH)
        diff.config(yscrollcommand=sc.set)
        sc.config(command=diff.yview)
        lendif = len(ar1) - len(ar2)
        if lendif > 0:
            x = {}
            for k in ar1[-1].keys():
                x[k] = ""
            for i in range(lendif):
                ar2.append(x)
        elif lendif < 0:
            x = {}
            for k in ar1[-1].keys():
                x[k] = ""
            for i in range(abs(lendif)):
                ar1.append(x)
        for i in range(len(ar1)):
            df = []
            for k in ar1[i].keys():
                if ar1[i][k] != ar2[i][k]:
                    df.append(k + ":" + ar1[i][k] + "|" + ar2[i][k])
            if len(df) != 0:
                diff.insert(END, str(df))
        num = diff.size()
        if diff.size() == 0:
            diff.insert(END, "Two files are identical")
        win.title("Differences found: {}".format(num))
        win.mainloop()
    else:
        win.title("Git good, lol ")
        tkinter.Label(master=win, text="use json, csv or a better app to handle ur files")
        win.iconbitmap("{}\\src\\".format(src) + "gg.ico")
        err = Tk()
        err.title("Давай по новой")
        err.geometry("300x100")
        err.iconbitmap("{}\\src\\".format(src) + "gg.ico")
        tkinter.Label(master=err, text='''Ошибка с указанными файлами 
    (принимаются только json и csv)''', ).pack()
        err.mainloop()


def show():
    nw = Tk()
    nw.iconbitmap("{}\\src\\".format(src) + "3dcat.ico")
    package = (datetime.datetime.now().strftime("%d\%m\%Y %H:%M:%S"), getProcs())
    nw.title("Сделано " + package[0])
    nw.geometry("1069x369")
    listbox = Listbox(nw)
    elder = Scrollbar(nw)
    skyrim = Scrollbar(nw, orient='horizontal')
    listbox.pack(side=LEFT, fill=BOTH, expand=YES)
    listbox.configure(background='grey')
    elder.pack(side=LEFT, fill=BOTH)
    skyrim.pack(side=BOTTOM, fill=BOTH)
    for vs in package[-1]:
        listbox.insert(END, str(vs).replace("{",
                                            "").replace("}", "").replace("\"", "").replace("\'", "").replace(r"\\",
                                                                                                             "\\").replace(
            ": ", ""))
    listbox.config(yscrollcommand=elder.set, xscrollcommand=skyrim.set)
    elder.config(command=listbox.yview)
    skyrim.config(command=listbox.xview)
    js = ttk.Button(text="Вывести как json", command=lambda: OutputAsJson(package), master=nw)
    csv = ttk.Button(text="Вывести как csv", command=lambda: OutputAsCSV(package), master=nw)
    comp = ttk.Button(text="сравнить", command=compare, master=nw)
    js.pack(side=RIGHT)
    csv.pack(side=RIGHT)
    comp.pack()
    nw.mainloop()


def BJ():
    os.system('cmd /c "python {path}\\blackjack\\blackjack.py"'.format(path=src))


def Cats():
    linux = Toplevel()
    linux.iconbitmap("{}\\src\\".format(src) + "3dcat.ico")
    linux.geometry("690x690")
    linux.title("Котик")
    cat = ImageTk.PhotoImage(
        Image.open("{}\\src\\".format(src) + "3dcat.jpg"))
    tkinter.Label(linux, image=cat).pack()
    linux.mainloop()


root = Tk()
root.iconbitmap("{}\\src\\".format(src) + "3dcat.ico")
root.geometry("500x300")
pro = ttk.Button(master=root, text="Снимок манагера", command=show)
pro.pack(side="top", expand=1)
black = ttk.Button(master=root, text="Блекджек", command=lambda: BJ())
black.pack(side="top", expand=1)
cats = ttk.Button(master=root, text="Котики", command=Cats)
cats.pack(side="top", expand=1)
root.title("Таск манагер с блекджеком и котиками")
img = ImageTk.PhotoImage(Image.open("{}\\src\\bck.png".format(src)))
tkinter.Label(root, image=img).pack()
root.mainloop()
