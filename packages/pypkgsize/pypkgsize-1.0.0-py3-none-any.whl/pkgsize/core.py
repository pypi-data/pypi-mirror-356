import importlib.metadata
import os
from pathlib import Path
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

_package_size_cache = {}

def _calculate_size_from_files(file_list, canonical_name_for_cache):
    if canonical_name_for_cache in _package_size_cache:
        return _package_size_cache[canonical_name_for_cache]

    total_size = 0
    if file_list:
        for file_path_str in file_list:
            try:
                path_obj = Path(file_path_str)
                if path_obj.is_file():
                    total_size += path_obj.stat().st_size
            except FileNotFoundError:
                pass
            except Exception:
                pass
    
    _package_size_cache[canonical_name_for_cache] = total_size
    return total_size

def get_package_size(distribution_or_data):
    
    if isinstance(distribution_or_data, dict):
        dist_name = distribution_or_data.get('name', 'UnknownPackageForCache')
        dist_canonical_name = canonicalize_name(dist_name)
        if dist_canonical_name in _package_size_cache:
            return _package_size_cache[dist_canonical_name]
        
        files_to_sum = distribution_or_data.get('files', [])
        return _calculate_size_from_files(files_to_sum, dist_canonical_name)
    else:
        distribution = distribution_or_data
        dist_canonical_name = canonicalize_name(distribution.metadata['Name'])
        if dist_canonical_name in _package_size_cache:
            return _package_size_cache[dist_canonical_name]

        total_size = 0
        file_paths_to_sum = []
        if distribution.files:
            location_path_obj = None
            try:
                located_file_root = distribution.locate_file('')
                if located_file_root:
                    location_path_obj = Path(located_file_root)
            except Exception:
                pass

            if location_path_obj and location_path_obj.is_dir():
                for path_obj_entry in distribution.files:
                    try:
                        abs_file_path = (location_path_obj / str(path_obj_entry)).resolve()
                        if abs_file_path.is_file():
                            file_paths_to_sum.append(str(abs_file_path))
                    except Exception:
                        pass
        
        return _calculate_size_from_files(file_paths_to_sum, dist_canonical_name)

def _get_recursive_dependencies(
    package_canonical_name,
    all_distributions_map,
    discovered_deps_set,
    processing_stack
):
    if package_canonical_name in processing_stack:
        return
    processing_stack.add(package_canonical_name)

    dist_entry = all_distributions_map.get(package_canonical_name)
    if not dist_entry:
        processing_stack.remove(package_canonical_name)
        return

    if isinstance(dist_entry, dict):
        requirements_list = dist_entry.get('requires', [])
    else:
        requirements_list = dist_entry.requires if dist_entry.requires is not None else []

    if not requirements_list:
        processing_stack.remove(package_canonical_name)
        return

    for req_string in requirements_list:
        try:
            req = Requirement(req_string)
            dep_canonical_name = canonicalize_name(req.name)

            if dep_canonical_name in all_distributions_map:
                if dep_canonical_name not in discovered_deps_set:
                    discovered_deps_set.add(dep_canonical_name)
                    
                    _get_recursive_dependencies(
                        dep_canonical_name,
                        all_distributions_map,
                        discovered_deps_set,
                        processing_stack
                    )
        except Exception:
            pass 

    processing_stack.remove(package_canonical_name)

def get_installed_packages_info(include_deps=False, external_package_data=None, target_env_description="current environment"):
    packages_info = []
    _package_size_cache.clear()
    
    source_iterable = None
    all_distributions_map = {}

    if external_package_data is not None:
        source_iterable = external_package_data
        for pkg_data in external_package_data:
            if 'name' in pkg_data:
                all_distributions_map[canonicalize_name(pkg_data['name'])] = pkg_data
    else:
        live_distributions = list(importlib.metadata.distributions())
        source_iterable = live_distributions
        for d in live_distributions:
            all_distributions_map[canonicalize_name(d.metadata['Name'])] = d

    if not source_iterable:
        return []

    for dist_or_data_item in source_iterable:
        is_dict_data = isinstance(dist_or_data_item, dict)

        if is_dict_data:
            name = dist_or_data_item.get('name', 'Unknown')
            version = dist_or_data_item.get('version', 'N/A')
            package_location = dist_or_data_item.get('location', 'N/A')
        else: 
            dist = dist_or_data_item
            name = dist.metadata['Name']
            version = dist.metadata['Version']
            package_location = "N/A"
            try:
                located_root = dist.locate_file('')
                package_location = str(located_root) if located_root else "N/A (unlocatable)"
            except FileNotFoundError:
                package_location = "N/A (not found)"
            except Exception:
                package_location = "Error determining location"

        current_package_size_bytes = get_package_size(dist_or_data_item)
        total_size_bytes = current_package_size_bytes

        dependencies_breakdown_list = []
        if include_deps:
            discovered_deps_for_this_package = set()
            _get_recursive_dependencies(
                canonicalize_name(name),
                all_distributions_map,
                discovered_deps_for_this_package,
                set()
            )
            
            for dep_canonical_name in discovered_deps_for_this_package:
                if dep_canonical_name == canonicalize_name(name):
                    continue

                dep_entry = all_distributions_map.get(dep_canonical_name)
                if dep_entry:
                    is_dep_dict_data = isinstance(dep_entry, dict)
                    if is_dep_dict_data:
                        dep_name = dep_entry.get('name', 'Unknown')
                        dep_version = dep_entry.get('version', 'N/A')
                        dep_location = dep_entry.get('location', 'N/A')
                    else:
                        dep_dist_obj = dep_entry
                        dep_name = dep_dist_obj.metadata['Name']
                        dep_version = dep_dist_obj.metadata['Version']
                        dep_location = "N/A"
                        try:
                            located_root = dep_dist_obj.locate_file('')
                            dep_location = str(located_root) if located_root else "N/A (unlocatable)"
                        except FileNotFoundError:
                            dep_location = "N/A (not found)"
                        except Exception:
                            dep_location = "Error determining location"
                    
                    dep_size_bytes = get_package_size(dep_entry)
                    
                    dependencies_breakdown_list.append({
                        "name": dep_name,
                        "version": dep_version,
                        "size_bytes": dep_size_bytes,
                        "location": dep_location
                    })
                    total_size_bytes += dep_size_bytes
        
        pkg_info_entry = {
            "name": name,
            "version": version,
            "size_bytes": total_size_bytes,
            "location": package_location,
        }
        if include_deps:
            dependencies_breakdown_list.sort(key=lambda d: d['size_bytes'], reverse=True)
            pkg_info_entry["dependencies_breakdown"] = dependencies_breakdown_list
        
        packages_info.append(pkg_info_entry)
        
    return packages_info

if __name__ == '__main__':
    installed_packages = get_installed_packages_info()
    if installed_packages:
        installed_packages.sort(key=lambda x: x['size_bytes'], reverse=True)
        print(f"{'Package Name':<40} | {'Version':<15} | {'Size':<15} | {'Location'}")
        print("-" * 100)
        for pkg in installed_packages:
            size_mb = pkg['size_bytes'] / (1024 * 1024)
            print(f"{pkg['name']:<40} | {pkg['version']:<15} | {size_mb:,.2f} MB{'':<7} | {pkg['location']}")
    else:
        print("No packages found or error retrieving package information.")
