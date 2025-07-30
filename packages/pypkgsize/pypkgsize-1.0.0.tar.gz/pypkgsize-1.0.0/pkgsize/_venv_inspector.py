import importlib.metadata
import json
import sys
from pathlib import Path
import os

def main():
    distributions_data = []
    processed_dist_names = set()
    for dist in importlib.metadata.distributions():
        dist_name = dist.metadata.get('Name')
        if not dist_name or dist_name in processed_dist_names:
            continue 
        processed_dist_names.add(dist_name)

        location_str = "N/A"
        location_path_obj = None
        try:
            located_file_root = dist.locate_file('')
            if located_file_root:
                 location_path_obj = Path(located_file_root)
                 location_str = str(location_path_obj)
            else:
                location_str = "N/A (unlocatable)"

        except FileNotFoundError:
            location_str = "N/A (not found)"
        except Exception:
            location_str = "Error determining location"

        files_list = []
        if dist.files and location_path_obj and location_path_obj.is_dir():
            for file_entry in dist.files:
                try:
                    abs_file_path = (location_path_obj / str(file_entry)).resolve()
                    if abs_file_path.is_file():
                        files_list.append(str(abs_file_path))
                except OSError:
                    pass
                except Exception:
                    pass
        
        requires_list = dist.requires if dist.requires is not None else []

        distributions_data.append({
            "name": dist_name,
            "version": dist.metadata.get('Version', 'N/A'),
            "location": location_str,
            "requires": requires_list,
            "files": files_list,
        })

    json.dump(distributions_data, sys.stdout)

if __name__ == "__main__":
    main()
