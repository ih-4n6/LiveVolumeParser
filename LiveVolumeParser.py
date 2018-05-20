import time
import os
from multiprocessing import Pool
from operator import itemgetter

def get_file_info(fp):
    """
    This is a demo function to be parsed by each worker under the function "worker"
    :param fp: full file path of file to get info of
    :return: dict of file details
    """
    # Create empty set of vallues in case errors occur in reading file
    dict_details = {'size': 0,
                    'ctime': '',
                    'mtime': ''}

    try:
        dict_details = {'size': os.path.getsize(fp),
                        'ctime': os.path.getctime(fp),
                        'mtime': os.path.getmtime(fp)}
    except FileNotFoundError:
        pass

    # Try to open file
    try:
        with open(fp, 'rb') as f:
            magic = f.read(8)
            dict_details['magic'] = magic
    except PermissionError:
        # Provide empty string if permission error
        dict_details['magic'] = ''
    return dict_details

def worker(file_list):
    """
    This is the function detailing which each worker (process) will do.
    :param file_list: list of full file paths to process
    :return: dict of file info
    """

    file_dict_details = {}

    for file_path in file_list:
        print('Parsing {}'.format(file_path))
        file_dict_details[file_path] = get_file_info(file_path)

    return file_dict_details

def build_file_list(root_path):
    """
    Function to build list of full file paths to send to workers.
    Additional filters can be added to this then only actioned if specified by input arguments
    :param root_path: Starting file path to build list from
    :return: list of file paths, sorted by size
    """

    list_file_paths = []

    for root, dirs, names in os.walk(root_path):
        for name in names:
            # Make full path
            full_path = os.path.join(root, name)

            # Add filter functions here

            # Add to list if it has passed all filter tests
            list_file_paths.append(full_path)

    list_file_paths = sorted(list_file_paths, key=itemgetter(1))

    return list_file_paths


if __name__ == '__main__':
    # Sys args will go in here
    num_processes = 8
    root_path = r'C:\\Users'

    # Create a pool with specified number of processes
    pool = Pool(processes=num_processes)

    # Build list of file paths
    print('Building file list from {0}'.format(root_path))
    file_path_list = build_file_list(root_path)
    print('\t{0} file paths returned'.format(len(file_path_list)))

    # Split input list according to num_processes
    print('Splitting file list into {0} chunks'.format(num_processes))
    master_list = []
    # First make empty sub lists, one for each process
    for n in range(num_processes):
        master_list.append([])
    # Now add file paths evenly to them
    count = 0
    for file_path in file_path_list:
        master_list[count % num_processes].append(file_path)
        count+=1
    print('\tDone')
    # Record the start time
    start_time = time.time()

    # Pass the work to the workers, which return results to a list
    print('Passing chunks to process pool for processing')
    results = pool.map(worker, master_list)
    print('Processing complete')

    # Record the end time
    end_time = time.time()
    print('{} parsed in {} seconds'.format(len(file_path_list), end_time - start_time))

    # Results can now be compiled into one master list, or kept separate for sending to workers for
    # additional processing