import csv
import regex as re
from typing import Tuple

class EmailChecker:
    def __init__(self) -> None:
        with open("sample_data.csv", "r", encoding="utf-8") as csvfile:
            self.csvreader = csv.reader(csvfile)
            self.rows = list(self.csvreader)
        self.header = self.rows[0]
        self.lowered_header = list(map(lambda x: x.lower(), self.header))
        self.rows.pop(0)

        with open("email_template.txt", "r") as f:
            self.template_data = f.read()

    def pattern_input(self) -> str:
        user = input("Would you like to pass a RegEx filter or an example (r/e)")
        if user == "r":
            filter = self.user_regex_pattern()
        elif user == "e":
            filter = self.user_regex_pattern()
        else:
            print("Invalid input. Exiting.")
            exit()
        return filter
        
    def retrieve_subject(self) -> str:
        """
        This function will retrieve the subject line from the email template.
        """
        return self.template_data.split("Subject: ")[1].split("\n")[0]

    def user_regex_pattern(self) -> str:
        """
        This function will take the user input and return a regex pattern.
        """
        filter = input(
            "Default filter is for: __[x]__ (including checks for accidental spaces). If you want to change it, enter a new filter."
        )
        filter = "(\_+\s*\_*\[*.*?\]*\_+\s*\_*)" if filter == "" else filter
        return filter

    def check_regex_pattern(self, filter) -> list:
        """
        This function will check the regex pattern against the email template.
        """
        filter = re.compile(filter)
        m = re.findall(filter, self.template_data)
        return m
    
    def extract_op_ed(self, m) -> Tuple[set, set]:
        """
        This function will extract the operator and editor from the regex pattern.
        """
        op, ed = set(), set()
        for i in range(len(m)):
            op.add(re.search(r".+?(?=[a-zA-Z]\s*)", m[i]).group())
            ed.add(re.search(r".+?(?=[a-zA-Z]\s*)", m[i][::-1]).group()[::-1])
        return op, ed
    
    def retrieve_body(self, email) -> str:
        body_index = email.index("Dear")
        return email[body_index:]

    def write_json(self, email, written_email, user) -> None:
        email["body"] = self.retrieve_body(written_email)
        email["subject"] = self.retrieve_subject()
        email["to"] = self.rows[user][self.header.index("to")]
        email["cc"] = self.rows[user][self.header.index("cc")]
        email["bcc"] = self.rows[user][self.lowered_header.index("bcc")]

        f = open("email_data.json", "w")
        json.dump(email, f)
        pass

    def write_email(self) -> str:
        for i in range(len(self.rows)):
            col_used = [False]*len(self.header)
            matches_not_used = []
            email = {}
            substituted_email = self.template_data
            for match in m:
                label = re.search(r"[a-zA-Z\s]+", match).group(0)
                if label not in self.header:
                    matches_not_used.append(match)
                else:
                    index = self.header.index(label)
                    substituted_email = substituted_email.replace(match, self.rows[i][index])
                    col_used[index] = True
            if False in col_used:
                print("The following data columns were not used for User {}:".format(self.rows[i][0]))
                unused_columns = []
                for i in range(len(col_used)):
                    if col_used[i] == False:
                        unused_columns.append(self.header[i])
                        # print(checker.header[i]
                print(unused_columns)
            if len(matches_not_used) != 0:
                print("The following matches were not used for User {}:".format(self.rows[i][0]))
                print(matches_not_used)
            self.write_json(email, substituted_email, i)