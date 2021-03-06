# ©LG, Peter the Great Polytechnical University, IBKS, 2020
# Developer: @GolovinEasyWin

# Библиотека PyQT5 позволяет разрабатывать GUI
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QProgressBar, QPushButton, QLabel

# Импортируем файлы с функциями и настройками для парсинга
import src.parse_functions as pf
import src.settings as st
import src.write_data as wd

# Выбор на исполнение ui-файла
Form, _ = uic.loadUiType("drom_parser.ui")


# Создание, запись в Excel-файл с последующим открытием
def start_csv(path):
    wd.start_file(path)


# Класс для работы с графическим интерфейсом пользователя (GUI)
class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('База объявлений auto.drom.ru')
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(290, 580, 531, 23)
        self.msgBox = QMessageBox(self)
        self.msgBox.setStyleSheet(
            "background-color: white;"
        )
        self.flag = QLabel(self)
        self.flag.setGeometry(80, 190, 251, 131)
        self.pixmap = QPixmap('images/japan.png')
        self.flag.setPixmap(self.pixmap)
        self.qbtn = QPushButton('Quit', self)
        self.UI_init()

    def UI_init(self):
        # Смена национального флага производителя автомобиля
        self.comboBoxAuto.currentIndexChanged.connect(self.choose_flag)

        # Активность при нажатии кнопки "Найти"
        self.searchButton.clicked.connect(self.searchButon_pressed)

    # Проверка checkBox "Автоматически открыть файл"
    def checkBox_condition(self, path):
        if self.checkBox.isChecked():
            start_csv(path)

    # Старт парсинга
    def searchButon_pressed(self):
        filter_region = self.filter_region()
        filter_car = self.filter_car()
        filter_price = self.filter_price()
        filter_year = self.filter_year()

        url = st.create_url(filter_region, filter_car, filter_year, filter_price)

        cars = pf.parse(url, self.progressBar)

        if len(cars) == 0:
            self.msgBox.setGeometry(750, 500, 300, 500)
            self.msgBox.setWindowTitle("Ошибка поиска")
            self.msgBox.setText("По данному запросу автомобилей не найдено")

            self.msgBox.exec()
            return -1

        wd.save_file(cars, wd.PATH_TO_FILE)
        self.checkBox_condition(wd.PATH_TO_FILE)

    # Обработка comboBox для выбора региона поиска
    def filter_region(self):
        region = self.comboBoxRegion.currentText()
        return region

    # Обработка MultiBox для выбора марки
    def filter_car(self):
        # Получение значения ComboBox для автомобиля
        car = self.comboBoxAuto.currentText()
        filter_data = car.lower()
        print(filter_data)
        return filter_data

    # Обработка MultiBox для ограничения года выпуска
    def filter_year(self):
        filter_year = ''
        st.year_from = self.comboBoxYear_1.currentText()
        st.year_to = self.comboBoxYear_2.currentText()

        if st.year_from != 'Любой' and st.year_to != 'Любой':
            # Если границы годов выпуска неправильные
            if st.year_from > st.year_to:
                tmp = st.year_to
                st.year_to = st.year_from
                st.year_from = tmp
            # Если указан один и тот же год выпуска
            elif st.year_from == st.year_to:
                return st.year_from
        if st.price_from == 'Любая' and st.price_to == 'Любая':
            if st.year_from != 'Любой' and st.year_to != 'Любой':
                filter_year = filter_year + '?minyear=' + st.year_from + '&maxyear=' + st.year_to
            elif st.year_from != 'Любой' and st.year_to == 'Любой':
                filter_year = filter_year + '?minyear=' + st.year_from
            elif st.year_from == 'Любой' and st.year_to != 'Любой':
                filter_year = filter_year + '?maxyear=' + st.year_to
        else:
            if st.year_from != 'Любой' and st.year_to != 'Любой':
                filter_year = filter_year + '&minyear=' + st.year_from + '&maxyear=' + st.year_to
            elif st.year_from != 'Любой' and st.year_to == 'Любой':
                filter_year = filter_year + '&minyear=' + st.year_from
            elif st.year_from == 'Любой' and st.year_to != 'Любой':
                filter_year = filter_year + '&maxyear=' + st.year_to

        print(filter_year)
        return filter_year

    # Обработка MultiBox для ограничения цены
    def filter_price(self):
        filter_price = ''
        st.price_from = self.comboBoxPrice_1.currentText().replace(' ', '')
        st.price_to = self.comboBoxPrice_2.currentText().replace(' ', '')

        if st.price_from != 'Любая' and st.price_to != 'Любая':
            # Если границы цены неправильные
            if int(st.price_from) > int(st.price_to):
                tmp = st.price_to
                st.price_to = st.price_from
                st.price_from = tmp

        if st.price_from != 'Любая' and st.price_to != 'Любая':
            filter_price = filter_price + '?minprice=' + st.price_from + '&maxprice=' + st.price_to
        elif st.price_from != 'Любая' and st.price_to == 'Любая':
            filter_price = filter_price + '?minprice=' + st.price_from
        elif st.price_from == 'Любая' and st.price_to != 'Любая':
            filter_price = filter_price + '?maxprice=' + st.price_to

        print(filter_price)
        return filter_price

    def choose_flag(self):
        auto = self.comboBoxAuto.currentText()
        if auto == 'Acura' or auto == 'Honda' or auto == 'Mitsubishi' or auto == 'Toyota' or auto == 'Subaru' or \
           auto == 'Suzuki' or auto == 'Nissan' or auto == 'Mazda' or auto == 'Lexus':
            pixmap = QPixmap('images/japan.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Audi' or auto == 'BMW' or auto == 'Opel' or auto == 'Volkswagen' or auto == 'Mercedes-Benz':
            pixmap = QPixmap('images/germany.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Ford' or auto == 'Chevrolet':
            pixmap = QPixmap('images/usa.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Kia' or auto == 'Daewoo' or auto == 'Hyundai':
            pixmap = QPixmap('images/korea.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Peugeot' or auto == 'Renault' or auto == 'Citroen':
            pixmap = QPixmap('images/france.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Volvo':
            pixmap = QPixmap('images/sweden.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Skoda':
            pixmap = QPixmap('images/cr.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Chery':
            pixmap = QPixmap('images/china.png')
            self.flag.setPixmap(pixmap)
        elif auto == 'Fiat':
            pixmap = QPixmap('images/italy.png')
            self.flag.setPixmap(pixmap)


if __name__ == '__main__':
    import sys
    # Создаем приложение
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
