"""    This program is part of spreadsheet.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Do NOT Edit This File If You Do NOT Know What You Doing :)

# this is an extension for editing table data
# table data are stored in an numpy ndarray
# the np array can be access by calling tableWidget.model().array
# to modify the data simply do array[row][column] = new_data
# if modify the shape of array, tableWidget.setModel(tableModel(ndarray, headers= headers))
# good luck !
table = None
from string import ascii_uppercase
def init(tableWidget):
    global table
    table = tableWidget

def getColumnArray(ascii):
    di=dict(zip(ascii_uppercase,[str((ord(c)%32)-1) for c in ascii_uppercase]))
    num = int(''.join([di[i] for i in ascii.split(None) ]))
    column = []
    for i in table.model().array:
        column.append(i[num])
    return column

def getRowArray(num):
    num = int(num)
    return table.model().array[num]

def getCellValue(row,column):
    if column.isnumeric():
        return table.model().array[int(row)][int(column)]
    else:
        di=dict(zip(ascii_uppercase,[str((ord(c)%32)-1) for c in ascii_uppercase]))
        column = int(''.join([di[i] for i in ascii.split(None) ]))
        return table.model().array[int(row)][int(column)]

def main(commandBar, printOutLabel, tableWidget,scripting = False, interact=False,cellfunc=False,screen_width=None,screen_height=None):
    import numpy as np
    

    model = tableWidget.model

    def print(*args,**kw):
        colsep= kw.get('sep',' ')
        flush= kw.get('flush',True)
        linesep = kw.get('end','\n')
        if flush:
            printOutLabel.setText(colsep.join( map(str,args)))
        else:
            printOutLabel.setText(printOutLabel.text()+linesep+colsep.join( map(str,args)))

    def getArray():
        return model().array

    def getHeaders():
        return model().headers

    def getDtype():
        d = model().array.dtype.name
        print(d)
        return d
    
    commands = []


    class column:
        def __init__(self,string):
            di=dict(zip(ascii_uppercase,[str((ord(c)%32)-1) for c in ascii_uppercase]))
            string = str(string)
            if string.isnumeric():
                self.column = int(string)
            else:
                self.column = int(''.join([di[i] for i in string.split(None) ]))

            self.data = tableWidget.model().array[:,self.column]

        def delete(self):
            tableWidget.model().array = np.delete(tableWidget.model().array,self.column,1)
            tableWidget.model().headers.pop(self.column)
            tableWidget.update()

# write your functions here

#    def someFunc():
#        print('done some function')

# End of all functions
    if scripting == False and interact==False:
        try:
            command = commandBar.text()
            command = compile(command, 'user', 'exec')
            exec(command)
        except Exception as e:
            print(e)
        commandBar.clear()
    elif scripting:
        pass
    elif interact:
        import threading
        from PySide2.QtWidgets import QDialog,QLabel,QWidget,QScrollArea,QVBoxLayout,QFormLayout,QLineEdit
        from PySide2.QtGui import Qt
        from PySide2.QtCore import Qt, QEvent
        import PySide2.QtGui as QtGui
        varFuncs = locals()
        def interact():
            
            def execute(line):
                locals().update(varFuncs)
                text = lineEdit['now'].text()
                label = QLabel('>>')
                label.setStyleSheet('color:white;')
                label1 = QLabel(text)
                label1.setStyleSheet('color:white;')
                formlayout.insertRow(formlayout.rowCount()-1,label,label1)
                lineEdit['now'].clear()
                spacing = ''

                def print(text, sep='',end='\n'):
                    label = QLabel(str(text)+end)
                    label.setStyleSheet('color:white;')
                    label.setMaximumHeight(15)
                    formlayout.insertRow(formlayout.rowCount()-1,QLabel(),label)

                if text[-1:] == ':':
                    spacing = '    '
                    mainlabel.setText('..')
                    lineEdit['space'] = True
                    lineEdit['buffer'] = text +'\n'

                elif lineEdit['space']== True:
                    if text.isspace():
                        mainlabel.setText('>>')
                        label.setText('/')
                        lineEdit['space'] = False
                        text = lineEdit['buffer']
                        try:
                            loca = loc
                            text = compile('locals().update(loca)\n' + text,'user','exec')
                            exec(text, locals(), loc)
                        except Exception as e:
                            print(e)
                    else :
                        spacing='    '
                        mainlabel.setText('..')
                        lineEdit['buffer'] += text + '\n'

                else:
                    try:
                        loca = loc
                        text = compile('locals().update(loca)\n' + text, 'user', 'exec')
                        exec(text, locals(), loc)
                    except Exception as e:
                        print(e)
                lineEdit['now'].insert(spacing)

            loc = {}
            scroll = QScrollArea()
            scroll.setStyleSheet('background-color:black;')
            scroll.verticalScrollBar().rangeChanged\
                .connect(lambda :scroll.verticalScrollBar().setValue(scroll.verticalScrollBar().maximum()))

            mainwidget = QWidget()

            scroll.setWidget(mainwidget)
            mainwidget.setStyleSheet('background-color:black;')

            layout = QVBoxLayout()
            layout.addWidget(scroll)
            scroll.setWidgetResizable(True)

            formlayout = QFormLayout(mainwidget)
            formlayout.setMargin(0)
            formlayout.setSpacing(0)
            formlayout.setVerticalSpacing(0)

            from sys import version,platform
            label = QLabel("Python "+str(version)+' on '+platform)
            label.setStyleSheet('background-color:black;color:white;')
            formlayout.addRow(QLabel(),label)

            line = QLineEdit()
            lineEdit = {'now':line,'space':False}
            line.setFrame(False)
            line.returnPressed.connect(lambda :execute(0))
            line.setStyleSheet('background-color:black; color:white;')
            #line.setFont(QtGui.QFont('Lucida Sans Typewriter', 10))

            mainlabel = QLabel('>>')
            mainlabel.setStyleSheet('background-color:black;color:white;')
            formlayout.addRow(mainlabel,line)
            window =QDialog()
            window.setStyleSheet('background-color:black;color:white;')
            window.setMinimumSize(screen_width/2,screen_height/2)
            window.setLayout(formlayout)
            window.setWindowTitle('python console')
            window.setWindowModality(Qt.WindowModal)
            window.setAttribute(Qt.WA_DeleteOnClose)
            window.setStyleSheet('backgroud-color:black;')
            window.exec_()
        a = threading.Thread(target=interact,daemon=True)
        a.start()
    elif cellfunc:
        return


def profile(text,tableWidget):
    from re import findall
    func_num = text.count('(')
    text = text.replace("(","('").replace(")","')")
    params = findall(r"('(.*?)')",text)
    cell = getCellValue
    