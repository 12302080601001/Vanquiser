#!/usr/bin/env python3
"""
Script to remove duplicate images from the uploads folder
"""
import os
import hashlib
import json
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def find_duplicates(upload_folder):
    """Find duplicate images based on file hash"""
    file_hashes = defaultdict(list)
    
    if not os.path.exists(upload_folder):
        print(f"Upload folder {upload_folder} does not exist")
        return {}
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    for filename in os.listdir(upload_folder):
        filepath = os.path.join(upload_folder, filename)
        if os.path.isfile(filepath):
            # Check if it's an image file
            _, ext = os.path.splitext(filename.lower())
            if ext in image_extensions:
                file_hash = get_file_hash(filepath)
                if file_hash:
                    file_hashes[file_hash].append(filepath)
    
    # Find duplicates (hashes with more than one file)
    duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
    
    return duplicates

def remove_duplicates(upload_folder, items_file):
    """Remove duplicate images and update items.json"""
    print("Scanning for duplicate images...")
    
    duplicates = find_duplicates(upload_folder)
    
    if not duplicates:
        print("No duplicate images found!")
        return
    
    print(f"Found {len(duplicates)} sets of duplicate images:")
    
    # Load items data to check which files are referenced
    items_data = []
    if os.path.exists(items_file):
        try:
            with open(items_file, 'r') as f:
                items_data = json.load(f)
        except Exception as e:
            print(f"Error loading items data: {e}")
    
    # Get list of referenced image files
    referenced_files = set()
    for item in items_data:
        if 'image' in item:
            # Extract filename from path
            image_path = item['image']
            if image_path.startswith('static/'):
                referenced_files.add(os.path.join(image_path))
    
    removed_count = 0
    
    for hash_val, file_list in duplicates.items():
        print(f"\nDuplicate set (hash: {hash_val[:8]}...):")
        
        # Sort files by modification time (keep the oldest)
        file_list.sort(key=lambda x: os.path.getmtime(x))
        
        # Keep the first file, remove the rest
        keep_file = file_list[0]
        remove_files = file_list[1:]
        
        print(f"  Keeping: {keep_file}")
        
        for remove_file in remove_files:
            # Check if this file is referenced in items
            relative_path = remove_file.replace('\\', '/')
            if relative_path in referenced_files:
                print(f"  Skipping: {remove_file} (referenced in items)")
            else:
                try:
                    os.remove(remove_file)
                    print(f"  Removed: {remove_file}")
                    removed_count += 1
                except Exception as e:
                    print(f"  Error removing {remove_file}: {e}")
    
    print(f"\nRemoved {removed_count} duplicate images.")

if __name__ == "__main__":
    upload_folder = "static/uploads"
    items_file = "data/items.json"
    
    remove_duplicates(upload_folder, items_file)
