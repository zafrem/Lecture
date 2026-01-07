#



def get_file_data():
    lst = []
    with open('_0_example_info.txt', "r", encoding="utf-8") as read_file:
        while True:
            for lines in read_file.readlines():
                if not lines: break
                row = lines.rstrip("\n").split("|")
                # print(f"Date : {row[0]}, Price : {row[1]}, Percentage : {row[2]}")
                lst.append(row)
            read_file.close()
            break
        read_file.close()
    return lst


if __name__ == "__main__":
    print(get_file_data())