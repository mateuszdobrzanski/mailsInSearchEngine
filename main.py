import dns.resolver
import mailsGoogleSearchEngine


def return_mxs(domain):
    for x in dns.resolver.resolve(domain, 'MX'):
        print(x.to_text())


file = open("demofile.txt", "r")

print('==========================================')
for row in file:
    print(row)
    print()
    print(return_mxs(row.strip()))
    print()
    print(mailsGoogleSearchEngine.emails_by_domain(row))
    print('==========================================')
