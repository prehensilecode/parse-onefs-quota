#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
import grp
import delorean


def print_usage_maybe(usage: ET.Element):

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


def main():
    REPORT_FN = "adhoc_quota_report_1649442443.xml"

    tree = ET.parse(REPORT_FN)
    root = tree.getroot()

    print("Report time:",
          f"{delorean.epoch(int(root.attrib['time'])).shift('US/Eastern').datetime.strftime('%Y-%m-%d %X %Z')}")

    MINGID = 10000
    for domain in root.iter('domain'):
        if domain.attrib['type'] == 'group':
            gid = int(domain.attrib['id'])
            # research groups have GIDs starting at 10001
            if gid > MINGID:
                gr_name = grp.getgrgid(gid).gr_name
                print(f"group={gr_name} ({gid})")
                for usage in domain.findall('usage'):
                    # NOTE: du(1) reports physical storage
                    if usage.attrib['resource'] in ('physical', 'logical'):
                        print_usage_maybe(usage)


if __name__ == '__main__':
    main()
