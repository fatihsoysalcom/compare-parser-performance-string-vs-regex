import time
import re
import random
import string

def generate_data(num_lines=50000):
    """Generates a large string of simulated data for parsing."""
    data_lines = []
    for i in range(num_lines):
        user_id = i + 1
        # Generate a random name
        name_length = random.randint(5, 10)
        name = ''.join(random.choices(string.ascii_letters, k=name_length)).capitalize()
        value = round(random.uniform(10.0, 1000.0), 2)
        data_lines.append(f"ID:{user_id} NAME:{name} VALUE:{value}")
    return "\n".join(data_lines)

def slow_parser(data_string):
    """
    Parses data using regular expressions, which can be slower for simple delimited data.
    This demonstrates an inefficient parsing strategy for this specific data structure.
    """
    parsed_records = []
    # Compiling regex is a good practice, but for simple delimited data, regex can still be slower
    # than direct string manipulation due to its overhead and generality.
    line_pattern = re.compile(r"ID:(\d+)\sNAME:([a-zA-Z]+)\sVALUE:([\d.]+)")
    for line in data_string.split('\n'):
        if not line:
            continue
        match = line_pattern.search(line)
        if match:
            record = {
                "id": int(match.group(1)),
                "name": match.group(2),
                "value": float(match.group(3))
            }
            parsed_records.append(record)
    return parsed_records

def fast_parser(data_string):
    """
    Parses data using string splitting, which is generally faster for simple delimited data.
    This demonstrates a more efficient parsing strategy by leveraging direct string methods.
    """
    parsed_records = []
    for line in data_string.split('\n'):
        if not line:
            continue
        record = {}
        # Split the line into key-value pair strings (e.g., ['ID:123', 'NAME:Alice', 'VALUE:45.67'])
        parts = line.split(' ')
        for part in parts:
            # Split each key-value pair (e.g., ['ID', '123'])
            key_val = part.split(':', 1)
            if len(key_val) == 2:
                key, val = key_val
                if key == "ID":
                    record["id"] = int(val)
                elif key == "NAME":
                    record["name"] = val
                elif key == "VALUE":
                    record["value"] = float(val)
        parsed_records.append(record)
    return parsed_records

if __name__ == "__main__":
    NUM_LINES = 100000 # Increased for more noticeable difference in performance
    print(f"Generating {NUM_LINES} lines of simulated data...")
    data_to_parse = generate_data(NUM_LINES)
    print("Data generation complete.\n")

    # --- Test Slow Parser --- 
    # This section measures the performance of the regex-based parser.
    start_time = time.perf_counter()
    slow_parsed_data = slow_parser(data_to_parse)
    end_time = time.perf_counter()
    slow_time = end_time - start_time
    print(f"Slow parser processed {len(slow_parsed_data)} records in {slow_time:.4f} seconds.")

    # --- Test Fast Parser --- 
    # This section measures the performance of the string-splitting parser.
    start_time = time.perf_counter()
    fast_parsed_data = fast_parser(data_to_parse)
    end_time = time.perf_counter()
    fast_time = end_time - start_time
    print(f"Fast parser processed {len(fast_parsed_data)} records in {fast_time:.4f} seconds.")

    print(f"\nPerformance difference: Fast parser was {slow_time / fast_time:.2f} times faster.")

    # Optional: Verify results are the same
    # assert slow_parsed_data == fast_parsed_data
    # print("Verification successful: Both parsers produced identical results.")
