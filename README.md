# mealpalinator

### Overview
CLi tool to automate mealpal orders in San Francisco (e.g. using cron jobs).

### Usage:
```
python mealpalinator.py --help
usage: mealpalinator.py [-h] -u COOKIE -d DATE -s SHOP

Mealpal auto reservation like a boss.

optional arguments:
  -h, --help            show this help message and exit
  -u COOKIE, --user-cookie COOKIE
                        MOBILE APP COOKIE
  -d DATE, --date DATE  YYYYMMDD
  -s SHOP, --shop SHOP  SHOP NAME
```

### Example: Ordering Spice Kit's meal on `20180315`
```
python mealpalinator.py --user-cookie=<mealpal_cookie_from_mobile_app> --date=20180315 --shop='Spice Kit'

[*] mealpalinator v0.1a - jerold@v00d00sec.com
[+] Attempting to authenticate to Mealpal using provided cookie...
[+] Authenticated as: Jerold Hoong
[+] Getting Spice Kit's schedule ID...
[+] Spice Kit's schedule id for 20180315 is: 46270904-16e0-416d-87e0-2e6260394090
[+] Attempting to reserve some food like a boss...
[+] Done! You ordered Organic Tofu Vietnamese Bowl and the order number is: 2238.
```

### Example: Ordering a meal from `Sushi Taka` that has already been sold out
```
python mealpalinator.py --user-cookie=<mealpal_cookie_from_mobile_app> --shop='Sushi Taka' --date=20180315

[*] mealpalinator v0.1a - jerold@v00d00sec.com
[+] Attempting to authenticate to Mealpal using provided cookie...
[+] Authenticated as: Jerold Hoong
[+] Getting Sushi Taka's schedule ID...
[+] Sushi Taka's schedule id for 20180315 is: 8c9e3a1c-3493-4a5b-b8e0-35c8dfecde21
[+] Attempting to reserve some food like a boss...
[!] Problem with reservation. Server returned the following code: 400 {"error":"ERROR_RESERVATION_LIMIT"}
```