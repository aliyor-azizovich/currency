import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re


class RealTimeCurrencyConverter:
    def __init__(self, url):
        # Получаем данные о курсах валют
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        # Ограничение точности до 4 знаков после запятой
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Конвертер валют')
        self.currency_converter = converter

        self.geometry("500x300")
        self.configure(bg='#f0f8ff')  # Цвет фона для окна

        # Метка приветствия
        self.intro_label = Label(self, text='Добро пожаловать в конвертер валют', fg='#4a90e2', bg='#f0f8ff', relief=tk.RAISED, borderwidth=3)
        self.intro_label.config(font=('Arial', 20, 'bold'))

        # Метка с курсом валют и датой
        self.date_label = Label(self, text=f"1 УЗБЕКСКИЙ СУМ = {self.currency_converter.convert('UZS', 'USD', 1)} USD \n Дата: {self.currency_converter.data['date']}", fg='#333', bg='#f0f8ff', relief=tk.GROOVE, borderwidth=5)
        self.date_label.config(font=('Arial', 14))

        self.intro_label.place(x=10, y=10)
        self.date_label.place(x=10, y=60, width=480)

        # Поле для ввода суммы
        valid = (self.register(self.restrict_number_only), '%d', '%P')
        self.amount_field = Entry(self, bd=3, relief=tk.RIDGE, justify=tk.CENTER, validate='key', validatecommand=valid, bg='#e6f7ff', font=('Arial', 12))
        self.converted_amount_field_label = Label(self, text='', fg='#4a90e2', bg='#e6f7ff', relief=tk.RIDGE, justify=tk.CENTER, width=17, borderwidth=3, font=('Arial', 14))

        # Выпадающие списки для выбора валют
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("UZS")  # значение по умолчанию
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")  # значение по умолчанию

        font = ("Arial", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable, values=list(self.currency_converter.currencies.keys()), font=font, state='readonly', width=12, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable, values=list(self.currency_converter.currencies.keys()), font=font, state='readonly', width=12, justify=tk.CENTER)

        # Размещение элементов интерфейса
        self.from_currency_dropdown.place(x=30, y=120)
        self.amount_field.place(x=30, y=160)
        self.to_currency_dropdown.place(x=340, y=120)
        self.converted_amount_field_label.place(x=320, y=160)

        # Кнопка для конвертации
        self.convert_button = Button(self, text="Конвертировать", fg="#ffffff", bg="#4a90e2", command=self.perform, font=('Arial', 12, 'bold'))
        self.convert_button.place(x=200, y=200, width=200)

    def perform(self):
        try:
            # Получение и обработка введенной суммы и валют
            amount = float(self.amount_field.get())
            from_curr = self.from_currency_variable.get()
            to_curr = self.to_currency_variable.get()

            # Конвертация и отображение результата
            converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
            converted_amount = round(converted_amount, 2)

            self.converted_amount_field_label.config(text=str(converted_amount))
        except ValueError:
            self.converted_amount_field_label.config(text="Некорректный ввод")

    def restrict_number_only(self, action, string):
        # Регулярное выражение для проверки корректности ввода числа
        regex = re.compile(r"^\d*\.?\d*$")
        result = regex.match(string)
        return (string == "" or result is not None)


if __name__ == '__main__':
    # URL для получения данных о курсах валют
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    app = App(converter)
    app.mainloop()
