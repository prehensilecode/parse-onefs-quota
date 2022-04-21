# parse-onefs-quota
Read Isilon OneFS XML quota reports.

File names are like:
- `scheduled_quota_summary_1650511800.xml`
- `scheduled_quota_report_1650511800.xml`

The timestamp in the name (1650511800 above) is in local timezone.

```
>>> import datetime
>>> datetime.datetime.fromtimestamp(1650511800).isoformat()
'2022-04-20T23:30:00'
```
