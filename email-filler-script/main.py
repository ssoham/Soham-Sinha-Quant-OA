from tabnanny import check
import regex as re
import json
from email_checker import EmailChecker
import click

@click.command()
@click.option('--template-file', default='email_template.txt', help='The template file to be edited.')
@click.option('--csv-file', default='email_data.csv', help='The CSV file to be edited.')
@click.option('--output-file', default='emails.json', help='The output file to be created.')
# def main():
def main(template_file, csv_file, output_file):
    # checker = EmailChecker('email_template.txt', 'sample_data.csv', 'emails.json')
    checker = EmailChecker(template_file, csv_file, output_file)
    checker.pattern_input()
    while len(checker.m) < 1:
        print("No matches for this pattern were found in the template.")
        user = input("Would you like to retry a pattern (y/n)")
        if user == "y":
            filter = checker.pattern_input()
        else:
            print("Exiting.")
            exit()

    checker.checking_patterns()
    checker.email_cleaner()
    checker.write_email()

if __name__ == "__main__":
    main()
