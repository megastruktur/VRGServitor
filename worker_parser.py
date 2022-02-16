import pygsheets
import datetime
from dotenv import load_dotenv
import os
import pytz
import locale
import pymorphy2

load_dotenv()

LOCALE = os.environ.get('LOCALE')
DEFAULT_TIMEZONE = 'Europe/Minsk'
locale.setlocale(locale.LC_TIME, LOCALE)

workers_tg = {
    'Артём': '@grizzlbear',
    'Дмитрий': '@G_no_W',
    'Летис': '@Letya_Pudeev',
    'Иван': '@MrKio',
    'Даниил': '@dutyala',
    'Даник': '@dutyala',
    'Костя': '@Arkatick',
}

days_off = ['В', 'ОВ']

SHEET_ID = os.environ.get('SHEET_ID')
TABLE_ROW_LENGTH = 33


def sheet_get_sheet():
    gc = pygsheets.authorize(service_file='service_account_secret.json')
    sheet = gc.open_by_key(SHEET_ID)
    return sheet.worksheet('title', 'ГРАФИК')


def get_workers_from_graph(tab, start_row_num, lines_per_worker):
    worker_cell = pygsheets.Address((start_row_num + 1, 1))
    workers = []
    while tab.cell(worker_cell).value != '':
        workers.append(tab.cell(worker_cell).value)
        worker_cell = worker_cell + (lines_per_worker, 0)
    return workers


def sheet_work_today_finder(dt, tab, with_usernames, lines_per_worker):
    m = pymorphy2.MorphAnalyzer()
    month = dt.strftime('%B')
    month_name = m.parse(month)[0].inflect({'nomn'}).word.title()
    search_str = month_name + '\'' + dt.strftime('%-y')
    row_num = tab.find(search_str)[0].row

    work_today = []
    workers = get_workers_from_graph(tab, row_num, lines_per_worker)

    address1 = pygsheets.Address((row_num, 1))
    hawking_variable = 1

    if tab.cell(address1 + (lines_per_worker, 1)).value != 'плановое':
        hawking_variable = 2

    address2 = pygsheets.Address((row_num + len(workers) * hawking_variable, TABLE_ROW_LENGTH))
    shifts = tab.range(address1.label + ':' + address2.label, returnas='matrix')

    for z in range(len(workers)):
        delta = z * hawking_variable
        if shifts[delta + 1][dt.day + 1] not in days_off:
            worker_name = shifts[delta + 1][0]
            if with_usernames and worker_name in workers_tg:
                worker_name += ' (' + workers_tg[worker_name] + ')'
            work_today.append(worker_name)
    return work_today


def sheet_get_workers(with_usernames=False, dt=None):
    if not dt:
        dt = datetime.datetime.now(pytz.timezone(DEFAULT_TIMEZONE))

    # Previously we had 2 rows per worker, now we have 1 row per worker
    lines_per_worker = 1
    if dt < datetime.datetime(2022, 2, 1, 0, 0, 0, 0, pytz.timezone(DEFAULT_TIMEZONE)):
        lines_per_worker = 2
    tab = sheet_get_sheet()
    return sheet_work_today_finder(dt, tab, with_usernames, lines_per_worker)


def main():
    # dt = datetime.datetime.now(pytz.timezone('Europe/Minsk'))
    dt = datetime.datetime(2022, 2, 4, 0, 0, 0, 0, pytz.timezone(DEFAULT_TIMEZONE))
    print(sheet_get_workers(True, dt))
    print(sheet_get_workers(True))


if __name__ == "__main__":
    main()
