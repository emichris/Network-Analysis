#/ your Python code to implement the features could be placed here
#/ note that you may use any language, there is no preference towards Python

import re
import collections
import argparse
import pandas as pd

t = re.compile(r'(?P<ip>^.*) - - \[(?P<dt>.*) -0400\] \"\w{3,4} (?P<d>.*) HTTP/1.0\" (?P<r>\d{3}) (?P<b>.\d{0,4})')

logs = [];

f = open(r'log_input\log.txt', 'r', encoding='utf8', errors='ignore');
columns = ['ip', 'dt', 'data', 'response', 'bandwidth']
k = 0; matched = 0; failed = 0;
for line in f:
    log_dict = {}
    m = t.match(line);

    #if we don't match then next line
    if not m:
        failed += 1;
        continue

    matched += 1
    
    logs.append({'ip': m.group('ip'), 'datetime': m.group('dt'), 'resource': m.group('d'), 'response': m.group('r'), 'bandwidth': m.group('b')})
    
f.close();


## Part 2 - Exercise 1 & 2
import collections

cnt_ip = collections.Counter()
cnt_resource = collections.Counter()

for log in logs:
    cnt_ip.update([log['ip']])
    cnt_resource.update([log['resource']])

"""
print('[*] %d lines matched the regular expression' % (matched))
print('[*] %d lines failed to match the regular expression' % (failed), end='\n\n')
print('[*] ============================================')
print('[*] 10 Most Frequently Occurring Domains Queried')
print('[*] ============================================')
for host, count in cnt_ip.most_common(10):
    print('[*] %-40s:  %d' % (host, count))
print('[*] ============================================', end='\n\n')

print('[*] 10 Most Frequently Accessed Resource')
print('[*] ============================================')
for resource, count in cnt_resource.most_common(10):
    print('[*] %-40s:  %d' % (resource, count))
print('[*] ============================================')

"""

f_hosts = open(r'log_output\hosts.txt', 'w');
for host, count in cnt_ip.most_common(10):
    f_hosts.write('%s,%d\n' % (host, count))
f_hosts.close();

f_resources = open(r'log_output\resources.txt', 'w')
for domain, _ in cnt_resource.most_common(10):
    f_resources.write('%s\n' % domain)
f_resources.close();



## Part 3 - Exercises 3 & 4
# Convert data to date

df_log = pd.DataFrame(logs)
df_log['datetime'] = pd.to_datetime(df_log['datetime'], format='%d/%b/%Y:%H:%M:%S')

index = pd.DatetimeIndex(df_log['datetime'])
data = pd.Series(range(0, len(logs)), index=index)

start_t = min(df_log['datetime'])
end_t = max(df_log['datetime'])
begin_window = pd.date_range(start_t, end_t, freq='1S')

cnt_t = collections.Counter()
for w in begin_window:
    s = w.strftime('%Y-%m-%d %H:%M:%S')
    e = (w+pd.Timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
    wr = w.strftime('%d/%b/%Y:%H:%M:%S -0400')
    cnt_t[wr] = len(data[s:e])


"""
print('[*] ============================================')
print('[*] 10 Busiest 60-minutes period')
print('[*] ============================================')
for t, count in cnt_t.most_common(10):
    print('[*] %-30s:  %d' % (t, count))
print('[*] ============================================', end='\n\n')

"""
f_out = open(r"log_output\hours.txt","w")
for t, count in cnt_t.most_common(10):
    f_out.write('%s,%d\n' % (t, count))
f_out.close()

