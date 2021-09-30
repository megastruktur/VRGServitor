import pygsheets
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

days = {
 '1': 'C', '2': 'D', '3': 'E', '4': 'F', '5': 'G', '6': 'H', '7': 'I', '8': 'J', '9': 'K', '10': 'L', '11': 'M',
 '12': 'N', '13': 'O', '14': 'P', '15': 'Q', '16': 'R', '17': 'S', '18': 'T', '19': 'U', '20': 'V', '21': 'W',
 '22': 'X', '23': 'Y', '24': 'Z', '25': 'AA', '26': 'AB', '27': 'AC', '28': 'AD', '29': 'AE', '30': 'AF', '31': 'AG'
}

months = {
    '1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май', '6': 'Июнь', '7': 'Июль', '8': 'Август',
    '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
}

workers = {
    'Артём': '@grizzlbear',
    'Дмитрий': '@G_no_W',
    'Летис': '@Letya_Pudeev',
    'Иван': '@MrKio',
}

days_off = ['В', 'ОВ']

SHEET_ID = os.environ.get('SHEET_ID')

dt = datetime.datetime.today()

def sheet_get_sheet():
    gc = pygsheets.authorize(service_file='service_account_secret.json')
    sheet = gc.open_by_key(SHEET_ID)
    return sheet.worksheet('title', 'ГРАФИК')


def sheet_find_start_row(tab):
    search_str = months[str(dt.month)] + '\'' + str(dt.year)[-2:]
    for i in range(12, 10000, 6):
        if tab.cell('A' + str(i)).value == search_str:
            return i


def sheet_work_today_finder(tab, row_num):
    work_today = []
    c = 1
    for i in workers:
        if tab.cell(days[str(dt.day)] + str(row_num + c)).value not in days_off:
            work_today.append(tab.cell('A' + str(row_num + c)).value)
        c += 1
    return work_today


def sheet_get_workers():

    tab = sheet_get_sheet()
    row_num = sheet_find_start_row(tab)
    return sheet_work_today_finder(tab, row_num)


def main():
    print(sheet_get_workers())


if __name__ == "__main__":
    main()
