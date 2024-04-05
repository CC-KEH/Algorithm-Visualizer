from sort import *
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
                draw_list(draw_info, {i: 'green', min_idx: 'red'}, clear_bg=True)
                yield True
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

def merge(draw_info,arr, l, m, r): 
    len1, len2 = m - l + 1, r - m
    left, right = [], [] 
    for i in range(0, len1): 
        left.append(arr[l + i])
         
    for i in range(0, len2):
        right.append(arr[m + i + 1])
    
    i, j, k = 0, 0, l 

    while i < len1 and j < len2: 
        if left[i] <= right[j]: 
            arr[k] = left[i] 
            i += 1

        else: 
            arr[k] = right[j] 
            j += 1
        draw_list(draw_info, {k: 'green'}, clear_bg=True)
        yield True
        k += 1
  
    while i < len1: 
        arr[k] = left[i] 
        k += 1
        i += 1
        draw_list(draw_info, {}, clear_bg=True)
        yield True
        
    while j < len2: 
        arr[k] = right[j] 
        k += 1
        j += 1
        draw_list(draw_info, {}, clear_bg=True)
        yield True

def merge_sort(draw_info,arr,low,high,ascending=True):
    if low < high:
        mid = (low + high) // 2
        yield from merge_sort(draw_info, arr, low, mid)
        yield from merge_sort(draw_info, arr, mid + 1, high)
        yield from merge(draw_info, arr, low, mid, high)
    return arr

def partition(draw_info, arr, low, high):
    pivot = arr[high]
    smallest_idx = low - 1
    for i in range(low, high+1):
        if arr[i] < pivot:
            smallest_idx += 1
            arr[i], arr[smallest_idx] = arr[smallest_idx], arr[i]
            draw_list(draw_info, {i: 'green', smallest_idx: 'red'}, clear_bg=True)
            yield True
    arr[smallest_idx + 1], arr[high] = arr[high], arr[smallest_idx + 1]
    pivot_idx = smallest_idx + 1
    draw_list(draw_info, {pivot_idx: 'blue'}, clear_bg=True)
    yield pivot_idx

def quick_sort(draw_info, arr, low, high, ascending=True):
    if low < high:
        pivot_gen = partition(draw_info, arr, low, high - 1)
        pivot_idx = None
        for val in pivot_gen:
            pivot_idx = val
        if pivot_idx is not None:
            yield from quick_sort(draw_info, arr, low, pivot_idx)
            yield from quick_sort(draw_info, arr, pivot_idx+1, high)
    return arr

def counting_sort(draw_info,arr, low, high, ascending=True, place=None):
    max_val = max(arr)
    freq_arr = [0] * (max_val+1)
    
    for num in arr:
        freq_arr[num] += 1

    for i in range(1, max_val + 1):
        freq_arr[i] += freq_arr[i - 1]
        
    output_array = [0] * len(arr)
 
    for i in range(len(arr) - 1, -1, -1):
        output_array[freq_arr[arr[i]] - 1] = arr[i]
        freq_arr[arr[i]] -= 1
    
    for i in range(len(arr)):
        arr[i] = output_array[i]
        draw_list(draw_info, {i: 'green'}, clear_bg=True)
        yield True
    
    return output_array
        
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
        yield from insertion_sort(draw_info,arr, i, end+1)

    size = min_run

    while size < high:
        for left in range(low, high, 2 * size):
            mid = min((left + size - 1), (high - 1))
            right = min((left + 2 * size - 1), (high - 1))
            if mid < right:
                yield from merge(draw_info, arr, left, mid, right)
        size = 2 * size
