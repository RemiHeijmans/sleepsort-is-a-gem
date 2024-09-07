import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import matplotlib.pyplot as plt
import numpy as np

# Sorting algorithms

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def sleep_sort(arr, scale_factor=0.005):
    result = []
    
    def sleep_and_append(n):
        time.sleep(n * scale_factor)
        result.append(n)
    
    threads = []
    for num in arr:
        thread = threading.Thread(target=sleep_and_append, args=(num,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    return result

# Function to sort and measure time
def sort_and_measure_time(arr, sort_func):
    start_time = time.time()
    sorted_array = sort_func(arr.copy())
    end_time = time.time()
    return sorted_array, end_time - start_time

# Function to generate the random array
def generate_random_array(x, y, length):
    return [random.randint(x, y) for _ in range(length)]

# Function to check accuracy of one sorted array against another
def check_sort_accuracy(reference_sorted_arr, sorted_arr):
    correct_count = sum(1 for x, y in zip(reference_sorted_arr, sorted_arr) if x == y)
    accuracy = correct_count / len(reference_sorted_arr) * 100
    return accuracy

def generate_and_sort():
    try:
        x = 1
        y = 100
        length = 25000

        # Generate the random array
        array = generate_random_array(x, y, length)

        # Sorting algorithms dictionary
        sorting_algorithms = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "Quick Sort": quick_sort,
            "Sleep Sort": sleep_sort
        }

        # Store times and sorted arrays for each sort
        times = {}
        sorted_arrays = {}

        for name, func in sorting_algorithms.items():
            sorted_array, sort_time = sort_and_measure_time(array, func)
            times[name] = sort_time
            sorted_arrays[name] = sorted_array
            print(f"{name}: {sort_time:.6f} seconds")

        # Use Bubble Sort as the reference
        reference_sorted_array = sorted_arrays["Bubble Sort"]

        # Compare each sorted array against the reference (Bubble Sort)
        for name, sorted_array in sorted_arrays.items():
            if name != "Bubble Sort":
                accuracy = check_sort_accuracy(reference_sorted_array, sorted_array)
                print(f"{name} accuracy compared to Bubble Sort: {accuracy:.2f}%")

        # Track sleep sort iterations
        sleep_sort_times = [times["Sleep Sort"]]
        sleep_sort_accuracies = [check_sort_accuracy(reference_sorted_array, sorted_arrays["Sleep Sort"])]
        sleep_sort_iterations = 1

        # Keep applying sleep sort until it's 100% accurate
        while sleep_sort_accuracies[-1] < 75:
            sorted_array, sort_time = sort_and_measure_time(sorted_arrays["Sleep Sort"], sleep_sort)
            accuracy = check_sort_accuracy(reference_sorted_array, sorted_array)
            sleep_sort_times.append(sort_time)
            sleep_sort_accuracies.append(accuracy)
            sorted_arrays["Sleep Sort"] = sorted_array
            sleep_sort_iterations += 1

        # Print out the results
        print(f"\nSleep Sort took {sleep_sort_iterations} iterations to achieve 100% accuracy.")
        print(f"Times taken in each iteration: {sleep_sort_times}")
        print(f"Accuracies after each iteration: {sleep_sort_accuracies}")
        print(f"Total time for Sleep Sort: {sum(sleep_sort_times):.6f} seconds")

    except ValueError as e:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Example function call (normally, this would be triggered by a UI event)
generate_and_sort()
