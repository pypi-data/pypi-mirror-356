import concurrent.futures


# Example function to process
def my_function(arg1, arg2):
    # Simulate processing
    return arg1 + arg2


# Tuple of tuples of arguments
args_tuple = ((1, 2), (3, 4), (5, 6), (7, 8))


# Function to process the tuple of tuples in parallel
def process_in_parallel(args_tuple):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.m
    with concurrent.futures.ThreadPoolExecutor() as executor:

        # Use executor.map to apply the function in parallel
        results = list(executor.map(lambda args: my_function(*args), args_tuple))
    return results


# Run the function in parallel and get the results
result = process_in_parallel(args_tuple)

print(result)
