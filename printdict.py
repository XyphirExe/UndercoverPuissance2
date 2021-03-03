import pickle
import sys
import run


def format_dict(dict_var):

    result = ""

    for word in dict_var.keys():

        len_word = (len(word) + 3) * " "

        result += word + " : "

        for word_in_list in dict_var[word]:

            result += word_in_list + "\n" + len_word

        result += "\n"

    return result


"""if __name__ == "_main__":"""

if not run.file_exist(sys.argv[1]):
    print("File not found")
else:
    with open("./dict/" + sys.argv[1], "rb") as f:
        dictionary = pickle.load(f)

    print(format_dict(dictionary))
    input()
