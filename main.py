import sys
from os import path
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QProgressBar, QPushButton, QListWidget,
                             QTextEdit, QLabel, QFileDialog)
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from utils import setup_driver, setup_sheets

rs_date_col = []
rs_time_col = []
rs_keyword_col = []
rs_position_col = []
rs_domain_col = []
rs_header_col = []
rs_url_col = []


def build_df(date_col, time_col, keyword_col, position_col, domain_col, header_col, url_col):
    for d in date_col:
        rs_date_col.append(d)
    for t in time_col:
        rs_time_col.append(t)
    for k in keyword_col:
        rs_keyword_col.append(k)
    for p in position_col:
        rs_position_col.append(p)
    for dom in domain_col:
        rs_domain_col.append(dom)
    for h in header_col:
        rs_header_col.append(h)
    for u in url_col:
        rs_url_col.append(u)


def write_df():
    data = {'Date': rs_date_col, 'Time': rs_time_col, 'Keyword': rs_keyword_col,
            'TS Position': rs_position_col, 'Domain': rs_domain_col,
            'Header': rs_header_col, 'URL': rs_url_col}
    df = pd.DataFrame(data)
    wks = setup_sheets(0)
    rec_count = len(wks.col_values(1))
    start_col = 'A'
    end_col = 'G'
    start_row = rec_count + 1
    end_row = start_row + len(rs_date_col)
    wks.update(start_col + str(start_row) + ':' + end_col + str(end_row), df.values.tolist())


def get_time(time_format):
    now = datetime.now()
    if time_format == 'd':
        return now.strftime("%d/%m/%Y")
    elif time_format == 't':
        return now.strftime("%H:%M:%S %p")


class SearchThread(QThread):
    """
    A thread class that handles the background execution of a keyword search operation.
    """
    add_result = pyqtSignal(str, int)
    update_label = pyqtSignal(str)

    def __init__(self, keywords):
        QThread.__init__(self)
        self.keywords = keywords

    def __del__(self):
        self.wait()

    def run(self):
        self.add_result.emit('setting up driver', 0)
        driver = setup_driver()
        self.add_result.emit('Getting search results', 0)
        for keyword in self.keywords:
            search_result = self.get_search_results(keyword, driver)
            self.add_result.emit(search_result, 1)
            # self.sleep(2)
        self.add_result.emit('Writing data to Google Sheets', 0)
        write_df()
        driver.quit()

    def get_search_results(self, keyword, driver):
        result = ''
        ts_date_col = []
        ts_time_col = []
        ts_keyword_col = []
        ts_position_col = []
        ts_domain_col = []
        ts_header_col = []
        ts_url_col = []

        ts_position = 0
        ts_count = 0

        search_word = keyword.replace(' ', '+')
        for i in range(1):
            matched_elements = driver.get("https://www.google.com/search?q=" +
                                          keyword + "&start=" + str(i))
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        ts_match = soup.find('h3', {'class': 'GmE3X'})
        if ts_match and ts_match.text == 'Top stories':

            scroll_section = driver.find_elements_by_xpath("//g-scrolling-carousel")
            for scroll in scroll_section:
                driver.execute_script("arguments[0].scrollIntoView();", scroll)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            title_divs = soup.find_all('div', {'class': 'E7YbUb'})
            if len(title_divs) > 2:
                for td in title_divs:
                    ts_title = ''
                    ts_position += 1
                    ts_count += 1

                    ts_date_col.append(get_time('d'))
                    ts_time_col.append(get_time('t'))

                    ts_keyword_col.append(keyword)
                    ts_position_col.append(ts_position)

                    title_name = td.find('div', {'class': 'mCBkyc oz3cqf p5AXld nDgy9d'})
                    if title_name and title_name.text:
                        ts_title = title_name.text
                    else:
                        title_name = td.find('div', {'class': 'mCBkyc oz3cqf p5AXld jBgGLd'})

                    if title_name and title_name.text:
                        ts_title = title_name.text
                    else:
                        title_name = td.find('div', {'class': 'mCBkyc oz3cqf p5AXld jBgGLd OSrXXb'})

                    if title_name and title_name.text:
                        ts_title = title_name.text

                    title_link = td.find('a', {'class': 'WlydOe'})
                    if title_link:
                        if title_link['href']:
                            url_string = title_link['href']
                            beg_str_index = 12
                            end_str_index = url_string.find('.com')
                            if end_str_index < beg_str_index:
                                end_str_index = url_string.find('.org')
                            if end_str_index < beg_str_index:
                                end_str_index = url_string.find('.net')

                            domain = url_string[beg_str_index:end_str_index]
                            ts_domain_col.append(domain)
                            ts_header_col.append(ts_title)
                            ts_url_col.append(url_string)

        else:
            result = 'No top stories found for ' + search_word

            ts_date_col.append(get_time('d'))
            ts_time_col.append(get_time('t'))
            ts_keyword_col.append(keyword)
            ts_position_col.append(0)
            ts_domain_col.append('N/A')
            ts_header_col.append('N/A')
            ts_url_col.append('N/A')

        result = str(ts_count) + ' top stories found for ' + keyword
        build_df(ts_date_col, ts_time_col, ts_keyword_col, ts_position_col, ts_domain_col, ts_header_col, ts_url_col)
        return result


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        # super(self.__class__, self).__init__()
        uic.loadUi('gsgui.ui', self)
        self.btn_start = self.findChild(QPushButton, "btn_start")
        self.btn_stop = self.findChild(QPushButton, "btn_stop")
        self.btn_import = self.findChild(QPushButton, "btn_import")
        self.btn_clear = self.findChild(QPushButton, "btn_clear")
        self.pb = self.findChild(QProgressBar, "progress_bar")
        self.list_results = self.findChild(QListWidget, "list_results")
        self.text_keywords = self.findChild(QTextEdit, "text_keywords")
        self.label_keywords_value = self.findChild(QLabel, "label_keywords_value")
        self.btn_start.clicked.connect(self.start_getting_search_results)
        self.btn_import.clicked.connect(self.btn_import_clicked)
        self.btn_clear.clicked.connect(self.btn_clear_clicked)

        self.text_keywords.textChanged.connect(self.list_text_changed)

        self.show()

        self.read_text_file()

    def list_text_changed(self):
        keyword_list_text = self.text_keywords.toPlainText()
        if keyword_list_text:
            data = keyword_list_text.splitlines()
            self.label_keywords_value.setText(str(len(data)))

    def read_text_file(self):
        file_found = path.exists("data/keywords.txt")
        if file_found:
            with open('data/keywords.txt') as f:
                content = f.readlines()
                keyword_list = [x.strip() for x in content]
                self.text_keywords.clear()
                for word in keyword_list:
                    self.text_keywords.append(word)

    def btn_import_clicked(self):
        options = QFileDialog.Options()
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options)
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"An error occurred: {e}")
        if file_name:
            f = open(file_name).read()
            self.text_keywords.clear()
            self.text_keywords.append(f)
            print(file_name)

    def btn_clear_clicked(self):
        self.text_keywords.clear()
        self.text_keywords.setFocus()

    def start_getting_search_results(self):
        keyword_list = []
        keyword_list_text = self.text_keywords.toPlainText()
        if keyword_list_text:
            keyword_list = keyword_list_text.splitlines()

        self.pb.setMaximum(len(keyword_list))
        self.pb.setValue(0)

        self.search_instance = SearchThread(keyword_list)
        self.search_instance.start()
        self.search_instance.finished.connect(self.done)
        self.search_instance.add_result.connect(self.add_result)

        self.btn_stop.setEnabled(True)
        self.btn_stop.clicked.connect(self.search_instance.terminate)
        self.btn_start.setEnabled(False)

        start_str = 'Searching ' + str(len(keyword_list)) + ' keywords'
        self.search_instance.add_result.emit(start_str, 0)

    def add_result(self, result_text, progress):
        self.list_results.addItem(result_text)
        if progress == 1:
            self.pb.setValue(self.pb.value() + 1)

    def done(self):
        self.btn_stop.setEnabled(False)
        self.btn_start.setEnabled(True)
        self.pb.setValue(0)
        self.list_results.addItem('Completed all tasks')
        QMessageBox.information(self, "Done!", "Done fetching search results")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
