import dns.resolver
import mailsGoogleSearchEngine
from datetime import datetime


def return_mxs(domain):
    mx_servers = []
    for x in dns.resolver.resolve(domain, 'MX'):
        # print(x.to_text())
        try:
            mx_servers.append(x.to_text().split(" "))
        except:
            mx_servers.append(['-1', 'Error, MX not found'])
    return mx_servers


def return_file_rows(f):
    count_lines = 0
    for count_lines, line in enumerate(f):
       pass
    return count_lines + 1


file = open("demofile2.txt", "r")


now = datetime.now()
file_name_string = now.strftime("%d-%m-%Y-%H-%M-%S") + '.txt'
output_file = open(file_name_string, "a")

lines = file.readlines()
no_rows = len(lines)
current_row = 1

output_file.write('==========================================\n')
print('==========================================')
for row in lines:
    print("BEGIN")
    output_str = ""
    output_file.write(row)
    print("%s%s%s %s" % (str(current_row), "/", str(no_rows), str(row)))

    try:
        output_str = str(return_mxs(row.strip()))
        output_file.write(output_str)
        print(output_str)
    except:
        output_file.write(str(['-1', 'Error, MX not found']))
        print(str(['-1', 'Error, MX not found']))

    output_str = str(mailsGoogleSearchEngine.emails_by_domain(row))
    output_file.write(output_str)
    print(output_str)
    output_file.write('==========================================\n')
    print('==========================================')
    current_row += 1

output_file.close()
