import pygsheets
import datetime
from dotenv import load_dotenv
import os
import pytz
import locale
import pymorphy2

load_dotenv()

LOCALE = os.environ.get('LOCALE')

locale.setlocale(locale.LC_TIME, LOCALE)

workers = {
    'Артём': '@grizzlbear',
    'Дмитрий': '@G_no_W',
    'Летис': '@Letya_Pudeev',
    'Иван': '@MrKio',
}

days_off = ['В', 'ОВ']

SHEET_ID = os.environ.get('SHEET_ID')


def sheet_get_sheet():
    gc = pygsheets.authorize(service_file='service_account_secret.json')
    sheet = gc.open_by_key(SHEET_ID)
    return sheet.worksheet('title', 'ГРАФИК')


def sheet_work_today_finder(dt, tab, with_usernames):
    m = pymorphy2.MorphAnalyzer()
    month = dt.strftime('%B')
    month_name = m.parse(month)[0].inflect({'nomn'}).word.title()
    search_str = month_name + '\'' + dt.strftime('%-y')
    row_num = tab.find(search_str)[0].row

    work_today = []

    address1 = pygsheets.Address((row_num, 1))
    address2 = pygsheets.Address((row_num + len(workers), 33))
    shifts = tab.range(address1.label + ':' + address2.label, returnas='matrix')

    for z in range(len(workers)):
        if shifts[z + 1][dt.day + 1] not in days_off:
            worker_name = shifts[z + 1][0]
            if with_usernames:
                worker_name += ' (' + workers[worker_name] + ')'
            work_today.append(worker_name)
    return work_today


def sheet_get_workers(with_usernames=False, dt=False):
    if not dt:
        dt = datetime.datetime.now(pytz.timezone('Europe/Minsk'))
    tab = sheet_get_sheet()
    return sheet_work_today_finder(dt, tab, with_usernames)


def main():
    print(sheet_get_workers())


if __name__ == "__main__":
    main()
