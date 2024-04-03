from Algorithm_Visualizer.sort.sort import *
from themes.colors import *
MIN_MERGE = 32

def calculate_min_run(n): 
    """Returns the minimum length of a 
    run from 23 - 64 so that 
    the len(array)/minrun is less than or 
    equal to a power of 2.  
    """
    r = 0
    while n >= MIN_MERGE: 
        r |= n & 1
        n >>= 1
    return n + r 

def bubble_sort(draw_info,arr,low,high,ascending=True):
    for i in range(high):
        for j in range(high-i-1):
            if (arr[j]>arr[j+1] and ascending) or (arr[j]<arr[j+1] and not ascending):
                arr[j],arr[j+1] = arr[j+1],arr[j]
                draw_list(draw_info,{j:GREEN,j+1:RED},clear_bg=True)
                yield True
    return arr
        
def selection_sort(draw_info, arr, low, high, ascending=True):
    for i in range(low, high):
        min_idx = i
        for j in range(i + 1, high):
            if (arr[j] < arr[min_idx] and ascending) or (arr[j] > arr[min_idx] and not ascending) :
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_list(draw_info, {i: 'green', min_idx: 'red'}, clear_bg=True)
        yield True
    return arr


def insertion_sort(draw_info,arr,low,high,ascending=True):
    for i in range(low, high):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            draw_list(draw_info, {j: 'green', j + 1: 'red'}, clear_bg=True)
            yield True
        arr[j + 1] = key
        draw_list(draw_info, {j + 1: 'blue'}, clear_bg=True)
        yield True
    return arr

def merge(draw_info, arr, left_half, right_half,ascending=True):
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[i + j] = left_half[i]
            i += 1
        else:
            arr[i + j] = right_half[j]
            j += 1
        draw_list(draw_info, {i + j: 'green'}, clear_bg=True)
        yield True

    while i < len(left_half):
        arr[i + j] = left_half[i]
        i += 1
        draw_list(draw_info, {i + j: 'green'}, clear_bg=True)
        yield True

    while j < len(right_half):
        arr[i + j] = right_half[j]
        j += 1
        draw_list(draw_info, {i + j: 'green'}, clear_bg=True)
        yield True

    
def merge_sort(draw_info, arr, low, high,ascending=True):
    if low < high:
        mid_point = (low + high) // 2
        yield from merge_sort(draw_info, arr, low, mid_point)
        yield from merge_sort(draw_info, arr, mid_point + 1, high)
        left_half = arr[low:mid_point + 1]
        right_half = arr[mid_point + 1:high + 1]
        yield from merge(draw_info, arr[low:high + 1], left_half, right_half)
    return arr

    
def partition(draw_info, arr, low, high):
    pivot = arr[high]
    smallest_idx = low - 1
    for i in range(low, high):
        if arr[i] < pivot:
            smallest_idx += 1
            arr[i], arr[smallest_idx] = arr[smallest_idx], arr[i]
            draw_list(draw_info, {i: 'green', smallest_idx: 'red'}, clear_bg=True)
            yield True
    arr[smallest_idx + 1], arr[high] = arr[high], arr[smallest_idx + 1]
    pivot_idx = smallest_idx + 1
    draw_list(draw_info, {pivot_idx: 'blue'}, clear_bg=True)
    yield pivot_idx


def quick_sort(draw_info, arr, low, high,ascending=True):
    if low < high:
        pivot_idx = yield from partition(draw_info, arr, low, high-1)
        yield from quick_sort(draw_info, arr, low, pivot_idx - 1)
        yield from quick_sort(draw_info, arr, pivot_idx + 1, high)
    return arr

def counting_sort(draw_info,arr, low, high, ascending=True, place=None):
    temp_arr = [0] * high
    freq_arr = [0] * high
    
    if place is None:    
        for i in range(high):
            freq_arr[arr[i]] += 1
    else:
        for i in range(high):
            index = arr[i] // place
            freq_arr[index % 10] += 1
            
    for i in range(1, len(freq_arr)):
        freq_arr[i] += freq_arr[i - 1]
    
    i = high - 1
    
    if place is None:
        while i >= low:
            temp_arr[freq_arr[arr[i]] - 1] = arr[i]
            freq_arr[arr[i]] -= 1
            i -= 1    
            yield True
    else:
        while i >= low:
            index = arr[i] // place
            temp_arr[freq_arr[index % 10] - 1] = arr[i]
            freq_arr[index % 10] -= 1
            i -= 1
            yield True
        
    for i in range(high):
        arr[i] = temp_arr[i]
        yield True
    
    draw_list(draw_info, {})  # Draw the final sorted list
    return arr
        
def radix_sort(draw_info,arr, low, high, ascending=True):
    max_ele = max(arr)
    place = 1
    while max_ele // place > 0:
        yield from counting_sort(draw_info,arr, low, high, place=place)
        place *= 10
    
def bucket_sort(draw_info,arr, low, high, ascending=True):
    buckets = [[] for _ in range(high)]

    for ele in arr:
        ele_idx = int(ele * 10)
        buckets[ele_idx].append(ele)
        yield True  # Yield after each element is placed in its bucket

    for bucket in buckets:
        bucket.sort()
        yield True  # Yield after each bucket is sorted

    final_arr = []
    for bucket in buckets:
        final_arr.extend(bucket)
        yield True  # Yield after extending the final array with each bucket's content

    draw_info.lst = final_arr  # Update the list in draw_info with the final sorted array
    yield True  # Yield after the final array is assigned back to draw_info


def tim_sort(draw_info,arr, low, high, ascending=True):
    min_run = calculate_min_run(high)
    for i in range(low, high, min_run):
        end = min((i + min_run - 1), high - 1)
        yield from insertion_sort(arr, i, end)

    size = min_run

    while size < high:
        for left in range(low, high, 2 * size):
            mid = min((left + size - 1), (high - 1))
            right = min((left + 2 * size - 1), (high - 1))
            if mid < right:
                yield from merge(arr, left, mid, right)
        size = 2 * size
