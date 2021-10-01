import pygsheets
from datetime import datetime, time, timedelta, date
from dotenv import load_dotenv
import os
import locale
import pymorphy2

load_dotenv()

SHEET_ID = os.environ.get('SHEET_ID')
LOCALE = os.environ.get('LOCALE')

locale.setlocale(locale.LC_TIME, LOCALE)

time_start_shift = time(hour=12, minute=00)
time_end_shift = time(hour=23, minute=00)


devices = ['PS4', 'Rift_S_Lite', 'Rift_S_Heavy', 'PRO_1', 'PRO_2', 'VIVE_1', 'VIVE_2']

def get_sheet(title):
    gc = pygsheets.authorize(service_file='service_account_secret.json')
    sheet = gc.open_by_key(SHEET_ID)
    return sheet.worksheet('title', title)


# Retrieve schedule sheet
def get_schedule_sheet(dt: datetime):
    m = pymorphy2.MorphAnalyzer()
    month = dt.today().strftime('%B')

    new_month = m.parse(month)[0].inflect({'nomn'}).word.title()
    sheet_name = new_month + '\'' + dt.strftime('%-y')

    return get_sheet(sheet_name)


# Get the 1 and the last cell name
def get_schedule_sheet_bounds(schedule_sheet, dt: datetime, returnas='range'):

    items_in_a_row = 4
    day_row_start = dt.day // items_in_a_row
    day_col_start = 4 if dt.day % items_in_a_row == 0 else dt.day % items_in_a_row - 1
    start_cell = pygsheets.Address((50 * day_row_start + 3, (len(devices) + 1) * day_col_start + 2))
    end_cell = start_cell + (47, len(devices) - 1)

    return schedule_sheet.range(start_cell.label + ':' + end_cell.label, returnas=returnas)


# Get full schedule
def get_schedule(dt: datetime):
    schedule_sheet = get_schedule_sheet(dt)
    schedule_datarange = get_schedule_sheet_bounds(schedule_sheet, dt)

    mrs = schedule_sheet.merged_ranges

    # Identify Schedules
    schedule_ranges = []
    for r in mrs:
        if is_range_in_range(r, schedule_datarange):
            schedule_ranges.append(r)

    # Parse Schedules
    schedules = []

    # Retrieve as matrix to speed up as every call to sheet takes time.
    schedule_datarange_matrix = get_schedule_sheet_bounds(schedule_sheet, dt, 'matrix')
    for schedule in schedule_ranges:

        # get time
        row_in_range_start = schedule.start[0] - schedule_datarange.start_addr[0]
        row_in_range_end = schedule.end[0] - schedule_datarange.start_addr[0]

        schedule_time_start = datetime.combine(date.today(), time_start_shift) + timedelta(
            minutes=15*row_in_range_start)
        schedule_time_end = datetime.combine(date.today(), time_start_shift) + timedelta(
            minutes=15*row_in_range_end)

        # get devices
        col_in_range_start = schedule.start[1] - schedule_datarange.start_addr[1]
        col_in_range_end = schedule.end[1] - schedule_datarange.start_addr[1]
        scheduled_devices = []
        for di in range(col_in_range_start, col_in_range_end):
            scheduled_devices.append(devices[di])
        # print(scheduled_devices)

        # Get schedule description
        description = schedule_datarange_matrix[row_in_range_start][col_in_range_start]
        # print([schedule_time_start.strftime('%H:%I'), schedule_time_start])
        schedules.append({
            'time_start': schedule_time_start.strftime('%H:%M'),
            'time_end': schedule_time_end.strftime('%H:%M'),
            'devices': scheduled_devices,
            'description': description,
        })

    return sorted(schedules, key=lambda i: (i['time_start']))


# Retrieve Merges in schedule bounds as long as we can only get ALL the merges from the list.
def get_merges_in_schedule_bounds():
    pass


# Is small range contained within the big range
def is_range_in_range(small_range: pygsheets.GridRange, big_range: pygsheets.DataRange):

    row_start_index_b = big_range.start_addr[0]
    row_end_index_b = big_range.end_addr[0]
    col_start_index_b = big_range.start_addr[1]
    col_end_index_b = big_range.end_addr[1]

    row_start_index_s = small_range.start[0]
    col_start_index_s = small_range.start[1]

    if row_start_index_b <= row_start_index_s < row_end_index_b and col_start_index_b <= col_start_index_s < \
            col_end_index_b:
        return True

    return False


def schedules_to_text(schedules):

    # text = ''
    for s in schedules:
        text = s['time_start'] + ' - ' + s['time_end'] + ' | ' + s['description'] + ' ( #' + ' #'.join(s['devices']) + ')'
        print(text)


def main():
    date_time_str = '2/10/2021 01:55:19'
    # dt = datetime.datetime.now(pytz.timezone('Europe/Minsk'))
    dt = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')
    schedules = get_schedule(dt)

    schedules_to_text(schedules)


if __name__ == "__main__":
    main()
