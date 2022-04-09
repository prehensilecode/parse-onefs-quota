#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
import grp
import delorean


def print_usage_maybe(usage: ET.Element):

    usage_type = usage.attrib['resource']

    KILO = 1024
    MEGA = KILO * KILO
    GIGA = MEGA * KILO
    TERA = GIGA * KILO

    du = int(usage.text)
    if du < KILO:
        print(f"  {usage_type} usage = {du} Bytes")
    elif du < MEGA:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/KILO:.4f} kiB")
    elif du < GIGA:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/MEGA:.4f} MiB")
    elif du < TERA:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/GIGA:.4f} GiB")
    else:
        print(f"  {usage_type} usage = {du} Bytes = {float(du)/TERA:.4f} TiB")


def main():
    REPORT_FN = "adhoc_quota_report_1649442443.xml"

    tree = ET.parse(REPORT_FN)
    root = tree.getroot()

    print("Report time:",
          f"{delorean.epoch(int(root.attrib['time'])).shift('US/Eastern').datetime.strftime('%Y-%m-%d %X %Z')}")

    for child in root:
        for domain in child.findall('domain'):
            if domain.attrib['type'] == 'group':
                gid = int(domain.attrib['id'])
                gr_name = grp.getgrgid(gid).gr_name
                if gid > 9999:
                    print(f"group={gr_name} ({gid})")
                    for usage in domain.findall('usage'):
                        if usage.attrib['resource'] in ('physical', 'logical'):
                            print_usage_maybe(usage)



if __name__ == '__main__':
    main()
