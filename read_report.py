#!/usr/bin/env python3
import sys
import os
import glob
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import grp
import datetime
import pytz
import delorean


debug_p = True

def debug_print_maybe(fstr):
    global debug_p

    if debug_p:
        print(eval(f'f"DEBUG: {fstr}"'))


def get_list_of_reports(reports_dir):
    global debug_p

    reports = glob.glob(reports_dir + '/scheduled_quota_report_*.xml')
    times = [delorean.epoch(int(r.split('.xml')[0].split('_')[-1])).shift('US/Eastern') for r in reports]

    retval = list(zip(times, reports))
    retval.sort(key=lambda k: k[0])

    return retval


def print_usage_maybe(usage: ET.Element):
    global debug_p

    usage_type = usage.attrib['resource']

    KIBI = 1024
    MEBI = KIBI * KIBI
    GIBI = MEBI * KIBI
    TEBI = GIBI * KIBI

    du = int(usage.text)
    if du < KIBI:
        print(f"  {usage_type} usage = {du} Bytes")
    elif du < MEBI:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/KIBI:.4f} kiB")
    elif du < GIBI:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/MEBI:.4f} MiB")
    elif du < TEBI:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/GIBI:.4f} GiB")
    else:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/TEBI:.4f} TiB")


def show_usage(report_fn: str):
    global debug_p

    tree = ET.parse(report_fn)
    root = tree.getroot()

    print("Report time:",
          f"{delorean.epoch(int(root.attrib['time'])).shift('US/Eastern').datetime.strftime('%Y-%m-%d %X %Z')}")

    MINGID = 10000
    for domain in root.iter('domain'):
        if domain.attrib['type'] == 'group':
            gid = int(domain.attrib['id'])
            # research groups have GIDs starting at 10001
            if gid > MINGID:
                try:
                    gr_name = grp.getgrgid(gid).gr_name
                except KeyError as e:
                    print(f'ERROR: {e}')
                    gr_name = f'unknown-{str(gid)}'

                print(f"group={gr_name} ({gid})")
                for usage in domain.findall('usage'):
                    # NOTE: du(1) reports physical storage
                    if usage.attrib['resource'] in ('physical', 'logical'):
                        print_usage_maybe(usage)


def main():
    global debug_p

    reports = get_list_of_reports('./fake_reports')
    if debug_p:
        print(f'DEBUG: list of reports:')
        for r in reports:
            print('\t', r)

    date_of_interest = datetime.date(2022, 4, 9)
    print(f'Picking one report only, on {date_of_interest}')

    report_of_interest = [r[1] for r in reports if r[0].date == date_of_interest][0]
    debug_print_maybe(f'DEBUG: report_of_interest = {report_of_interest}')
    show_usage(report_of_interest)

    print('')
    print('========================================')
    print('')

    print(f'Printing all reports:')
    for r in reports:
        debug_print_maybe(f'r[0].date = {r[0].date}; report = {r[1]}')
        debug_print_maybe(f'date_of_interest == r[0].date - {date_of_interest == r[0].date}')

        show_usage(r[1])
        print('- - -')


if __name__ == '__main__':
    main()
