import sys
import threading
from queue import Queue
import os
import random
from string import ascii_letters
import urllib.request as request

index_url = sys.argv[1]
output_folder = ''.join(random.choices(ascii_letters, k=5))
output_filename = sys.argv[2]

root_url = '/'.join(index_url.split('/')[:-1])
print(f"Using root URL {root_url}")

def line_filter(line: str):
    return line.endswith('.ts')

def append_root_to_filename(filename: str):
    return f"{root_url}/{filename}"

def download_file(file_url: str):
    return request.urlopen(file_url).read()

item_queue = Queue()
downloaded_items = {}

def download_worker():
    while not item_queue.empty():
        next_filename = item_queue.get()
        next_url = append_root_to_filename(next_filename)
        downloaded_items[next_filename] = download_file(next_url)
        item_queue.task_done()
        print(f"{item_queue.unfinished_tasks} .ts files remaining", end='\r')

index_file_text = request.urlopen(index_url).read().decode('utf-8')
index_file_list = list(filter(line_filter, index_file_text.split('\n')))
for filename in index_file_list:
    item_queue.put(filename)

print("Starting workers")
for thread_index in range(0, 30):
    thread = threading.Thread(target=download_worker)
    thread.start()

item_queue.join()
print()

os.mkdir(output_folder)
for file in downloaded_items:
    with open(f'{output_folder}/{file}', 'wb') as output_file:
        output_file.write(downloaded_items[file])
with open(f'{output_folder}/index.m3u8', 'w') as m3u8_file:
    m3u8_file.write(index_file_text)

os.system(f'ffmpeg -i {output_folder}/index.m3u8 -codec copy {output_filename}')
os.system(f'rm -rf {output_folder}')
