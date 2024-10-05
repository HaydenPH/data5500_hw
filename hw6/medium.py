def find_second_largest(arr):
    largest = second_largest = float('-inf')
    for num in arr:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
    return second_largest


arr = [1, 2, 3, 4, 5]
second_largest_number = find_second_largest(arr)
print("Second largest number is:", second_largest_number)

# The code only passes through each number in the array once and gathers the largest and second largest number on that pass.
# So the Big O notation is O(n)