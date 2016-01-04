import win32con,win32api, win32process, win32gui, time, sqlite3, os.path
import urllib.request, urllib.parse
import json, socket, sys

db = sqlite3.connect("sql3.db")
#if sys.argv[1]=='rebuild':
#    db.execute("DROP TABLE IF EXISTS titles;")

db.execute("CREATE TABLE IF NOT EXISTS titles (time,title,imagename);")
cur = db.cursor()

def send_data():
    ret = cur.execute("SELECT COUNT(*) FROM titles").fetchall()
    if ret[0][0] != 0:
        print("Есть что отправить")
        Data = {'Header':[socket.gethostname()],'Lines':[]}
        ret = cur.execute("select time,title,imagename from titles").fetchall()
        for r in ret:
            Data['Lines'].append({'time':r[0],'title':r[1],'imagename':r[2]})
        print(Data)
        #data = urllib.parse.urlencode(values).encode('utf-8')
        #print(data)
        #url='http://127.0.0.1:5000/test'
        #req = urllib.request.Request(url,data)
        #f = urllib.request.urlopen(req)

    else:
        print("Таблица чистая")

#send_data()

windowTitle = ""
counter = 0
while ( True ) :
    counter += 1
    time.sleep(1)
    hwnd = win32gui.GetForegroundWindow()
    newWindowTitle = win32gui.GetWindowText(hwnd)
    if( newWindowTitle != windowTitle ):
        tId,pId = 0,0
        (tId,pId) = win32process.GetWindowThreadProcessId(hwnd)
        exename = "Unknown"
        try:
            pshandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pId)
            exename = win32process.GetModuleFileNameEx(pshandle, 0)
        except:
            print("Что-то пошло не так. {0} {1} {2}".format(tId,pId,newWindowTitle))
        windowTitle = newWindowTitle
        #print(windowTitle,exename)
        cur.execute("INSERT INTO titles VALUES(?,?,?)",(time.strftime("%d.%m.%Y %H:%M:%S"),windowTitle,exename))
        db.commit()
    if counter>10:
        #send_data()
        counter = 0

__author__ = 'Pavel Zaikin (@zztalker)'
