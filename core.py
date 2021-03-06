# define imports
import re
from ipwhois import IPWhois

while True:
    # create intro banner
    def start():
        print("------------")
        print("- Enter IP -")
        print("------------")

    # activate the function start
    start()

    # capture user input and store as variable user_in
    user_in = input(">> ")

    # create function to check if real ip address
    def is_valid_ipv4():
        """Validates IPv4 addresses.
        """
        pattern = re.compile(r"""
            ^
            (?:
              # Dotted variants:
              (?:
                # Decimal 1-255 (no leading 0's)
                [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
              |
                0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
              |
                0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
              )
              (?:                  # Repeat 0-3 times, separated by a dot
                \.
                (?:
                  [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
                |
                  0x0*[0-9a-f]{1,2}
                |
                  0+[1-3]?[0-7]{0,2}
                )
              ){0,3}
            |
              0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
            |
              0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
            |
              # Decimal notation, 1-4294967295:
              429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
              42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
              4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
            )
            $
        """, re.VERBOSE | re.IGNORECASE)
        return pattern.match(user_in) is not None

    # perform checks to make sure that correct ip address is filled in
    if user_in != "":
        if is_valid_ipv4():
            obj = IPWhois(user_in)
            result = obj.lookup_whois()
            print("-------- Raw Output --------")
            print("      "+user_in+"          ")
            print(result)
            result_list = list(result.values())
            result_string = ''.join(str(result_list)).lower()
            name_result = result.get("asn_description")
            created_result = result.get("asn_date")
            print(">> COMPANY: " + name_result)
            print(">> ASSIGNED DATE: " + str(created_result))
            if "yahoo" in result_string:
                print(">> Valid Yahoo Address!")
            else:
                print(">> Email may not have originated from Yahoo!")
            break
        else:
            print("[Error] - Please enter a valid IP Address!")
            continue
    else:
        print("[Error] - Please enter an IP Address!")
        continue
