from tabnanny import check
import regex as re
import json
from email_checker import EmailChecker
import click


if __name__ == "__main__":
    checker = EmailChecker()
    filter = checker.pattern_input()

    while len(checker.check_regex_pattern(filter)) < 1:
        print("No matches for this pattern were found in the template.")
        user = input("Would you like to retry a pattern (y/n)")
        if user == "y":
            filter = checker.pattern_input()
        else:
            print("Exiting.")
            exit()

    m = checker.check_regex_pattern(filter)
    op, ed = checker.extract_op_ed(m)
    
    if len(op) != 1 or len(ed) != 1:
        print("Multiple patterns were detected.")
        print("The initial pattern passed was:", filter)
        if len(op) != 1:
            for opening in list(op):
                is_replaced = input("Should {} be considered correct? (y/n)".format(opening))
                if is_replaced == "n":
                    op.remove(opening)
                    for match in m:
                        if opening in match:
                            m.remove(match)
        if len(ed) != 1:
            for ending in list(ed):
                is_replaced = input("Should {} be considered correct? (y/n)".format(ending))
                if is_replaced == "n":
                    ed.remove(ending)
                    for match in m:
                        if ending in match:
                            m.remove(match)
        
        print(m)
    

    emails = [] 
    template_data = checker.template_data

    
    for match in m:
        label = re.search(r"[a-zA-Z\s]+", match).group(0)
        label = label.strip()

        if label not in checker.header:
            if label.lower() in checker.lowered_header:
                replace = input("Would you like to replace {} from the CSV with {} in the template? (y/n)".format(checker.header[checker.lowered_header.index(label.lower())], label))
                if replace == "y":
                    checker.header[checker.lowered_header.index(label)]= label
                if replace == "n":
                    m.remove(match)


    checker.write_email()
