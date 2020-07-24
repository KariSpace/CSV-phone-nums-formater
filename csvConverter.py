import csv
import re
from logging import log

csv_file = 'YOUR_FILE.csv'  # your file
problem_file = 'problem_file.csv'
ok_file = "ok_file.csv"
no_copy_problem_file = 'no-copy-problem_file.csv'
no_copy_ok_file = "no-copy-ok-file.csv"


def csv_writer(line_to_write, file_to_write):
    try:
        with open(file_to_write, 'a', newline='') as file_to_write:
            writer = csv.writer(file_to_write,  delimiter=';')
            writer.writerow(line_to_write)
    except Exception as e:
            log.error('Error: %s') % e.message


def dell_duplicates(before_file, after_file, field_names_list):
    print("\nstarted to drop duplicates...")
    with open(before_file, 'r', newline='') as inputfile:
        with open(after_file, 'w', newline='') as outputfile:

            duplicatereader = csv.DictReader(inputfile, delimiter=';')
            uniquewrite = csv.DictWriter(outputfile,
                                        fieldnames=field_names_list,
                                        delimiter=';')

            uniquewrite.writeheader()
            keysread = []

            for row in duplicatereader:
                key = (row[field_names_list[0]], row[field_names_list[1]])

                if key not in keysread:
                        keysread.append(key)
                        uniquewrite.writerow(row)


def phoneTransformer(phone):
    phone = re.sub(r'\D', "", phone)
    if len(phone) >= 9 and phone.isdigit():
        ok_phone = '380' + phone[-9:]  # adding country code
        return ok_phone
    else:
        raise ValueError('Can\'t format phone')


def main():
    with open(csv_file, 'r') as csv_f:
        reader = csv.reader(csv_f)

        i = 0
        a = 0
        c = 0

        field_names_list = next(reader)
        print("it`s gonna take a few seconds...")
        csv_writer(field_names_list, ok_file)
        csv_writer(field_names_list, problem_file)

        for row in reader:
            i += 1
            id_num = row[0]
            try:
                ok_num = phoneTransformer(row[1])
                a += 1
                ok_line = [id_num, ok_num]
                csv_writer(ok_line, ok_file)
            except ValueError:
                problem_num = row[1]
                c += 1
                problem_line = [id_num, problem_num]
                csv_writer(problem_line, problem_file)

        print("\nall : " + str(i))
        print("ok phone num : " + str(a))
        print("wrong phone num : " + str(c))

        dell_duplicates(ok_file, no_copy_ok_file, field_names_list)
        dell_duplicates(problem_file, no_copy_problem_file, field_names_list)


if __name__ == '__main__':
     main()
