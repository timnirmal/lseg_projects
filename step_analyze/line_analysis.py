from step_analyze.dataset import int_list

from collections import Counter

def get_flat_list():
    # Flatten the list of lists
    flat_list = [num for sublist in int_list for num in sublist]
    return flat_list

def not_used():
    flat_list = get_flat_list()

    count = 0
    missing_list = []

    # the numbers are from 1 - 172. But some are missing find them
    for i in range(1, 173):
        if i not in flat_list:
            missing_list.append(i)
            count += 1

    print(f"Missing numbers: {missing_list}")
    print(f"Total missing numbers: {count}")

    return missing_list


def frequency_analysis():
    flat_list = get_flat_list()

    # Count the frequency of each number
    frequency = Counter(flat_list)

    freq_dict = {}

    # Display the frequency of each number
    for number, count in frequency.items():
        # print(f"Number {number} appears {count} times")
        # freq_dict[number] = count
        pass

    # Optional: To display in sorted order by number
    for number in sorted(frequency):
        # print(f"Number {number} appears {frequency[number]} times")
        # add to dictionary
        freq_dict[number] = frequency[number]


    return freq_dict


not_used()

freq_dict = frequency_analysis()
print(freq_dict)
