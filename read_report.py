#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
import grp
import delorean

REPORT_FN = "adhoc_quota_report_1649442443.xml"

tree = ET.parse(REPORT_FN)
root = tree.getroot()

print(root)
print(f"root.attrib['time'] = {root.attrib['time']} = {delorean.epoch(int(root.attrib['time'])).shift('US/Eastern')}")

KILO = 1024
MEGA = KILO * KILO
GIGA = MEGA * KILO
TERA = GIGA * KILO


for child in root:
    for domain in child.findall('domain'):
        if domain.attrib['type'] == 'group':
            gid = int(domain.attrib['id'])
            gr_name = grp.getgrgid(gid).gr_name
            if gid > 9999:
                print(f"group={gr_name} ({gid})")
                for usage in domain.findall('usage'):
                    if usage.attrib['resource'] == 'physical':
                        du = int(usage.text)
                        if du < KILO:
                            print(f"  physical usage = {du} Bytes")
                        elif du < MEGA:
                            print(f"  physical usage = {du} Bytes = {float(du)/KILO:.4f} kiB")
                        elif du < GIGA:
                            print(f"  physical usage = {du} Bytes = {float(du)/MEGA:.4f} MiB")
                        elif du < TERA:
                            print(f"  physical usage = {du} Bytes = {float(du)/GIGA:.4f} GiB")
                        else:
                            print(f"  physical usage = {du} Bytes = {float(du)/TERA:.4f} TiB")
                    if usage.attrib['resource'] == 'logical':
                        du = int(usage.text)
                        if du < KILO:
                            print(f"  logical usage = {du} Bytes")
                        elif du < MEGA:
                            print(f"  logical usage = {du} Bytes = {float(du)/KILO:.4f} kiB")
                        elif du < GIGA:
                            print(f"  logical usage = {du} Bytes = {float(du)/MEGA:.4f} MiB")
                        elif du < TERA:
                            print(f"  logical usage = {du} Bytes = {float(du)/GIGA:.4f} GiB")
                        else:
                            print(f"  logical usage = {du} Bytes = {float(du)/TERA:.4f} TiB")

