import json
import urllib.request
import sys, threading
import re, datetime, time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QStatusBar, QDialog,QFormLayout,QCheckBox,QHBoxLayout,QCalendarWidget, QTabWidget,QMenu, QApplication, QMainWindow, QWidget, QTableWidget,QPushButton, QTableWidgetItem, QVBoxLayout,QHeaderView, QGridLayout, QLabel,QAbstractItemView, QAction, QComboBox,QLineEdit

class PropertiesWindow(QDialog):
    def __init__(self):
        super(PropertiesWindow, self).__init__()

        self.title = "Search properties"
        self.top   = 100
        self.left  = 100
        self.width = 600
        self.height= 695
        self.setFixedSize(self.width,self.height)

        self.InitWidnow()

    def InitWidnow(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,self.width,self.height)
        self.CreateMenu()


        vbox = QVBoxLayout()
        fbox = QFormLayout()

        vbox.addWidget(self.textBoxMaxPrice)
        vbox.addWidget(self.textBoxMinPrice)

        fbox.addRow(self.boxKeywords, self.textBoxKeywords)
        fbox.addRow(self.boxLocality, self.textBoxLocality)
        fbox.addRow(self.boxPrice, vbox)
        fbox.addRow(self.boxMethod, self.comboMethod)
        fbox.addRow(self.boxLowDate, self.calLowDate)
        fbox.addRow(self.boxHighDate, self.calHighDate)
        fbox.addRow(self.saveButton, self.exitButton)



        self.setLayout(fbox)
        self.boxKeywords.setWhatsThis("Choose, if you want to search by keyword(s).")
        self.textBoxKeywords.setWhatsThis("All keywords must be separated by comas. For Example: Tadana, bikes")
        self.boxPrice.setWhatsThis("Choose, if you want to search by price.")
        self.textBoxMaxPrice.setWhatsThis("Maximum price that will be allowed while searching.")
        self.textBoxMinPrice.setWhatsThis("Minimum price that will be allowed while searching.")
        self.boxMethod.setWhatsThis("Chooses, if you want to search by method.")
        self.comboMethod.setWhatsThis("Allowed methods of trading")
        self.boxLowDate.setWhatsThis("Choose, if you want to search by start date.")
        self.calLowDate.setWhatsThis("Earlier date that will be allowed while searching. Check date in callendar once.")
        self.boxHighDate.setWhatsThis("Choose, if you want to search by longest date.")
        self.calHighDate.setWhatsThis("Olders date that will be allowed while searching. Check date in callendar once.")
        self.boxLocality.setWhatsThis("Choose, if you want to search by locality(ies).")
        self.textBoxLocality.setWhatsThis("All localities must be separated by comas. For Example: Odessa, Kiev")
        self.saveButton.setWhatsThis("Save button. Click after making changes to save your search properties to config file.")
        self.exitButton.setWhatsThis("Exit button. Click if you want to exit properties menu. Do not forget to save ;)")
        self.show()

    def CreateMenu(self):
        #Keywords
        self.boxKeywords = QCheckBox('Search by keywords',self)
        self.textBoxKeywords = QLineEdit(self)

        #Price
        self.boxPrice = QCheckBox('Search by price',self)
        self.textBoxMinPrice = QLineEdit(self)
        self.textBoxMaxPrice = QLineEdit(self)
        self.textBoxMaxPrice.setText("Max. price...")
        self.textBoxMinPrice.setText("Min. price...")

        #Method
        self.boxMethod = QCheckBox('Search by method',self)
        self.comboMethod = QComboBox(self)
        self.comboMethod.addItem("Tender")
        self.comboMethod.addItem("Auction")
        self.comboMethod.addItem("Enquiries")

        #Date
        self.boxLowDate = QCheckBox('Search by low date',self)
        self.calLowDate = QCalendarWidget(self)
        self.calLowDate.setGridVisible(True)
        self.calLowDate.clicked[QtCore.QDate].connect(self.SetLowDate)
        self.boxHighDate = QCheckBox('Search by high date',self)
        self.calHighDate = QCalendarWidget(self)
        self.calHighDate.setGridVisible(True)
        self.calHighDate.clicked[QtCore.QDate].connect(self.setHighDate)

        #Locality
        self.boxLocality = QCheckBox('Search by localities',self)
        self.textBoxLocality = QLineEdit(self)

        #SaveButton
        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.SaveAllData)

        #CloseButton
        self.exitButton = QPushButton(self)
        self.exitButton.setText("Close")
        self.exitButton.clicked.connect(self.close)

        #options
        self.textBoxKeywords.setEnabled(0)
        self.textBoxMaxPrice.setEnabled(0)
        self.textBoxMinPrice.setEnabled(0)
        self.comboMethod.setEnabled(0)
        self.calHighDate.setEnabled(0)
        self.calLowDate.setEnabled(0)
        self.textBoxLocality.setEnabled(0)
        self.saveButton.setEnabled(0)

        #custom
        self.boxHighDate_state = False
        self.boxLowDate_state = False
        self.boxLocality_state = False
        self.boxMethod_state = False
        self.boxPrice_state = False
        self.boxKeywords_state = False

        #check state

        if config['searchByKeyWords'] == "yes":
            self.boxKeywords.setChecked(True)
            self.string2 = self.setString(config['keyWords'])
            self.textBoxKeywords.setText(str(self.string2))
            self.textBoxKeywords.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxKeywords_state = True
        if config['searchByPrice'] == "yes":
            self.boxPrice.setChecked(True)
            self.textBoxMaxPrice.setText(config['priceMax'])
            self.textBoxMinPrice.setText(config['priceMin'])
            self.textBoxMaxPrice.setEnabled(1)
            self.textBoxMinPrice.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxPrice_state = True
        if config['searchBylocality'] == "yes":
            self.boxLocality.setChecked(True)
            self.string1 = self.setString(config['searchBylocality'])
            self.textBoxLocality.setText(str(self.string1))
            self.textBoxLocality.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxLocality_state = True
        if config['searchByStartDate'] == "yes":
            self.boxLowDate.setChecked(True)
            self.calLowDate.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxLowDate_state = True
        if config['searchByEndDate'] == "yes":
            self.boxHighDate.setChecked(True)
            self.calHighDate.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxHighDate_state = True
        if config['searchByMethod'] == "yes":
            self.boxMethod.setChecked(True)
            self.comboMethod.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxMethod_state = True

        #events
        self.boxHighDate.stateChanged.connect(self.boxHighDateState)
        self.boxKeywords.stateChanged.connect(self.boxKeywordsState)
        self.boxLocality.stateChanged.connect(self.boxLocalityState)
        self.boxMethod.stateChanged.connect(self.boxMethodState)
        self.boxPrice.stateChanged.connect(self.boxPriceState)
        self.boxLowDate.stateChanged.connect(self.boxLowDateState)



    def setString(self, list):
        string_s = str(list[0])
        i=1
        while i < len(list):
            string_s = string_s +  ","+ str(list[i])
            i=i+1
        return string_s

    def boxHighDateState(self):
        if self.boxHighDate_state == False:
            self.calHighDate.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxHighDate_state = True
        else:
            self.boxHighDate_state = False
            self.calHighDate.setEnabled(0)
            if self.boxLocality_state or self.boxLowDate_state or self.boxKeywords_state or self.boxMethod_state or self.boxPrice_state or self.CheckIfYes():
                pass
            else:
                self.saveButton.setEnabled(0)

    def CheckIfYes(self):

        for k in config:
            if config[k] == "yes":
                return True
        return False

    def boxKeywordsState(self):
        if self.boxKeywords_state == False:
            self.textBoxKeywords.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxKeywords_state = True
        else:
            self.boxKeywords_state = False
            self.textBoxKeywords.setEnabled(0)
            if self.boxLocality_state or self.boxHighDate_state or self.boxLowDate_state or self.boxMethod_state or self.boxPrice_state or self.CheckIfYes():
                pass
            else:
                self.saveButton.setEnabled(0)

    def boxLocalityState(self):
        if self.boxLocality_state == False:
            self.textBoxLocality.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxLocality_state = True
        else:
            self.boxLocality_state = False
            self.textBoxLocality.setEnabled(0)
            if self.boxHighDate_state or self.boxLowDate_state or self.boxKeywords_state or self.boxMethod_state or self.boxPrice_state or self.CheckIfYes():
                pass
            else:
                self.saveButton.setEnabled(0)

    def boxMethodState(self):
        if self.boxMethod_state == False:
            self.comboMethod.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxMethod_state = True
        else:
            self.boxMethod_state = False
            self.comboMethod.setEnabled(0)
            if self.boxLocality_state or self.boxHighDate_state or self.boxLowDate_state or self.boxKeywords_state or self.boxPrice_state or self.CheckIfYes():
                pass
            else:
                self.saveButton.setEnabled(0)

    def boxPriceState(self):
        if self.boxPrice_state == False:
            self.textBoxMinPrice.setEnabled(1)
            self.textBoxMaxPrice.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxPrice_state = True
        else:
            self.boxPrice_state = False
            self.textBoxMinPrice.setEnabled(0)
            self.textBoxMaxPrice.setEnabled(0)
            if self.boxLocality_state or self.boxHighDate_state or self.boxLowDate_state or self.boxKeywords_state or self.boxMethod_state or self.CheckIfYes():
                pass
            else:
                self.saveButton.setEnabled(0)

    def boxLowDateState(self):
        if self.boxLowDate_state == False:
            self.calLowDate.setEnabled(1)
            self.saveButton.setEnabled(1)
            self.boxLowDate_state = True
        else:
            self.boxLowDate_state = False
            self.calLowDate.setEnabled(0)
            if self.boxLocality_state or self.boxHighDate_state or self.boxKeywords_state or self.boxMethod_state or self.boxPrice_state or self.CheckIfYes():
                pass
            else:
                self.saveButton.setEnabled(0)


    def SetLowDate(self, date):
        month = str(date.month())
        day = str(date.day())
        if len(month) == 1:
            month = "0" + month
        elif len(dat) == 1:
            day = "0"+day
        self.lowdate = day + "/" + month + "/" + str(date.year())

    def setHighDate(self, date):
        month = str(date.month())
        day = str(date.day())
        if len(month) == 1:
            month = "0" + month
        elif len(dat) == 1:
            day = "0"+day
        self.highdate = day + "/" + month + "/" + str(date.year())

    def SaveAllData(self):
        global config
        self.locality_status = "no"
        self.keywords_status = "no"
        self.price_status = "no"
        self.lowdate_status = "no"
        self.highdate_status = "no"
        self.method_status = "no"


        self.keywords = [0]
        self.localities = [0]
        self.minPrice = "0"
        self.maxPrice = "0"


        if self.boxLocality_state:
            del self.locality_status
            del self.localities
            self.localities_string = str(self.textBoxLocality.text())
            self.localities = self.localities_string.split(",")
            self.locality_status = "yes"

        if self.boxKeywords_state:
            del self.keywords
            del self.keywords_status
            self.keywords_string = str(self.textBoxKeywords.text())
            self.keywords = self.keywords_string.split(",")
            i = 0
            while i < len(self.keywords):
                self.keywords[i].strip()
                i=i+1
            self.keywords_status = "yes"

        if self.boxPrice_state:
            del self.price_status
            self.price_status = "yes"
            self.priceMinprice = re.search("\\d*", self.textBoxMinPrice.text())
            self.priceMaxprice = re.search("\\d*", self.textBoxMaxPrice.text())
            if not self.priceMinprice.group(0):
                pass
            else:
                del self.minPrice
                self.minPrice = str(self.priceMinprice.group(0))
            if not self.priceMaxprice.group(0):
                pass
            else:
                del self.maxPrice
                self.maxPrice = str(self.priceMaxprice.group(0))

        if self.boxLowDate_state:
            del self.lowdate_status
            self.lowdate_status = "yes"
        else:
            self.lowdate = "00/00/0000"

        if self.boxHighDate_state:
            del self.highdate_status
            self.highdate_status = "yes"
        else:
            self.highdate = "00/00/0000"

        if self.boxMethod_state:
            del self.method_status
            self.method_status = "yes"


        data = {"searchByKeyWords": str(self.keywords_status),
                "keyWords": self.keywords,

                "searchByPrice":str(self.price_status),
                "priceMin":str(self.minPrice),
                "priceMax":str(self.maxPrice),

                "searchBylocality":str(self.locality_status),
                "locality":self.localities,

                "searchByStartDate":str(self.lowdate_status),
                "startDate":str(self.lowdate),

                "searchByEndDate":str(self.highdate_status),
                "endDate":str(self.highdate),

                "searchByMethod":str(self.method_status),
                "method":str(self.comboMethod.currentText()).lower()}
        with open("config.json", 'w') as response:
            json.dump(data,response,indent = 4)
        with open("config.json",'r') as response:
            config = json.load(response)
        self.close()




class DataCiclusThread(QtCore.QThread):
    ciclusDone = QtCore.pyqtSignal(int)
    def __init__(self,parent=None):
        super(DataCiclusThread, self).__init__()

    def run(self):
        global tg_get_data
        print("//////////////////////PAUSED///////////////////////")
        tg_get_data = 1

class GetDataThread(QtCore.QThread):
    threadDone = QtCore.pyqtSignal(int)
    def __init__(self, parent = None):
        global tg_get_data, thread
        super(GetDataThread, self).__init__()
        self.buffer = thread

    def run(self):
        print("threading in process")

        time.sleep(1)
        self.get_last_url()
        while self.buffer != 0:
            self.get_next_page_url()
            self.buffer = self.buffer-1

        while True:

            self.get_data()
            self.get_next_page_url()
        self.threadDone.emit(0)
    def get_next_page_url(self):
        try:
            with urllib.request.urlopen(self.tender_url) as response:
                buffer = json.load(response)
            del self.tender_url
            self.tender_url = buffer['next_page']['uri'] + tender_param + "&limit=1000"
        except urllib.request.URLError as err:
            self.get_next_page_url()
    def get_last_url(self):

        try:
            with urllib.request.urlopen(tender_last_url) as response:
                buffer = json.load(response)
            self.tender_url = buffer['prev_page']['uri'] + tender_param + "&limit=1000"
        except urllib.request.URLError as err:
            self.get_last_url()


    def get_data(self):

        global list_id,idx_check,idx_match,tg_get_data,buffer_get_data,idx_check,list_status, list_url,list_telephone,list_currency,list_description,list_price,list_procurementMethod,list_title,list_email,list_postCode,list_locality,list_startDate,list_endDate,list_awardCriteria
        #Get tender list
        try:
            with urllib.request.urlopen(self.tender_url) as response:
                data = json.load(response)
        except urllib.request.URLError as err:
            pass


        #Format the data
        list_l = []
        idx_s = 0
        while idx_s < len(data['data']):
            list_l.append(data['data'][idx_s]['id'])
            idx_s=idx_s+1

        #Get data

        id_get = 0

        while id_get < len(list_l):
            if buffer_get_data != tg_get_data:
                while buffer_get_data != tg_get_data:
                    pass
            idx_check = idx_check+1
            tender_data_url = tender_basic_url + '/' + list_l[id_get] + tender_url_param
            try:
                with urllib.request.urlopen(tender_data_url) as response:
                    _data = json.load(response)
                if 'tenderPeriod' in _data['data']:
                    if 'value' in _data['data']:
                        if 'locality' in _data['data']['procuringEntity']['address']:
                            if 'telephone' in _data['data']['procuringEntity']['contactPoint']:
                                if Window.CheckIfExist(_data) == 0:
                                    idx_match = idx_match+1
                                    list_telephone.append(_data['data']['procuringEntity']['contactPoint']['telephone'])
                                    list_price.append(_data['data']['value']['amount'])
                                    list_procurementMethod.append(_data['data']['procurementMethod'])
                                    list_status.append(_data['data']['status'])
                                    list_title.append(_data['data']['title'])
                                    list_email.append(_data['data']['procuringEntity']['contactPoint']['email'])
                                    list_postCode.append(_data['data']['procuringEntity']['address']['postalCode'])
                                    list_locality.append(_data['data']['procuringEntity']['address']['locality'])
                                    list_startDate.append(_data['data']['tenderPeriod']['startDate'])
                                    list_endDate.append(_data['data']['tenderPeriod']['endDate'])
                                    list_awardCriteria.append(_data['data']['awardCriteria'])
                                    list_description.append(_data['data']['items'][0]['description'])
                                    list_currency.append(_data['data']['value']['currency'])
                                    list_id.append(list_l[id_get])
                                    Window.PutRow()
                                else:
                                    pass
                            else:
                                pass
                    else:

                        pass

                else:

                    pass
                id_get = id_get+1
                statusThread.start()
            except urllib.request.URLError as err:
                pass
        del list_l
        del id_get


class CheckSaveRowChanges(QtCore.QThread):
    mainThread = QtCore.pyqtSignal(int)
    def __init__(self, parent = None):
        super(CheckSaveRowChanges, self).__init__()

    def run(self):
        print("EMIT")
        self.addRow_saved()

    def addRow_saved(self):
        with open('best.json','r') as response:
            data = json.load(response)
        idx = len(data.keys())-1
        currentRowCount = tableWidget_saved.rowCount()
        tableWidget_saved.insertRow(currentRowCount)
        tableWidget_saved.setItem(currentRowCount,0, QTableWidgetItem(str(data[str(idx)]['procurementMethod'])))
        tableWidget_saved.setItem(currentRowCount,1, QTableWidgetItem(str(data[str(idx)]['status'])))
        tableWidget_saved.setItem(currentRowCount,2, QTableWidgetItem(str(data[str(idx)]['price'])))
        tableWidget_saved.setItem(currentRowCount,3, QTableWidgetItem(str(data[str(idx)]['title'])))
        tableWidget_saved.setItem(currentRowCount,4, QTableWidgetItem(str(data[str(idx)]['email'])))
        tableWidget_saved.setItem(currentRowCount,5, QTableWidgetItem(str(data[str(idx)]['postalCode'])))
        tableWidget_saved.setItem(currentRowCount,6, QTableWidgetItem(str(data[str(idx)]['locality'])))
        tableWidget_saved.setItem(currentRowCount,7, QTableWidgetItem(str(Window.set_Date(data[str(idx)]['startDate']))))
        tableWidget_saved.setItem(currentRowCount,8, QTableWidgetItem(str(Window.set_Date(data[str(idx)]['endDate']))))
        tableWidget_saved.setItem(currentRowCount,9, QTableWidgetItem(str(data[str(idx)]['description'])))


class SaveTabWidget(QTableWidget):
    def __init__(self, parent=None):
        super(SaveTabWidget, self).__init__(parent)

    def contextMenuEvent(self,event):
        context_menu_all_tab = QMenu(self)
        saveDataByRow = context_menu_all_tab.addAction("Delete")
        action = context_menu_all_tab.exec_(self.mapToGlobal(event.pos()))
        if action == saveDataByRow:
            self.DeleteObject(event)

    def DeleteObject(self,position):
        r= self.selectedIndexes()[0]
        cell = r.row()
        self.removeRow(r.row())

        with open("best.json", 'r') as response:
            buffer = json.load(response)

        buffer["delete"] = buffer.pop(str(cell))

        for i in list(buffer.keys()):
            if i == "0":
                buffer[i] = buffer.pop(i)
            elif i == "delete":
                pass
            else:
                buffer[str(int(i)-1)] = buffer.pop(i)



        del buffer["delete"]
        with open("best.json", 'w') as response:
            json.dump(buffer, response, indent=4)




class AllTabWidget(QTableWidget):
    def __init__(self, parent=None):
        super(AllTabWidget,self).__init__(parent)
        self.workerThread = CheckSaveRowChanges()

    def contextMenuEvent(self,event):
        context_menu_all_tab = QMenu(self)
        saveDataByRow = context_menu_all_tab.addAction("Save")
        deleteRow = context_menu_all_tab.addAction("Delete Row")
        deleteTable = context_menu_all_tab.addAction("Delete All")

        action = context_menu_all_tab.exec_(self.mapToGlobal(event.pos()))
        if action == saveDataByRow:
            self.SaveObject()
        elif action == deleteRow:
            self.DeleteRow()
        elif action == deleteTable:
            self.DeleteTable()
    def DeleteTable(self):
        global date_today,best,config,list_id,idx_match,idx_check,list_status, list_url,list_telephone,list_currency,list_description,list_price,list_procurementMethod,list_title,list_email,list_postCode,list_locality,list_startDate,list_endDate,list_awardCriteria
        i = 0
        while i < tableWidget.rowCount():
            tableWidget.removeRow(i)
            i=i+1
        del list_price
        del list_currency
        del list_description
        del list_email
        del list_endDate
        del list_startDate
        del list_locality
        del list_title
        del list_postCode
        del list_id
        del list_status
        del list_procurementMethod
        del list_telephone
        del list_awardCriteria
        Window.VariablesIni()
    def DeleteRow(self):
        r= tableWidget.selectedIndexes()[0]
        sel = r.row()
        tableWidget.removeRow(r.row())
        del list_price[sel]
        del list_currency[sel]
        del list_description[sel]
        del list_email[sel]
        del list_endDate[sel]
        del list_startDate[sel]
        del list_locality[sel]
        del list_title[sel]
        del list_postCode[sel]
        del list_id[sel]
        del list_status[sel]
        del list_procurementMethod[sel]
        del list_telephone[sel]
        del list_awardCriteria[sel]
    def SaveObject(self):

        r= tableWidget.selectedIndexes()[0]
        sel = r.row()
        self.GetDataInRow(r.row())
        tableWidget.removeRow(r.row())
        buffer = {}
        with open("best.json", 'r') as response:
            buffer = json.load(response)

        if buffer:
            if len(buffer.keys()) != 1:

                buffer[int(list(buffer.keys())[-1]) + 1] = {'price':str(self.row_price),
                                'awardCriteria':str(self.row_awardCriteria),
                                'telephone':str(self.row_telephone),
                                'status':str(self.row_status),
                                 'procurementMethod':str(self.row_procurementMethod),
                                 'currency':str(self.row_currency),
                                 'description':str(self.row_description),
                                 'email':str(self.row_email),
                                 'endDate':str(self.row_endDate),
                                 'startDate':str(self.row_startDate),
                                 'locality':str(self.row_locality),
                                 'title':str(self.row_title),
                                 'postalCode':str(self.row_postalCode),
                                 'id':str(self.row_id)}
            else:
                buffer[1] = {'price':str(self.row_price),
                                'awardCriteria':str(self.row_awardCriteria),
                                'telephone':str(self.row_telephone),
                                'status':str(self.row_status),
                                'procurementMethod':str(self.row_procurementMethod),
                                 'currency':str(self.row_currency),
                                 'description':str(self.row_description),
                                 'email':str(self.row_email),
                                 'endDate':str(self.row_endDate),
                                 'startDate':str(self.row_startDate),
                                 'locality':str(self.row_locality),
                                 'title':str(self.row_title),
                                 'postalCode':str(self.row_postalCode),
                                 'id':str(self.row_id)}
        elif not buffer:
            buffer[0] = {'price':str(self.row_price),
                            'awardCriteria':str(self.row_awardCriteria),
                            'telephone':str(self.row_telephone),
                            'status':str(self.row_status),
                            'procurementMethod':str(self.row_procurementMethod),
                             'currency':str(self.row_currency),
                             'description':str(self.row_description),
                             'email':str(self.row_email),
                             'endDate':str(self.row_endDate),
                             'startDate':str(self.row_startDate),
                             'locality':str(self.row_locality),
                             'title':str(self.row_title),
                             'postalCode':str(self.row_postalCode),
                             'id':str(self.row_id)}
        with open("best.json", 'w') as response:
            json.dump(buffer, response, indent = 4)
        self.workerThread.start()
        del list_price[sel]
        del list_currency[sel]
        del list_description[sel]
        del list_email[sel]
        del list_endDate[sel]
        del list_startDate[sel]
        del list_locality[sel]
        del list_title[sel]
        del list_postCode[sel]
        del list_id[sel]
        del list_status[sel]
        del list_procurementMethod[sel]
        del list_telephone[sel]
        del list_awardCriteria[sel]

    def GetDataInRow(self,row):
        self.row_price = list_price[row]
        self.row_currency = list_currency[row]
        self.row_description = list_description[row]
        self.row_email = list_email[row]
        self.row_endDate = list_endDate[row]
        self.row_startDate = list_startDate[row]
        self.row_locality = list_locality[row]
        self.row_title = list_title[row]
        self.row_postalCode = list_postCode[row]
        self.row_id = list_id[row]
        self.row_procurementMethod = list_procurementMethod[row]
        self.row_status = list_status[row]
        self.row_telephone = list_telephone[row]
        self.row_awardCriteria = list_awardCriteria[row]

class SetStatusTipThread(QtCore.QThread):
    statusTip = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(SetStatusTipThread, self).__init__()
    def run(self):
        self.statusTip.emit(0)


class ClickDialog(QDialog):
    def __init__(self, data, parent=None):
        super(ClickDialog, self).__init__(parent)
        self.data = data
        self.title = "Info"
        self.width = 900
        self.height = 540
        self.top = 100
        self.left = 100

        self.tableWidget = QTableWidget(self)
        self.InitWidnow()

    def InitWidnow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,self.width,self.height)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)

        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(13)
        self.header = self.tableWidget.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(['Info'])
        self.tableWidget.setVerticalHeaderLabels(['Status','Started','End','Method','Price','Title','Description','Email','Telephone','Locality','PostalCode','AwardCriteria','ID'])
        self.tableWidget.setItem(0,0, QTableWidgetItem(str(self.data['procurementMethod'])))
        self.tableWidget.setItem(1,0, QTableWidgetItem(str(Window.set_Date(self.data['startDate']))))
        self.tableWidget.setItem(2,0, QTableWidgetItem(str(Window.set_Date(self.data['endDate']))))
        self.tableWidget.setItem(3,0, QTableWidgetItem(str(self.data['status'])))
        self.tableWidget.setItem(4,0, QTableWidgetItem(str(self.data['price'])+" "+self.data['currency']))
        self.tableWidget.setItem(5,0, QTableWidgetItem(str(self.data['title'])))
        self.tableWidget.setItem(6,0, QTableWidgetItem(str(self.data['description'])))
        self.tableWidget.setItem(7,0, QTableWidgetItem(str(self.data['email'])))
        self.tableWidget.setItem(8,0, QTableWidgetItem(str(self.data['telephone'])))
        self.tableWidget.setItem(9,0, QTableWidgetItem(str(self.data['locality'])))
        self.tableWidget.setItem(10,0, QTableWidgetItem(str(self.data['postalCode'])))
        self.tableWidget.setItem(11,0, QTableWidgetItem(str(self.data['awardCriteria'])))
        self.tableWidget.setItem(12,0, QTableWidgetItem(str(self.data['id'])))

        self.setLayout(self.layout)
        self.show()



class Window(QMainWindow):
    def __init__(self):
        global tg_get_data, buffer_get_data
        tg_get_data = 2
        buffer_get_data = 0
        super(Window, self).__init__()
        Window.VariablesIni()
        self.title = "SomeAPPforProzorro"
        self.top   = 100
        self.left  = 100
        self.width = 1280
        self.height= 720
        self.InitWidnow()
        self.workerThread =GetDataThread()
        self.workerThread.threadDone.connect(self.threadDone)
        self.workerThread.start()



    def threadDone(self):
        print("thread Execution completed")

    def InitWidnow(self):
        global wid, statusThread
        main = QWidget(self)
        wid = QWidget()

        statusThread = SetStatusTipThread()
        statusThread.statusTip.connect(self.SetStatusTip)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.tabs = QTabWidget()
        self.tab = QWidget()
        self.tabs.resize(1920,1080)
        self.tabs.addTab(wid,"All")
        self.tabs.addTab(self.tab,"Saved")


        self.setCentralWidget(main)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,self.width,self.height)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.MenuItem()
        self.CreateTable()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        main.setLayout(layout)
        wid.vBoxLayout = QVBoxLayout()
        self.tab.vBoxLayout_saved = QVBoxLayout()
        wid.vBoxLayout.addWidget(tableWidget)
        self.tab.vBoxLayout_saved.addWidget(tableWidget_saved)
        self.tab.setLayout(self.tab.vBoxLayout_saved)
        wid.setLayout(wid.vBoxLayout)
        self.show()


    def MenuItem(self):
        #Menu items
        updateData = QAction("&Start", self)
        updateData.setShortcut("Ctrl+R")
        updateData.setStatusTip('Start searching')
        updateData.triggered.connect(self.UpdateData)

        pauseData = QAction("&Stop", self)
        pauseData.setShortcut("Ctrl+P")
        pauseData.setStatusTip("Stop searching")
        pauseData.triggered.connect(self.PauseSearching)

        propertiesData = QAction("&Properties",self)
        propertiesData.setShortcut("Ctrl+W")
        propertiesData.setStatusTip("Searching properties")
        propertiesData.triggered.connect(self.openProperties)

        addThread = QAction("&Enable multithreading",self)
        addThread.setShortcut("Ctrl+Z")
        addThread.triggered.connect(self.AddThread)

        exitFromMain = QAction("&Quit",self)
        exitFromMain.setShortcut("Ctrl+Q")
        exitFromMain.setStatusTip("Exit from application")
        exitFromMain.triggered.connect(self.ExitFromMain)

        #Menu Initialization
        mainMenu = self.menuBar()
        resetData = mainMenu.addMenu("&File")
        resetData.addAction(updateData)
        resetData.addAction(pauseData)
        resetData.addAction(propertiesData)
        resetData.addAction(addThread)
        resetData.addAction(exitFromMain)


    def AddThread(self):
        global thread
        thread = 1
        self.w1 = GetDataThread()
        self.w1.start()
        thread = 2
        self.w2 = GetDataThread()
        self.w2.start()
        thread = 3
        self.w3 = GetDataThread()
        self.w3.start()
        thread = 4
        self.w4 = GetDataThread()
        self.w4.start()
        thread = 5
        self.w5 = GetDataThread()
        self.w5.start()
        thread = 6
        self.w6 = GetDataThread()
        self.w6.start()
        thread = 7
        self.w7 = GetDataThread()
        self.w7.start()
        thread = 8
        self.w8 = GetDataThread()
        self.w8.start()
        thread = 9
        self.w9 = GetDataThread()
        self.w9.start()
        thread = 10
        self.w10 = GetDataThread()
        self.w10.start()
        thread = 11
        self.w11 = GetDataThread()
        self.w11.start()
        thread = 12
        self.w12 = GetDataThread()
        self.w12.start()
        thread = 13
        self.w13 = GetDataThread()
        self.w13.start()
        thread = 14
        self.w14 = GetDataThread()
        self.w14.start()
        thread = 15
        self.w15 = GetDataThread()
        self.w15.start()
        thread = 16
        self.w16 = GetDataThread()
        self.w16.start()
        thread = 17
        self.w17 = GetDataThread()
        self.w17.start()
        thread = 18
        self.w18 = GetDataThread()
        self.w18.start()
        thread = 19
        self.w19 = GetDataThread()
        self.w19.start()
        thread = 20
        self.w20 = GetDataThread()
        self.w20.start()
        thread = 21




    def PauseSearching(self):
        self.workerThread_searching = DataCiclusThread()
        self.workerThread_searching.start()
        self.setStatusTip("Searching paused")

    def ExitFromMain(self):
        self.close()

    def openProperties(self):
        self.propertiesWindow = PropertiesWindow()
        self.propertiesWindow.show()


    def VariablesIni():
        global tender_param,tender_basic_url,tender_last_url,thread,date_today,best,config,list_id,idx_match,idx_check,list_status, list_url,list_telephone,list_currency,list_description,list_price,list_procurementMethod,list_title,list_email,list_postCode,list_locality,list_startDate,list_endDate,list_awardCriteria
        list_price = []
        list_currency = []
        list_procurementMethod = []
        list_title = []
        list_telephone = []
        list_url = []
        list_description = []
        list_email = []
        list_postCode = []
        list_locality = []
        list_startDate = []
        list_endDate = []
        list_awardCriteria = []
        list_status = []
        list_id = []
        date_buff = datetime.datetime.today().strftime('%Y/%m/%d')
        date_today = datetime.datetime.strptime(date_buff, '%Y/%m/%d')
        global tender_basic_url,tender_param,tender_url_param
        tender_param = "&opt_pretty=1"
        tender_url_param = "?opt_pretty=1"
        tender_basic_url = "https://public.api.openprocurement.org/api/2.5/tenders"
        tender_last_url = "https://public.api.openprocurement.org/api/2.5/tenders?offset=last_page" + tender_param
        idx_check = 0
        idx_match = 0
        thread = 0
        with open("config.json", 'r') as response:
            config = json.load(response)
        with open("best.json", 'r') as response:
            best = json.load(response)

    def UpdateData(self):
        global tg_get_data
        tg_get_data = 0
        buffer_get_data = 0
        self.setStatusTip("Searching continued")










    def SetStatusTip(self):
        self.statusBar.showMessage("Checked: "+str(idx_check)+"   |   "+"Match: "+str(idx_match))
    def CheckIfExist(_date):
        global idx_check
        if Window.CheckByConfg(_date) == 1:
            return 1
        get_dateEndDate = re.search("(\d{4})-(\d{1,2})-(\d{2})", _date['data']['tenderPeriod']['endDate'])
        date = datetime.datetime.strptime(get_dateEndDate.group(1) + "/" + get_dateEndDate.group(2) + "/" + get_dateEndDate.group(3), '%Y/%m/%d')
        if date < date_today:
            return 1
        idx=0

        while idx < len(list_id):
            idx_c=idx+1
            while idx_c < len(list_id):
                if list_id[idx] == list_id[idx_c]:
                    return 1
                idx_c=idx_c+1
            idx=idx+1
        return 0

    def CheckByConfg(data):
        if Window.CheckConfig() == 1:
            if config['searchByKeyWords'] == "yes":
                list_keywords = config['keyWords']
                if not list_keywords:
                    pass
                else:
                    title_c = data['data']['title']
                    description_c = data['data']['items'][0]['description']
                    print(description_c)
                    for i in list_keywords:
                        if i.lower() in description_c.lower():
                            word = i
                            break
                        elif i.lower() in title_c.lower():
                            word = i
                            break
                        word = i

                    if str(word).lower() not in description_c.lower():
                        return 1
                    elif str(word).lower() not in title_c.lower():
                        return 1
                    else:
                        pass


            if config['searchByPrice'] == "yes":
                checkMinPrice = config['priceMin']
                checkMaxPrice = config['priceMax']
                if checkMinPrice == "0":
                    pass
                else:
                    if float(checkMinPrice) > float(data['data']['value']['amount']):

                        return 1
                if checkMaxPrice == "0":
                    pass
                else:
                    if float(checkMaxPrice) < float(data['data']['value']['amount']):
                        return 1

            if config['searchBylocality'] == "yes":
                list_localities = config['locality']
                if not list_localities[-1]:
                    for i in list_localities:
                        if str(i).lower() in str(data['data']['procuringEntity']['address']['locality']).lower():
                            loc = i
                            break
                        loc = i
                    if str(loc).lower() not in str(data['data']['procuringEntity']['address']['locality']).lower():
                        return 1
                    else:
                        pass

            if config['searchByStartDate'] == "yes":
                datelow_buf = re.search("(\d{2})/(\d{2})/(\d{4})", config['startDate'])
                datelow = datetime.datetime.strptime(datelow_buf.group(3) + "/" + datelow_buf.group(2) +"/"+ datelow_buf.group(1), '%Y/%m/%d')

                lowDate_buf = re.search("(\d{4})-(\d{1,2})-(\d{2})",data['data']['tenderPeriod']['endDate'])
                lowDate = datetime.datetime.strptime(lowDate_buf.group(1) + "/" + lowDate_buf.group(2) + "/" + lowDate_buf.group(3), '%Y/%m/%d')

                if str(datelow) == "0000/00/00":
                    pass
                else:
                    if datelow > lowDate:
                        return 1
                    else:
                        pass

            if config['searchByEndDate'] == "yes":
                dateEnd = config['endDate']
                dateEnd_buf = re.search("(\d{2})/(\d{2})/(\d{4})", config['endDate'])
                dateEnd = datetime.datetime.strptime(dateEnd_buf.group(3) + "/" + dateEnd_buf.group(2) +"/"+ dateEnd_buf.group(1), '%Y/%m/%d')

                endDate_buf = re.search("(\d{4})-(\d{1,2})-(\d{2})",data['data']['tenderPeriod']['endDate'])
                endDate = datetime.datetime.strptime(endDate_buf.group(1) + "/" + endDate_buf.group(2) + "/" + endDate_buf.group(3), '%Y/%m/%d')

                if str(dateEnd) == "0000/00/00":
                    pass
                else:
                    if dateEnd < endDate:
                        return 1
                    else:
                        pass

            if config['searchByMethod'] == "yes":
                method_search = config['method']

                if str(method_search).lower() in str(data['data']['status']).lower():
                    pass
                else:
                    return 1

        return 0


    def CheckConfig():

        for i in config:
            if config[i] == "yes":
                return 1
        return 0

    def CreateTable(self):
        global tableWidget, tableWidget_saved, best
        tableWidget_saved = SaveTabWidget()
        tableWidget_saved.setColumnCount(10)
        tableWidget = AllTabWidget()
        tableWidget.setColumnCount(10)
        tableWidget.setSortingEnabled(True)

        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidget.cellClicked.connect(self.cellClick)
        tableWidget_saved.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidget_saved.cellClicked.connect(self.cellClick_saved)

        tableWidget.setHorizontalHeaderLabels(['Status','Method','Price', 'Title', 'Email', 'Code', 'Locality', 'Started', 'End','Description'])
        tableWidget_saved.setHorizontalHeaderLabels(['Status','Method','Price', 'Title', 'Email', 'Code', 'Locality', 'Started', 'End','Description'])
        header =tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tableWidget.setColumnWidth(3,300)
        header_v = tableWidget.verticalHeader()
        header_v.setDefaultSectionSize(100)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.Stretch)
        header_saved = tableWidget_saved.horizontalHeader()
        header_saved.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tableWidget_saved.setColumnWidth(2,300)
        tableWidget_saved.resizeRowsToContents()
        header_saved.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header_saved.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header_saved.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header_saved.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header_saved.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header_saved.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header_saved.setSectionResizeMode(9, QHeaderView.Stretch)

        idx=0
        while idx < len(list(best.keys())):
            tableWidget_saved.insertRow(idx)
            tableWidget_saved.setItem(idx,0, QTableWidgetItem(str(best[str(idx)]['procurementMethod'])))
            tableWidget_saved.setItem(idx,1, QTableWidgetItem(str(best[str(idx)]['status'])))
            tableWidget_saved.setItem(idx,2, QTableWidgetItem(str(best[str(idx)]['price'])))
            tableWidget_saved.setItem(idx,3, QTableWidgetItem(str(best[str(idx)]['title'])))
            tableWidget_saved.setItem(idx,4, QTableWidgetItem(str(best[str(idx)]['email'])))
            tableWidget_saved.setItem(idx,5, QTableWidgetItem(str(best[str(idx)]['postalCode'])))
            tableWidget_saved.setItem(idx,6, QTableWidgetItem(str(best[str(idx)]['locality'])))
            tableWidget_saved.setItem(idx,7, QTableWidgetItem(str(Window.set_Date(best[str(idx)]['startDate']))))
            tableWidget_saved.setItem(idx,8, QTableWidgetItem(str(Window.set_Date(best[str(idx)]['endDate']))))
            tableWidget_saved.setItem(idx,9, QTableWidgetItem(str(best[str(idx)]['description'])))
            idx=idx+1











    def cellClick_saved(self,row,col):
        r= tableWidget_saved.selectedIndexes()[0]
        data_s = {}
        self.GetDataInRow_saved(r.row())
        data_s['procurementMethod'] = self.row_procurementMethod
        data_s['startDate'] = self.row_startDate
        data_s['endDate'] = self.row_endDate
        data_s['status'] = self.row_status
        data_s['price'] = self.row_price
        data_s['currency'] = self.row_currency
        data_s['title'] = self.row_title
        data_s['description'] = self.row_description
        data_s['email'] = self.row_email
        data_s['telephone'] = self.row_telephone
        data_s['locality'] = self.row_locality
        data_s['postalCode'] = self.row_postalCode
        data_s['awardCriteria'] = self.row_awardCriteria
        data_s['id'] = self.row_id
        self.dialogTable_save = ClickDialog(data_s, parent=None)
        self.dialogTable_save.show()

    def GetDataInRow_saved(self,row):
        with open("best.json", 'r') as response:
            buffer = json.load(response)
        self.row_price = buffer[str(row)]['price']
        self.row_currency = buffer[str(row)]['currency']
        self.row_description = buffer[str(row)]['description']
        self.row_email = buffer[str(row)]['email']
        self.row_endDate = buffer[str(row)]['endDate']
        self.row_startDate = buffer[str(row)]['startDate']
        self.row_locality = buffer[str(row)]['locality']
        self.row_title = buffer[str(row)]['title']
        self.row_postalCode = buffer[str(row)]['postalCode']
        self.row_id = buffer[str(row)]['id']
        self.row_procurementMethod = buffer[str(row)]['procurementMethod']
        self.row_status = buffer[str(row)]['status']
        self.row_telephone = buffer[str(row)]['telephone']
        self.row_awardCriteria = buffer[str(row)]['awardCriteria']
    def GetDataInRow(self,row):
        self.row_price = list_price[row]
        self.row_currency = list_currency[row]
        self.row_description = list_description[row]
        self.row_email = list_email[row]
        self.row_endDate = list_endDate[row]
        self.row_startDate = list_startDate[row]
        self.row_locality = list_locality[row]
        self.row_title = list_title[row]
        self.row_postalCode = list_postCode[row]
        self.row_id = list_id[row]
        self.row_procurementMethod = list_procurementMethod[row]
        self.row_status = list_status[row]
        self.row_telephone = list_telephone[row]
        self.row_awardCriteria = list_awardCriteria[row]
    def cellClick(self,row,col):
        r= tableWidget.selectedIndexes()[0]
        data_s = {}
        self.GetDataInRow(r.row())
        data_s['procurementMethod'] = self.row_procurementMethod
        data_s['startDate'] = self.row_startDate
        data_s['endDate'] = self.row_endDate
        data_s['status'] = self.row_status
        data_s['price'] = self.row_price
        data_s['currency'] = self.row_currency
        data_s['title'] = self.row_title
        data_s['description'] = self.row_description
        data_s['email'] = self.row_email
        data_s['telephone'] = self.row_telephone
        data_s['locality'] = self.row_locality
        data_s['postalCode'] = self.row_postalCode
        data_s['awardCriteria'] = self.row_awardCriteria
        data_s['id'] = self.row_id
        self.dialogTable = ClickDialog(data_s)
        self.dialogTable.show()

    def set_Date(Date):
        get_date = re.search("(\d{4})-(\d{1,2})-(\d{2})", Date)
        return str(get_date.group(3)) +"/"+ str(get_date.group(2)) +"/"+ str(get_date.group(1))

    def PutRow():
        idx = len(list_currency)-1
        currentRowCount = tableWidget.rowCount()
        tableWidget.insertRow(currentRowCount)
        tableWidget.setItem(currentRowCount,0, QTableWidgetItem(str(list_procurementMethod[idx])))
        tableWidget.setItem(currentRowCount,1, QTableWidgetItem(str(list_status[idx])))
        tableWidget.setItem(currentRowCount,2, QTableWidgetItem(str(list_price[idx])))
        tableWidget.setItem(currentRowCount,3, QTableWidgetItem(str(list_title[idx])))
        tableWidget.setItem(currentRowCount,4, QTableWidgetItem(str(list_email[idx])))
        tableWidget.setItem(currentRowCount,5, QTableWidgetItem(str(list_postCode[idx])))
        tableWidget.setItem(currentRowCount,6, QTableWidgetItem(str(list_locality[idx])))
        tableWidget.setItem(currentRowCount,7, QTableWidgetItem(str(Window.set_Date(list_startDate[idx]))))
        tableWidget.setItem(currentRowCount,8, QTableWidgetItem(str(Window.set_Date(list_endDate[idx]))))
        tableWidget.setItem(currentRowCount,9, QTableWidgetItem(str(list_description[idx])))




if __name__ == '__main__':

    #Setup the application window
    app = QApplication(sys.argv)
    window = Window()





    #Execute and cleanup
    app.exec_()
