import csv
from os import path

def save_as_tsv(location, file_name, data):
    """
    Saves infomation in an ordered dictionary to a tsv file

    Parameters
    ----------
    location: str
        Absolute file path of the location to write tsv.
    file_name: str
        Name of the tsv.
    data: ordered dict
        Data to write to the tsv.
    """
    
    full_file_path = location + file_name + ".tsv"

    if path.exists(full_file_path):
        with open(full_file_path, "a+") as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(data.values())
    else:
        with open(full_file_path, "w", newline='') as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(data.keys())
            tsv_writer.writerow(data.values())