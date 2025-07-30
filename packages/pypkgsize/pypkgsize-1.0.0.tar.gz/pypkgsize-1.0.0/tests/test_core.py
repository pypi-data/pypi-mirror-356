import pytest
from pathlib import Path
from unittest.mock import MagicMock, call

# Ensure pkgsize.core can be imported.
# This might require adding an __init__.py to the tests folder (if not already present)
# and ensuring the main project directory (pypkgsize) is in PYTHONPATH,
# or the package is installed in editable mode (e.g., pip install -e . from the root of pypkgsize).
from pkgsize.core import _calculate_size_from_files, _package_size_cache, canonicalize_name

# Helper to create a mock Path object with a specific size
def mock_path_object(file_path_str, size_bytes, is_file=True):
    mock_path = MagicMock(spec=Path)
    # When Path objects are created, their string representation might be used internally or for comparison.
    mock_path.__str__.return_value = file_path_str 
    mock_path.is_file.return_value = is_file
    if is_file:
        mock_stat = MagicMock()
        mock_stat.st_size = size_bytes
        mock_path.stat.return_value = mock_stat
    else:
        # If it's not a file, stat might not be called or might raise an error if called.
        pass
    return mock_path

@pytest.fixture(autouse=True)
def clear_cache_before_each_test():
    _package_size_cache.clear()
    yield # This ensures the cache is also cleared after the test if needed

def test_calculate_size_from_files_empty_list(mocker):
    """Test with an empty list of files."""
    # Mock the Path class constructor specifically within pkgsize.core
    path_constructor_mock = mocker.patch('pkgsize.core.Path')
    assert _calculate_size_from_files([], "test_pkg_empty") == 0
    path_constructor_mock.assert_not_called() # Path() constructor shouldn't be called for an empty list

def test_calculate_size_from_files_single_file(mocker):
    """Test with a single file."""
    file_path_str = "/fake/path/file1.py"
    mock_file1 = mock_path_object(file_path_str, 100)
    
    path_constructor_mock = mocker.patch('pkgsize.core.Path', return_value=mock_file1)
    
    assert _calculate_size_from_files([file_path_str], "test_pkg_single") == 100
    path_constructor_mock.assert_called_once_with(file_path_str)
    mock_file1.is_file.assert_called_once()
    mock_file1.stat.assert_called_once()

def test_calculate_size_from_files_multiple_files(mocker):
    """Test with multiple files."""
    file1_path_str = "/fake/path/file1.py"
    file2_path_str = "/fake/path/file2.py"
    
    mock_file1 = mock_path_object(file1_path_str, 100)
    mock_file2 = mock_path_object(file2_path_str, 200)

    # Path() will be called for each file string in the list.
    def path_side_effect(path_arg_str):
        if path_arg_str == file1_path_str:
            return mock_file1
        if path_arg_str == file2_path_str:
            return mock_file2
        raise ValueError(f"Unexpected path argument to Path constructor: {path_arg_str}")

    path_constructor_mock = mocker.patch('pkgsize.core.Path', side_effect=path_side_effect)
    
    assert _calculate_size_from_files([file1_path_str, file2_path_str], "test_pkg_multi") == 300
    assert path_constructor_mock.call_count == 2
    path_constructor_mock.assert_any_call(file1_path_str)
    path_constructor_mock.assert_any_call(file2_path_str)
    mock_file1.stat.assert_called_once()
    mock_file2.stat.assert_called_once()

def test_calculate_size_from_files_file_not_file(mocker):
    """Test with a path that is_file() returns False."""
    file1_path_str = "/fake/path/file1.py" # Valid file
    file2_path_str = "/fake/path/not_a_file.txt" # Not a file
    
    mock_file1 = mock_path_object(file1_path_str, 100, is_file=True)
    mock_not_a_file = mock_path_object(file2_path_str, 0, is_file=False)

    def path_side_effect(path_arg_str):
        if path_arg_str == file1_path_str:
            return mock_file1
        if path_arg_str == file2_path_str:
            return mock_not_a_file
        raise ValueError(f"Unexpected path argument to Path constructor: {path_arg_str}")

    path_constructor_mock = mocker.patch('pkgsize.core.Path', side_effect=path_side_effect)
    
    assert _calculate_size_from_files([file1_path_str, file2_path_str], "test_pkg_mixed") == 100
    
    path_constructor_mock.assert_any_call(file1_path_str)
    path_constructor_mock.assert_any_call(file2_path_str)
    
    mock_file1.is_file.assert_called_once()
    mock_file1.stat.assert_called_once()
    
    mock_not_a_file.is_file.assert_called_once() 
    mock_not_a_file.stat.assert_not_called() # stat should not be called if is_file is False

def test_calculate_size_from_files_caching(mocker):
    """Test that results are cached and Path().stat() is not called again."""
    file_path_str = "/fake/path/file_for_cache.py"
    mock_file_for_cache = mock_path_object(file_path_str, 150)
    
    path_constructor_mock = mocker.patch('pkgsize.core.Path', return_value=mock_file_for_cache)
    
    # First call: should calculate, call Path() and .stat(), and cache
    assert _calculate_size_from_files([file_path_str], "test_pkg_caching_demo") == 150
    path_constructor_mock.assert_called_once_with(file_path_str)
    mock_file_for_cache.is_file.assert_called_once()
    mock_file_for_cache.stat.assert_called_once()

    # Reset mocks for the next part of the test
    path_constructor_mock.reset_mock()
    mock_file_for_cache.is_file.reset_mock()
    mock_file_for_cache.stat.reset_mock()

    # Second call with the same canonical name: should return from cache
    assert _calculate_size_from_files([file_path_str], "test_pkg_caching_demo") == 150
    
    # Path() constructor, .is_file(), and .stat() should NOT be called again
    path_constructor_mock.assert_not_called()
    mock_file_for_cache.is_file.assert_not_called()
    mock_file_for_cache.stat.assert_not_called()


# --- Tests for get_package_size ---

from pkgsize.core import get_package_size # Add get_package_size

def test_get_package_size_with_dict_data_no_files(mocker):
    """Test get_package_size with dictionary data that has an empty 'files' list."""
    mock_calculate_size = mocker.patch('pkgsize.core._calculate_size_from_files', return_value=0)
    mock_canonicalize = mocker.patch('pkgsize.core.canonicalize_name')
    mock_canonicalize.side_effect = lambda x: x # Pass-through

    pkg_data = {"name": "TestPkg", "files": []}
    assert get_package_size(pkg_data) == 0
    mock_calculate_size.assert_called_once_with([], "TestPkg")
    mock_canonicalize.assert_called_once_with("TestPkg")

def test_get_package_size_with_dict_data_with_files(mocker):
    """Test get_package_size with dictionary data that has files."""
    mock_calculate_size = mocker.patch('pkgsize.core._calculate_size_from_files', return_value=1234)
    mock_canonicalize = mocker.patch('pkgsize.core.canonicalize_name')
    mock_canonicalize.side_effect = lambda x: x

    pkg_data = {"name": "TestPkgWithFiles", "files": ["/path/to/file1", "/path/to/file2"]}
    assert get_package_size(pkg_data) == 1234
    mock_calculate_size.assert_called_once_with(["/path/to/file1", "/path/to/file2"], "TestPkgWithFiles")
    mock_canonicalize.assert_called_once_with("TestPkgWithFiles")

def test_get_package_size_with_dict_data_caching(mocker):
    """Test caching behavior when get_package_size receives dict data."""
    mock_calculate_size = mocker.patch('pkgsize.core._calculate_size_from_files', return_value=500)
    # canonicalize_name will be called for cache key generation
    mock_canonicalize = mocker.patch('pkgsize.core.canonicalize_name')
    mock_canonicalize.side_effect = lambda name: f"canon_{name}"

    pkg_data = {"name": "CachedPkg", "files": ["/file.txt"]}

    # First call
    assert get_package_size(pkg_data) == 500
    mock_calculate_size.assert_called_once_with(["/file.txt"], "canon_CachedPkg")
    mock_canonicalize.assert_called_once_with("CachedPkg")
    
    mock_calculate_size.reset_mock()
    mock_canonicalize.reset_mock()

    # Manually populate the cache as if _calculate_size_from_files did it
    # This is because _calculate_size_from_files is mocked and won't populate the actual cache.
    _package_size_cache["canon_CachedPkg"] = 500

    # Second call - _calculate_size_from_files should not be called again due to cache hit in get_package_size
    assert get_package_size(pkg_data) == 500
    mock_calculate_size.assert_not_called()
    # canonicalize_name is still called to check the cache
    mock_canonicalize.assert_called_once_with("CachedPkg")


# Mock for importlib.metadata.Distribution
from importlib.metadata import Distribution

def test_get_package_size_with_distribution_object_no_files(mocker):
    """Test get_package_size with a Distribution object that has no files."""
    mock_calculate_size = mocker.patch('pkgsize.core._calculate_size_from_files', return_value=0)
    mock_canonicalize = mocker.patch('pkgsize.core.canonicalize_name')
    mock_canonicalize.side_effect = lambda x: x

    dist = mocker.create_autospec(Distribution, instance=True, name="DistNoFiles_spec")
    dist.metadata = {'Name': "DistNoFiles", 'Version': "1.0"}
    dist.files = []
    mock_location = MagicMock(spec=Path)
    # For empty files, is_dir might not be checked if location itself is None, but good to have for consistency
    mock_location.is_dir.return_value = True 
    dist.locate_file.return_value = mock_location

    assert get_package_size(dist) == 0
    # _calculate_size_from_files is called with an empty list of resolved paths
    mock_calculate_size.assert_called_once_with([], "DistNoFiles")
    mock_canonicalize.assert_called_once_with("DistNoFiles")

def test_get_package_size_with_distribution_object_one_file(mocker):
    """Test get_package_size with a Distribution object that has one file."""
    mock_calculate_size = mocker.patch('pkgsize.core._calculate_size_from_files', return_value=1000)
    mock_canonicalize = mocker.patch('pkgsize.core.canonicalize_name')
    mock_canonicalize.side_effect = lambda x: x

    # Path object that will be returned by the instance's dist.locate_file('')
    mock_dist_location_path = MagicMock(name="mock_dist_location_path_obj") # No spec=Path
    mock_dist_location_path.is_dir.return_value = True

    # Final resolved Path object (result of .resolve())
    mock_resolved_file1 = MagicMock() # No spec=Path
    mock_resolved_file1.is_file.return_value = True
    mock_resolved_file1.__str__.return_value = "/fake/dist/location/file1.py"

    # Intermediate Path object (result of __truediv__ before .resolve())
    mock_joined_path1 = MagicMock() # No spec=Path
    mock_joined_path1.resolve.return_value = mock_resolved_file1
    
    # Configure __truediv__ to return the joined_path mock when called with "file1.py"
    def truediv_side_effect_one_file(relative_path_str):
        if relative_path_str == "file1.py":
            return mock_joined_path1
        # Fallback for unexpected calls, aids debugging
        fallback_mock = MagicMock(name=f"truediv_fallback_{relative_path_str}")
        fallback_mock.resolve.return_value = MagicMock(is_file=lambda: False) # Ensure it doesn't accidentally pass is_file check
        return fallback_mock
    mock_dist_location_path.__truediv__.side_effect = truediv_side_effect_one_file

    # Create an autospecced Distribution instance
    dist = mocker.create_autospec(Distribution, instance=True, name="DistWithOneFile_spec")
    dist.metadata = {'Name': "DistWithOneFile", 'Version': "1.0"}
    dist.files = ["file1.py"]

    # Mock dist.locate_file to return a marker string
    locate_file_marker = "marker_for_path_constructor_one_file"
    dist.locate_file = MagicMock(return_value=locate_file_marker, name="dist_locate_file_mock")

    # Patch pkgsize.core.Path constructor
    # mock_dist_location_path is defined earlier and configured with is_dir, __truediv__ etc.
    def path_constructor_side_effect(arg):
        if arg == locate_file_marker:
            return mock_dist_location_path # This is our pre-configured mock
        # For any other Path() call in the SUT for this test, create a default mock
        return MagicMock(name=f"unexpected_Path_call_with_{arg}") 
    mock_path_constructor = mocker.patch('pkgsize.core.Path', side_effect=path_constructor_side_effect)

    result_size = get_package_size(dist)
    assert result_size == 1000

    dist.locate_file.assert_called_once_with('')
    mock_path_constructor.assert_called_once_with(locate_file_marker)
    mock_dist_location_path.is_dir.assert_called_once()

    # Assert that __truediv__ was called correctly
    mock_dist_location_path.__truediv__.assert_called_once_with("file1.py")
    mock_joined_path1.resolve.assert_called_once()
    mock_resolved_file1.is_file.assert_called_once()
    mock_calculate_size.assert_called_once_with(['/fake/dist/location/file1.py'], 'DistWithOneFile')
    mock_canonicalize.assert_called_once_with("DistWithOneFile")

def test_get_package_size_with_distribution_object_caching(mocker):
    """Test caching with Distribution objects."""
    mock_calculate_size = mocker.patch('pkgsize.core._calculate_size_from_files', return_value=300)
    mock_canonicalize = mocker.patch('pkgsize.core.canonicalize_name')
    mock_canonicalize.side_effect = lambda name: f"canon_{name}"

    # Path object that the patched Distribution.locate_file will return for this test
    mock_dist_location_path_caching = MagicMock(name="mock_dist_location_path_caching_obj")
    mock_dist_location_path_caching.is_dir.return_value = True

    # Create an autospecced Distribution instance
    dist = mocker.create_autospec(Distribution, instance=True, name="CachedDist_spec")
    dist.metadata = {'Name': "CachedDist", 'Version': "1.0"}
    dist.files = ["file.txt"]

    # Mock dist.locate_file to return a marker string
    locate_file_marker_caching = "marker_for_path_constructor_caching"
    dist.locate_file = MagicMock(return_value=locate_file_marker_caching, name="dist_locate_file_caching_mock")

    # Patch pkgsize.core.Path constructor for this test
    # mock_dist_location_path_caching is defined earlier and configured
    def path_constructor_side_effect_caching(arg):
        if arg == locate_file_marker_caching:
            return mock_dist_location_path_caching # This is our pre-configured mock
        return MagicMock(name=f"unexpected_Path_call_caching_with_{arg}")
    mock_path_constructor_caching = mocker.patch('pkgsize.core.Path', side_effect=path_constructor_side_effect_caching)

    # Mocking the result of (location / str(p_entry_obj)).resolve()
    mock_resolved_cached_file = MagicMock() # No spec=Path
    mock_resolved_cached_file.is_file.return_value = True
    mock_resolved_cached_file.__str__.return_value = "/fake/cached_dist_location/file.txt"
    
    mock_joined_cached_path = MagicMock() # No spec=Path
    mock_joined_cached_path.resolve.return_value = mock_resolved_cached_file

    def truediv_side_effect_cached_file(relative_path_str):
        if relative_path_str == "file.txt":
            return mock_joined_cached_path
        fallback_mock = MagicMock(name=f"truediv_fallback_cached_{relative_path_str}")
        fallback_mock.resolve.return_value = MagicMock(is_file=lambda: False)
        return fallback_mock
    mock_dist_location_path_caching.__truediv__.side_effect = truediv_side_effect_cached_file
    
    # First call
    result_size1 = get_package_size(dist)
    assert result_size1 == 300
    # Ensure it's called with the correct file list from the mocked distribution
    mock_calculate_size.assert_called_once_with(['/fake/cached_dist_location/file.txt'], 'canon_CachedDist')
    dist.locate_file.assert_called_once_with('') # Called on the instance mock
    mock_path_constructor_caching.assert_called_once_with(locate_file_marker_caching)
    mock_dist_location_path_caching.is_dir.assert_called_once()
    mock_dist_location_path_caching.__truediv__.assert_called_once_with("file.txt")
    mock_joined_cached_path.resolve.assert_called_once()
    mock_resolved_cached_file.is_file.assert_called_once()

    mock_calculate_size.reset_mock()
    mock_canonicalize.reset_mock()
    dist.locate_file.reset_mock() # Reset the instance mock
    mock_path_constructor_caching.reset_mock() # Reset the Path constructor mock
    mock_dist_location_path_caching.reset_mock() # Reset calls to is_dir, __truediv__ etc.

    # Manually populate the cache as if _calculate_size_from_files did it
    _package_size_cache["canon_CachedDist"] = 300

    # Second call
    result_size2 = get_package_size(dist)
    assert result_size2 == 300
    mock_calculate_size.assert_not_called() 
    mock_canonicalize.assert_called_once_with("CachedDist")
    # locate_file and Path() constructor should NOT be called again due to the cache hit
    dist.locate_file.assert_not_called()
    mock_path_constructor_caching.assert_not_called()