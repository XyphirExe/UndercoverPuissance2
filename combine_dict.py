import sys
import run
import pickle
import printdict

if __name__ == "__main_":

    all_dict = False

    option_no = 1
    while (len(sys.argv) - 1) >= option_no or sys.argv[option_no][0] == "-":
        if sys.argv[option_no] == ("--all" or "-A"):
            all_dict = True

    list_dict = []

    if all_dict:
        dict_no = 1
        while run.file_exist("dict" + str(dict_no)):
            list_dict.append("dict" + str(dict_no))
            dict_no += 1

    else:
        while (len(sys.argv) - 1) >= option_no:
            if run.file_exist(sys.argv[option_no]):
                list_dict.append(sys.argv[option_no])
            else:
                print(sys.argv[option_no] + " n'a pas été trouvé.")

    whole_dict = dict()
    for dictionary in list_dict:

        with open(dictionary, "rb") as f:
            whole_dict.update(pickle.load(f))

    dict_no = 1
    while run.file_exist("dict" + str(dict_no)):
        dict_no += 1

    with open("dict" + str(dict_no), 'wb') as file:
        pickle.dump(whole_dict, file)

    print("\"dict" + str(dict_no) + "\" a été créé : \n" + printdict.format_dict(whole_dict))

    input()
