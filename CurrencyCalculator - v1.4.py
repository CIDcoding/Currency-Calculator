import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap #for images
from PyQt5.QtGui import QFont  #for font size

## back-end code ##########################################
import datetime
from forex_python.converter import CurrencyRates
import decimal


class Window(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Load the UI Page - added path too
        uic.loadUi("PS_calculator_UI - vf.ui", self)

        ### currency section ####
        self.from_currency_input = self.findChild(QComboBox, 'from_currency')
        self.to_currency_input = self.findChild(QComboBox, 'to_currency')
        self.exchange_rate_output = self.findChild(QLineEdit, 'rate')
        self.exchange_currency = self.findChild(QPushButton, 'exchange_btn')
        self.exchange_currency.clicked.connect(self.exchange_from_to)

        ##### conversion section ####
        self.transfer_price_input = self.findChild(QLineEdit, 'transfer_price')
        self.converted_price_output = self.findChild(QLineEdit, 'conv_price')
        self.convert_button = self.findChild(QPushButton, 'convert_btn')
        self.convert_button.clicked.connect(self.convert_amount)

        #### add profit section #####
        self.preset_margin_input = self.findChild(QSpinBox, 'preset_margin')
        self.add_preset_margin_button = self.findChild(QPushButton, 'add_profit_btn')
        self.add_preset_margin_button.clicked.connect(self.add_profit_margin)
        self.custom_margin_input = self.findChild(QLineEdit, 'custom_margin')
        self.add_custom_margin_button = self.findChild(QPushButton, 'add_custom_margin_btn')
        self.add_custom_margin_button.clicked.connect(self.add_custom_profit_margin)

        #### sales section #####
        self.final_sales_price = self.findChild(QLineEdit, 'sales_price')
        self.refresh_sales = self.findChild(QPushButton, 'refresh_sales')
        self.refresh_sales.clicked.connect(self.refresh_sales_calculator)

        #### My profit section #####
        self.prof_transfer_currency = self.findChild(QComboBox, 'transfer_currency')
        self.prof_transfer_price = self.findChild(QLineEdit, 'transfer_price_prof')
        self.prof_sales_currency = self.findChild(QComboBox, 'sales_currency')
        self.prof_sales_price = self.findChild(QLineEdit, 'sales_price_prof')
        self.prof_current_rate = self.findChild(QLineEdit, 'current_r')
        self.prof_custom_rate = self.findChild(QLineEdit, 'custom_r')
        self.prof_get_rate = self.findChild(QPushButton, 'get_rate_btn')
        self.prof_get_rate.clicked.connect(self.display_prof_rate)

        #### calculate profit setion ####
        self.get_profit = self.findChild(QPushButton, 'get_profit_btn')
        self.get_profit.clicked.connect(self.calculate_my_profit)
        self.profit_current = self.findChild(QLineEdit, 'current_profit')
        self.profit_custom = self.findChild(QLineEdit, 'custom_profit')
        self.refresh_profit = self.findChild(QPushButton, 'refresh_profit')
        self.refresh_profit.clicked.connect(self.refresh_profit_section)
        self.refresh = self.findChild(QPushButton, 'refresh_all')
        self.refresh.clicked.connect(self.refresh_calculator)

        self.show()

    ''' exchange currency after pressing the Exchange button'''

    def exchange_from_to(self):
        from_c = self.from_currency_input.currentText()
        to_c = self.to_currency_input.currentText()
        # currency rates
        cr = CurrencyRates(force_decimal=True)
        # at local time
        local_time = datetime.datetime.now()
        print(local_time)
        current_rate = cr.get_rate(from_c, to_c, local_time)
        print(current_rate)
        #actual_rate = current_rate - decimal.Decimal(0.02)
        # change text in Exchange rate display
        self.exchange_rate_output.setText(str(round(current_rate,5)))

        if self.from_currency_input.currentText() == 'GBP':
            self.transfer_price_input.setPlaceholderText('£')
        elif self.from_currency_input.currentText() == 'USD':
            self.transfer_price_input.setPlaceholderText('$')
        elif self.from_currency_input.currentText() == 'EUR':
            self.transfer_price_input.setPlaceholderText('€')
        elif self.from_currency_input.currentText() == 'JPY':
            self.transfer_price_input.setPlaceholderText('¥')

        return from_c, to_c, cr, local_time

    ''' Convert entered amount at the current exchange rate after pressing the convert button'''

    def convert_amount(self):
        from_c = self.from_currency_input.currentText()
        to_c = self.to_currency_input.currentText()
        # currency rates
        cr = CurrencyRates(force_decimal=True)
        # at local time
        local_time = datetime.datetime.now()
        current_rate = cr.get_rate(from_c, to_c, local_time)
        to_exchange = self.transfer_price_input.text()
        #new_currency = cr.convert(from_c, to_c, decimal.Decimal(to_exchange), local_time)
        new_currency = decimal.Decimal(to_exchange)*(current_rate - decimal.Decimal(0.02))

        self.converted_price_output.setText(str(round(new_currency, 5)))

        if self.to_currency_input.currentText() == 'GBP':
            self.converted_price_output.setText(' £ ' + str(round(new_currency)))
        elif self.to_currency_input.currentText() == 'EUR':
            self.converted_price_output.setText(' € ' + str(round(new_currency)))
        elif self.to_currency_input.currentText() == 'USD':
            self.converted_price_output.setText(' $ ' + str(round(new_currency)))
        elif self.to_currency_input.currentText() == 'JPY':
            self.converted_price_output.setText(' ¥ ' + str(round(new_currency)))

    ''' add preset profit margin and calculate final sales price '''

    def add_custom_profit_margin(self):
        # from and To
        from_c = self.from_currency_input.currentText()
        to_c = self.to_currency_input.currentText()
        # currency rates
        cr = CurrencyRates(force_decimal=True)
        # at local time
        local_time = datetime.datetime.now()
        current_rate = cr.get_rate(from_c, to_c, local_time)
        actual_rate = current_rate - decimal.Decimal(0.02)
        to_exchange = self.transfer_price_input.text()
        # new_currency = cr.convert(from_c, to_c, decimal.Decimal(to_exchange), local_time)
        #converted_price_current = cr.convert(from_c, to_c, decimal.Decimal(to_exchange), local_time)
        converted_price = decimal.Decimal(to_exchange) * actual_rate
        ### adding custom profit ###
        custom_profit = self.custom_margin_input.text()
        sales_price = round(
            decimal.Decimal(converted_price) * 100 / (100 - decimal.Decimal(custom_profit)))
        self.final_sales_price.setText(str(sales_price))

        if self.to_currency_input.currentText() == 'GBP':
            self.final_sales_price.setText(' £ ' + str(sales_price))
        elif self.to_currency_input.currentText() == 'EUR':
            self.final_sales_price.setText(' € ' + str(sales_price))
        elif self.to_currency_input.currentText() == 'USD':
            self.final_sales_price.setText(' $ ' + str(sales_price))



    def add_profit_margin(self):
        # from and To
        from_c = self.from_currency_input.currentText()
        to_c = self.to_currency_input.currentText()
        # currency rates
        cr = CurrencyRates(force_decimal=True) #current
        #cr_custom = self.custom_rate_input.text()
        # at local time
        local_time = datetime.datetime.now()
        current_rate = cr.get_rate(from_c, to_c, local_time)
        actual_rate = current_rate - decimal.Decimal(0.02)
        to_exchange = self.transfer_price_input.text()
        #converted_price_current = cr.convert(from_c, to_c, decimal.Decimal(to_exchange), local_time)
        #converted_price_custom = decimal.Decimal(to_exchange) * decimal.Decimal(cr_custom)
        converted_price = decimal.Decimal(to_exchange) * actual_rate
        ### adding custom profit ###
        preset_profit = self.preset_margin_input.value()
        sales_price = round(
            decimal.Decimal(converted_price) * 100 / (100 - decimal.Decimal(preset_profit)))
        #custom_sales_price = round(converted_price_custom * 100 / (100 - decimal.Decimal(preset_profit)))

        #self.current_sales_price.setText(str(current_sales_price))


        if self.to_currency_input.currentText() == 'GBP':
            self.final_sales_price.setText('£ ' + str(sales_price))
        elif self.to_currency_input.currentText() == 'EUR':
            self.final_sales_price.setText('€ ' + str(sales_price))
        elif self.to_currency_input.currentText() == 'USD':
            self.final_sales_price.setText('$ ' + str(sales_price))




    def refresh_sales_calculator(self):
        self.exchange_rate_output.setText('')
        #self.custom_rate_input.setText('')
        self.transfer_price_input.setText('')
        self.converted_price_output.setText('')
        self.custom_margin_input.setText('')
        self.final_sales_price.setText('')


    ''' calculate/ display profit rates'''

    def display_prof_rate(self):
        # from and To
        from_c = self.prof_sales_currency.currentText()
        to_c = self.prof_transfer_currency.currentText()
        #### prices #####
        # sales_price = self.prof_sales_price.text()
        # transfer_price = self.prof_transfer_price.text()
        # currency rates
        cr = CurrencyRates(force_decimal=True)
        # at local time
        local_time = datetime.datetime.now()
        current_rate = cr.get_rate(to_c, from_c, local_time)
        # to_exchange = decimal.Decimal(transfer_price)
        # converted_price = cr.convert(to_c, from_c, decimal.Decimal(to_exchange), local_time)
        self.prof_current_rate.setText(str(round(current_rate, 6)))

    ''' calculate profit from known final sales price and transfer price'''

    def calculate_my_profit(self):
        # from and To
        from_c = self.prof_sales_currency.currentText()
        to_c = self.prof_transfer_currency.currentText()
        #### prices #####
        sales_price = self.prof_sales_price.text()
        transfer_price = self.prof_transfer_price.text()
        # currency rates
        cr = CurrencyRates(force_decimal=True)
        # at local time
        local_time = datetime.datetime.now()
        current_rate = cr.get_rate(to_c, from_c, local_time)
        to_exchange = decimal.Decimal(transfer_price)
        converted_price = cr.convert(to_c, from_c, decimal.Decimal(to_exchange), local_time)
        ##### calculating profit ######
        my_profit = round(((1 - decimal.Decimal(converted_price) / decimal.Decimal(sales_price)) * 100), 1)
        self.profit_current.setText(str(my_profit) + '%')
        ### adding custom profit ###

        if self.prof_custom_rate.text():
            custom_conversion = decimal.Decimal(transfer_price) * decimal.Decimal(self.prof_custom_rate.text())
            custom_profit = round(((1 - decimal.Decimal(custom_conversion) / decimal.Decimal(sales_price)) * 100), 1)
            self.profit_custom.setText(str(custom_profit) + '%')

    ''' refresh all the profit section'''

    def refresh_profit_section(self):
        self.prof_transfer_price.setText('')
        self.prof_sales_price.setText('')
        self.prof_current_rate.setText('')
        self.prof_custom_rate.setText('')
        self.profit_current.setText('')
        self.profit_custom.setText('')

    ''' refresh entire calculator'''

    def refresh_calculator(self):
        self.exchange_rate_output.setText('')
        #self.custom_rate_input.setText('')
        self.transfer_price_input.setText('')
        self.converted_price_output.setText('')
        self.custom_margin_input.setText('')
        self.final_sales_price.setText('')
        #self.current_sales_price.setText('')
        self.prof_transfer_price.setText('')
        self.prof_sales_price.setText('')
        self.prof_current_rate.setText('')
        self.prof_custom_rate.setText('')
        self.profit_current.setText('')
        self.profit_custom.setText('')


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()

