import csv

def run():
    filename = "normalized_data.csv"
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        # is_first_row = True
        for row in datareader:
            # if is_first_row:
            #     is_first_row = False
            #     for i in range(13, 22):
            #         new_file = 'normalized_data_20' + str(i) + '.csv'
            #         nf = open(new_file, 'w')
            #         writer = csv.writer(nf)
            #         writer.writerow(row)
            #         nf.close()
            #     continue

            year = row[2]
            file = 'normalized_data_' + str(year) + '.csv'
            f = open(file, 'w')
            writer = csv.writer(f)
            writer.writerow(row)
            f.close()

if __name__ == "__main__":
    run()
