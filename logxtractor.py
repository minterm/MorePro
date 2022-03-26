# logxtractor.py: extract user data from MorePro logs

import os
import pandas as pd

################################################################################
def extract_dfs_from_log(logpath, ss='"userData":', ss2="FitupHttpUtil"):
    ''' Pull out relevant info from an appLog file.
    Parameters
    ----------
    logpath : string
        Path to the log file.
    ss : string
        The string highlighting where the data starts in a line.
    ss2 : string
        A secondary string just to ensure it's what I think it is.
    Returns
    -------
    userData : dict
        Dictionary of Pandas data frames
    '''
    with open(logpath, 'r', encoding='utf-8', errors='ignore') as f:
        appLog = f.readlines()
    userData = {}
    for line, i in zip(appLog, range(len(appLog))):
        if ss in line and ss2 in line:
            start = line.find(ss) + len(ss)
            if line[start] != '[':
                raise NotImplementedError
            s = start + 1
            c = 0
            while s < len(line):
                if line[s] == '[':
                    c += 1
                elif line[s] == ']':
                    if c == 0:
                        break
                    c -= 1
                s += 1
            try:
                frame = pd.read_json(line[start:s+1])
            except ValueError as e:
                print("\tUnfinished line in the log.")
                print(e)
                print(logpath)
                print(i, start, s+1)
                print("\tAttempting to partially salvage.")
                while s > start:
                    s -= 1
                    if line[s] == '}':
                        break
                frame = pd.read_json(line[start:s+1]+']')
            try:
                if frame['dataType'].nunique() == 1:
                    sheetname = frame['dataType'][0]
                else:
                    raise NotImplementedError
            except KeyError as e:
                print(e)
                print("Skipping this line because no dataType")
                #TODO figure out if this happens for some other format that 
                #     instead may actually be useful/interesting to use.
                continue
            if sheetname in userData.keys():
                userData[sheetname].append(frame)
            else:
                userData[sheetname] = [frame]
        else:
            continue
    for key in userData.keys():
        userData[key] = pd.concat(userData[key])
        # TODO: data mods can programmatically happen in here now!
    return userData

def send_dfs_to_db(userData, outfile='database.xlsx'):
    for key in userData.keys():
        df = userData[key]
        try:
            with pd.ExcelWriter(outfile, engine='openpyxl', mode='a') as wrt:
                df.to_excel(wrt, sheet_name=key)
        except FileNotFoundError:
            with pd.ExcelWriter(outfile, mode='w') as wrt:
                df.to_excel(wrt, sheet_name=key)
    return

def run_all(logdir='./Copied Logs/appLog/', outfile='all_test.xlsx'):
    infiles = os.listdir(logdir)
    infiles = [logdir + x for x in infiles if x.endswith(".txt")]
    allData = {}
    for infile in infiles:
        userData = extract_dfs_from_log(infile)
        for key in userData.keys():
            if key in allData.keys():
                allData[key].append(userData[key])
            else:
                allData[key] = [userData[key]]
    for key in allData.keys():
        allData[key] = pd.concat(allData[key])
    return send_dfs_to_db(allData, outfile)

################################################################################
if __name__ == "__main__":
    rtn = extract_dfs_from_log("./Copied Logs/appLog/2022-03-10appLog.txt")
    send_dfs_to_db(rtn, 'dbtest.xlsx')
