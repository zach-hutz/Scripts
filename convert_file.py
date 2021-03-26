import re
def replace(file):
    # Read contents from file as a single string
    file_handle = open(file, 'r', encoding="utf8")
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    #file_string = (re.sub(pattern, subst, file_string))
    file_string2 = file_string.replace("\n\n", "\n====================\n")

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w', encoding="utf8")
    file_handle.write(file_string2)
    file_handle.close()

replace("ShitGirlsSay_tweets.csv")
