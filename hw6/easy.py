def sum_of_array(arr):
    total_sum = 0
    for num in arr:
        total_sum += num
    return total_sum

array = [1, 2, 3, 4, 5]

print(f"Sum of array: {sum_of_array(array)}")

# It reads each number in the array one at a time and adds it. The more numbers in the array, the more time it will take
# The big O Notation is O(n)