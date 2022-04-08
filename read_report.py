#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
import xmltodict, json
import grp

REPORT_FN = "adhoc_quota_report_1649442443.xml"

tree = ET.parse(REPORT_FN)
root = tree.getroot()

print(root)
print(tree)

GIGA = 1024*1024*1024
TERA = 1024 * GIGA


for child in root:
    for domain in child.findall('domain'):
        if domain.attrib['type'] == 'group':
            gid = int(domain.attrib['id'])
            gr_name = grp.getgrgid(gid).gr_name
            if gid > 9999:
                print(f"group={gr_name} ({gid})")
                for usage in domain.findall('usage'):
                    if usage.attrib['resource'] == 'physical':
                        print(f"  physical usage = {int(usage.text)} Bytes = {float(usage.text)/TERA:.4e} TiB")
                    if usage.attrib['resource'] == 'logical':
                        print(f"  logical usage = {int(usage.text)} Bytes = {float(usage.text)/TERA:.4e} TiB")

