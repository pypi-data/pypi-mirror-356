import pickle
import requests
import json
import os
from pathlib import Path
import psutil
import subprocess
import shutil
import re
import time
from datetime import datetime
import pytz

Features = dict
Print = None
FileWrite = None
# dump

import cv2
import os

def path(p):
  """
  Example:
    # Define a base directory
    base_dir = Path("/home/user")

    # Build a nested directory path using the / operator
    project_dir = base_dir / "Documents" / "Projects" / "MyProject"
  
  Notes:
    * The base_dir MUST be a path, i.e. this is invalid:
      project_dir = "/home/user" / Path("Documents") / "Projects" / "MyProject"
  """
  return Path(p)

def ts():
  local_tz = pytz.timezone('America/New_York')
  return datetime.now(local_tz).strftime("%m_%d_%Y_%H_%M_%S")

def save_image(img, path):
  cv2.imwrite(path, img) # correctly formats depending on ext provided

def seconds_to_clock(seconds):
  # Convert seconds to HH:MM:SS format
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return f"{hours:02}:{minutes:02}:{seconds:02}"

# this is wrong
def benchmark(f):
  start_time = time.time()
  #f()
  end_time = time.time()
  execution_time = end_time - start_time
  print("Execution time:", execution_time)

def parent_paths_glob(file_paths):
  """
  add all the parent paths to a set
  """
  s = set()
  for file_path in file_paths:
    s.add(d(file_path))
  return s

def d(path):
  return os.path.dirname(path)

def move_files(source_dir, target_dir):
    """
    Moves all files from source_dir to target_dir.

    Parameters:
    - source_dir: The directory to move files from.
    - target_dir: The directory to move files to.
    """
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Move each file from source_dir to target_dir
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        # Only move files; skip directories
        if os.path.isfile(source_path):
            print(f"Moving {filename} to {target_dir}...")
            shutil.move(source_path, target_path)

def opj(*args):
    # os.path.join rules:
    # - Joins multiple paths or filenames into a single path.
    # - Leading slashes in any component (except the first) discard previous parts.
    # - Trailing slashes are preserved.
    # - Use to join directories and filenames in a platform-independent way.
    return os.path.join(*args)

def opjs(paths, name_to_join):
  # i.e. opjs(['/a/b/c', '/a/b/d'], 'transcriptions')
  # returns ['/a/b/c/transcriptions', '/a/b/d/transcriptions']
  full_paths = []
  for path in paths:
      full_path = opj(path, name_to_join)
      full_paths.append(full_path)
  return full_paths

def m(f, arr):
  # map with a simpler interface, but less powerful because it cannot access each element, which might be desired with something like a dict, i.e. x[key]

  # also can't be called with multiple arguments...
  return list(map(lambda x: f(x), arr))

def ld(path):
  return os.listdir(path)

def ldp(path):
  files = os.listdir(path) 
  paths = [opj(path, file) for file in files]
  return paths

def flatten(nested_list):
  flattened_list = [item for sublist in nested_list for item in sublist]
  return(flattened_list)


def flatten_into(a,b):
  """
  a is a list
  b is a list of lists
  flatten the lists of b into a
  """
  for sublist in b:
      a.extend(sublist)

# Concatenate clips
def mem():
    memory = psutil.virtual_memory()
    available_memory_gb = memory.available / (1024 ** 3)
    print(f"Available Memory: {available_memory_gb:.2f} GB")

def fd(l, key, value):
  # find dict in list of dicts
  # this could return multiple dicts..
  # we'll assume one dict returned
  for d in l:
      if d[key] == value:
        return d
  return None

def rm(path):
    """
    Remove a file or folder and all its contents if it's a folder.

    :param path: The path to the file or folder to be removed
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Successfully removed the folder: {path}")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"Successfully removed the file: {path}")
        else:
            print(f"The path does not exist: {path}")
    except Exception as e:
        print(f"Error removing the path: {e}")

def mkdir(dir):
  os.makedirs(dir, exist_ok=True)

def rm_mkdir(dir):
  rm(dir)
  os.makedirs(dir, exist_ok=True)


def pd(o, fp):
    with open(fp, 'wb') as f:
        pickle.dump(o, f)


def pl(fp):
    with open(fp, 'rb') as f:
        return pickle.load(f)


def p(x) -> Print:
    print(x)


def w(x, fp):
    with open(fp, 'w') as f:
        f.write(x)

def wb(x, fp):
    with open(fp, 'wb') as f:
        f.write(x)

def wa(x, fp):
    with open(fp, 'a') as f:
        f.write(x)

def rl(f):
    with open(f, 'r') as u:
        return u.readlines()

def r(f):
    with open(f, 'r') as u:
        return u.read()

def rb(file_path):
    """
    Read the file in binary mode and return the content.
    """
    with open(file_path, 'rb') as file:  # Notice 'rb' for reading in binary mode
        return file.read()


def jl(jf):
    with open(jf, 'r') as f:
        return json.load(f)


def jd(x, fp):
    with open(fp, 'w') as f:
        json.dump(x, f, indent=2)

def jls(j):
    return json.loads(j)

def ls(dir):
  """
  Returns [dir/child_dir1, dir/child_dir2, ...]

  Example:
  utils.ls('twitch_streams')
  -> ['twitch_streams/royal2','twitch_streams/renegade',...]
  """
  return [os.path.join(dir, f) for f in os.listdir(dir)]

"""
def w(f):
    with open(f, 'w') as u:
        return json.loads(u.read())
"""

#from bs4 import BeautifulSoup
#def soup(url): 
#  response = requests.get(url)
#  if response.status_code == 200:
#    return BeautifulSoup(response.content, 'html.parser')
#  else:
#    print(f'non-200 response with {url}')
#    exit()
#      # throw an error?
#      # print? 
#      # Do I want calling code to catch?

def everything_before_extension(filename):

  pattern = r'^(.*)\.mp4$'

  match = re.match(pattern, filename)
  if match:
      base = match.group(1)
  return base

def get_file_basename(file_path):
  # Split the path by '/'
  path_parts = file_path.split('/')

  # Extract the last part (filename) and then split by '.' to remove the extension
  file_name_without_extension = path_parts[-1].split('.')[0]

  return file_name_without_extension


def source_env(script_path):
    """
    Source environment variables from a shell script into the current environment.
    """
    # Command to source the script and then output the environment
    command = f"source {script_path} && env"
    
    # Run the command and capture the output
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    out, err = proc.communicate()

    # Set the sourced environment variables in the current environment
    for line in out.splitlines():
        key, _, value = line.partition(b"=")
        os.environ[key.decode()] = value.decode()
