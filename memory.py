from functools import partial
from PyQt6.QtWidgets import *
import random

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Memory")
        self.matrix = 4
        self.values = self.get_values(self.matrix)
        self.openValues = list()
        self.finishedIndex = list()
        self.buttons = list()
        for x in range(self.matrix):
            for y in range(self.matrix):
                self.new_button = QPushButton(" ", self)
                self.new_button.setCheckable(True)
                self.value = self.values.pop()
                self.new_button.clicked.connect(partial(self.click,self.new_button,x,y,self.value))
                self.buttons.append([self.new_button,x,y,self.value])
        layout = QGridLayout()
        for button in self.buttons:
            layout.addWidget(button[0],button[1],button[2])
            button[0].setFixedSize(100,100)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def get_values(self, matrix):
        count = int(matrix * matrix / 2)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        stuff = list()
        for x in range(count):
            index = random.randint(0, len(letters) - 1)
            stuff.append(letters[index])
            stuff.append(letters[index])
        random.shuffle(stuff)
        return stuff


    def re_open(self):
        for z in range(len(self.buttons)):
            if z not in self.finishedIndex:
                self.buttons[z][0].setDisabled(False)


    def click(self,button,x,y,value,checked):
        index = self.buttons.index([button,x,y,value])
        if checked:
            self.buttons[index][0].setText(value)
            self.openValues.append([button,x,y,value])
            if len(self.openValues) == 2:
                second_index = self.buttons.index(
                    [self.openValues[0][0], self.openValues[0][1], self.openValues[0][2], self.openValues[0][3]])
                for z in range(len(self.buttons)):
                    if z not in [index,second_index]:
                        self.buttons[z][0].setDisabled(True)
                if self.openValues[0][3] == self.openValues[1][3]:
                    self.buttons[index][0].setDisabled(True)
                    self.buttons[second_index][0].setDisabled(True)
                    self.finishedIndex.append(index)
                    self.finishedIndex.append(second_index)
                    self.openValues.clear()
                    self.re_open()
                    if len(self.finishedIndex) == (self.matrix * self.matrix):
                        msg = QMessageBox(self)
                        msg.setWindowTitle("finished")
                        msg.setText("You won!")
                        msg.setFixedSize(300,300)
                        msg.setStandardButtons(QMessageBox.StandardButton.Close)
                        close = msg.exec()
                        if close == QMessageBox.StandardButton.Close:
                            exit()
        elif not checked:
            self.buttons[index][0].setText(" ")
            self.openValues.remove([button,x,y,value])
            if len(self.openValues) == 0:
                self.re_open()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
