arr = [1, 3, 5, 9, 11, 0, 12, 1, 12, 21, 22, 16, 17]

def print_array(array, original_first_index):
    result = []
    for i in range(len(array)):
        if i == original_first_index:
            result.append(f"*{array[i]}")
        else:
            result.append(str(array[i]))
    print(" ".join(result))

print(f"Масив {len(arr)} елементів:")

print_array(arr, 0)

k = int(input("Ціле число k: "))

n = len(arr)
shift = k % n

print(f"Зсув вправо на {shift} елементи")

shifted_arr = arr[-shift:] + arr[:-shift]
print_array(shifted_arr, shift)