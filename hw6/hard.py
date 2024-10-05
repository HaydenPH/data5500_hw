def find_max_difference(arr):

    min_value = max_value = arr[0]

    for num in arr:
        if num < min_value:
            min_value = num
        if num > max_value:
            max_value = num
    return max_value - min_value


arr = [1, 2, 3, 4, 5]
max_diff = find_max_difference(arr)
print("The max difference is:", max_diff)

#again the time complexity of this code is O(n) becuse it only has to cycle through the array once.