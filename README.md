# MorePro
Save [MorePro V19 Smartwatch](https://www.more-pro.com/products/v19-ecg-monitor-fitness-tracker) data as Excel sheet via phone logs.

The MorePro app sucks because it only lets you export info as a screenshot.
It would be much more useful to be able to save and keep the actual data.
With that, you can have fun and process the data however you want.

## Instructions
First, copy log files from your MorePro app on your phone over to the computer.
On Android, I found these in:
"...\Internal storage\Android\data\com.chenyu.morepro\cache\WoFit\File\"
They're titled: "YYYY-MM-DDappLog.txt" and only a couple days' worth of data 
is kept at a time, so be sure to back up onto the computer regularly.

Once you have the logs, run
```
$ python
>> from logxtractor import *
>> run_all("path/to/logs/", "output_filename.xlsx")
```
to create a single Excel sheet with all recovered data.


![example output](https://raw.githubusercontent.com/minterm/MorePro/main/example%20output.png)
