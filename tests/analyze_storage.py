#!/usr/bin/env python3

def calculate_total():
    file_sizes = {
        'mp4': 319.21,
        'insv': 49.21,
        'jpg': 9.90,
        'vob': 9.03,
        'wav': 6.84,
        'lrv': 3.46,
        'mpg': 1.40,
        'mpeg': 1.30,
        'partial': 1.30,
        'm4a': 1.19,
        'png': 0.62,
        'mov': 0.50,
        'mkv': 0.23,
        'no_extension': 0.19,
        'insp': 0.19,
        'zip': 0.16,
        'heic': 0.12,
        'pdf': 0.03,
        'jpeg': 0.02,
        'mogrt': 0.02,
        'gif': 0.02
        # Other formats sum to less than 0.01 GB
    }
    
    total = sum(file_sizes.values())
    
    print("Storage Summary")
    print("=" * 50)
    print(f"Total Storage: {total:.2f} GB")
    print("\nBreakdown by largest formats:")
    print("-" * 50)
    
    # Sort by size and show percentage
    sorted_sizes = sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)
    for ext, size in sorted_sizes:
        if size > 1.0:  # Only show formats using more than 1GB
            percentage = (size / total) * 100
            print(f"{ext:10} {size:8.2f} GB ({percentage:5.1f}%)")

if __name__ == "__main__":
    calculate_total()