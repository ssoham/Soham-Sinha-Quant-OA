import csv
import regex as re
from typing import Tuple
from itertools import product
import json

class EmailChecker:

    def __init__(self, template_file, csv_file, output_file) -> None:
        self.template_data = template_file
        self.csv_file = csv_file
        self.output_file = output_file
        print("hi")

        with open(csv_file, "r", encoding="utf-8") as csvfile:
            self.csvreader = csv.reader(csvfile)
            self.rows = list(self.csvreader)
        self.header = self.rows[0]
        self.lowered_header = list(map(lambda x: x.lower(), self.header))
        self.rows.pop(0)

        with open(template_file, "r") as f:
            self.template_data = f.read()


    """
    Giving the user the option for what they want to enter.
    """
    def pattern_input(self) -> None:
        user = input("Would you like to pass a RegEx filter or an example (r/e)")
        if user == "r":
            self.response = "r"
            self.get_regex_matches()
        elif user == "e":
            self.response = "e"
            self.user_example_pattern()
        else:
            print("Invalid input. Exiting.")
            exit()
        pass
    

    """
    Asks the user for a regex pattern and locates all the matches within the file.
    """
    def get_regex_matches(self) -> None:
        """
        The default regex pattern is decided b the given template and the fact that the pattern is very distinct,
        it cannot be mistaken for a regular word. Furthermore, the default RegEx pattern is robust enough to handle typos,
        such as _ _[x]_ _.
        """
        filter = input(
            "Default filter is for: __[x]__ (including checks for accidental spaces). If you want to change it, enter a new filter."
        )
        filter = "(\_+\s*\_*\[*.*?\]*\_+\s*\_*)" if filter == "" else filter
        filter = re.compile(filter)
        self.m = re.findall(re.compile(filter), self.template_data)
        
        while len(self.m) < 1:
            print("No matches for this pattern were found in the template.")
            user = input("Would you like to retry a pattern (y/n)")
            if user == "y":
                filter = self.pattern_input()
            else:
                print("Exiting.")
                exit()

    """
    Asks the user for an example pattern to later extract the opening and ending patterns.
    """
    def user_example_pattern(self) -> None:
        string = input("Entter your opening and ending brackets aroudn a letter: ")
        self.opening = re.search(r".+?(?=[a-zA-Z]\s*)", string).group()
        # gets list of typos
        # - https://stackoverflow.com/a/16479607
        self.opening = [''.join(reversed(x)).rstrip()
                        for x in product(*[(c, c+' ') for c in reversed(self.opening)])]
        self.ending = re.search(r".+?(?=[a-zA-Z]\s*)", string[::-1]).group()[::-1]
        self.ending = [''.join(reversed(x)).rstrip()
                         for x in product(*[(c, c+' ') for c in reversed(self.ending)])]
        pass

    """
    Adds all the matches to a set. Will be used to check if all the matches should be used.

    @param m: the matches to be analyzed
    """
    def extract_op_ed(self, m) -> Tuple[set, set]:
        """
        This function will extract the operator and editor from the regex pattern.
        """
        op, ed = set(), set()
        for i in range(len(m)):
            op.add(re.search(r".+?(?=[a-zA-Z]\s*)", m[i]).group())
            ed.add(re.search(r".+?(?=[a-zA-Z]\s*)", m[i][::-1]).group()[::-1])
        return op, ed
    
    """
    Gets of the email from the given template.

    @return the subject of the email
    """
    def retrieve_subject(self) -> str:
        """
        This function will retrieve the subject line from the email template.
        """
        return self.template_data.split("Subject: ")[1].split("\n")[0]
    
    """
    Gets body of the email from the given template.

    @param email: the email to be written
    
    @return the email body
    """
    def retrieve_body(self, email) -> str:
        body_index = email.index("Dear")
        return email[body_index:]

    """
    Writes the list of emails to the indicated JSON file.
    """
    def write_json(self, emails) -> None:
        f = open(self.output_file, "w")
        json.dump(emails, f)
        pass

    """
    Updates the specific JSON object based on the user's information.
    
    @param email: the JSON object to be updated
    @param written_email: the edited email
    @param user: the user's index in the csv file

    @return the updated JSON upject
    """
    def json_attributes(self, email, written_email, user) -> dict:
        email["body"] = self.retrieve_body(written_email)
        email["subject"] = self.retrieve_subject()
        email["to"] = self.rows[user][self.header.index("to")]
        email["cc"] = self.rows[user][self.header.index("cc")]
        email["bcc"] = self.rows[user][self.lowered_header.index("bcc")]

        return email

    """
    Updates the email based on the user's information. If scertain matches/columns were not used, the user is alerted.
    """
    def write_email(self) -> None:
        emails = []
        for i in range(len(self.rows)):
            col_used = [False]*len(self.header)
            matches_not_used = []
            email = {}
            substituted_email = self.template_data
            for match in self.m:
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
            
            email = self.json_attributes(email, substituted_email, i)
            emails.append(email)
        self.write_json(emails)

    """
    Writes an email based on a given set of labels (used when the user gives an example)

    @param labels: the possible labels to be used

    @return the email
    """
    def write_email(self, labels) -> None:
        emails = []
        for i in range(len(self.rows)):
            col_used = [False]*len(self.header)
            email = {}
            substituted_email = self.template_data
            for label in labels:
                header_label = re.search(r"[a-zA-Z\s]+", label).group(0)
                if header_label == ' ':
                    continue
                if label not in substituted_email:
                    col_used[self.lowered_header.index(header_label)] = True
                else:
                    substituted_email = substituted_email.replace(label, self.rows[i][self.lowered_header.index(header_label)])
            if False in col_used:
                print("The following data columns were not used for User {}:".format(self.rows[i][0]))
                unused_columns = []
                for i in range(len(col_used)):
                    if col_used[i] == False:
                        unused_columns.append(self.header[i])
                        # print(checker.header[i]
                print(unused_columns)
            email = self.json_attributes(email, substituted_email, i)
            emails.append(email)
        self.write_json(emails)

    """
    If multiple distinct patterns are found, the user is asked to confirm each, whether they should be marked correct or not.
    """
    def checking_patterns(self) -> None:
        op, ed = self.extract_op_ed(self.m)
        
        if len(op) != 1 or len(ed) != 1:
            print("Multiple patterns were detected.")
            print("The initial pattern passed was:", filter)
            if len(op) != 1:
                for opening in list(op):
                    is_replaced = input("Should {} be considered correct? (y/n)".format(opening))
                    if is_replaced == "n":
                        op.remove(opening)
                        for match in self.m:
                            if opening in match:
                                self.m.remove(match)
            if len(ed) != 1:
                for ending in list(ed):
                    is_replaced = input("Should {} be considered correct? (y/n)".format(ending))
                    if is_replaced == "n":
                        ed.remove(ending)
                        for match in self.m:
                            if ending in match:
                                self.m.remove(match)
    

    """
    Updates the CSV in the case of no matching headers and regex matches.
    """
    def email_cleaner(self) -> None:
        for match in self.m:
            label = re.search(r"[a-zA-Z\s]+", match).group(0)
            label = label.strip()

            if label not in self.header:
                if label.lower() in self.lowered_header:
                    replace = input("Would you like to replace {} from the CSV with {} in the template? (y/n)".format(self.header[self.lowered_header.index(label.lower())], label))
                    if replace == "y":
                        self.header[self.lowered_header.index(label)]= label
                    if replace == "n":
                        self.m.remove(match)