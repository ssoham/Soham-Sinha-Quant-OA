from email_checker import EmailChecker
import click

@click.command()
@click.option('--template-file', default='email_template.txt', help='The template file to be edited.')
@click.option('--csv-file', default='sample_data.csv', help='The CSV file to be edited.')
@click.option('--output-file', default='emails.json', help='The output file to be created.')
def main(template_file, csv_file, output_file):
    checker = EmailChecker(template_file, csv_file, output_file)
    checker.pattern_input()

    if checker.response == "r":
        checker.checking_patterns()
        checker.email_cleaner()
        checker.write_email()
    if checker.response == "e":
        # accounts for every single possible combination of typos and header column
        labels = []
        for i in range(len(checker.header)):
            for j in range(len(checker.opening)):
                for k in range(len(checker.ending)):
                    labels.append(checker.opening[j] + checker.lowered_header[i] + checker.ending[k])
        checker.write_email(labels)

if __name__ == "__main__":
    main()
