from servicepytan.utils import request_json, check_default_options, endpoint_url, get_folder_and_path

folder, endpoint = get_folder_and_path()

def get_list(query={}, key_file='st_api_credentials.json', request_type="GET"):
  url = endpoint_url(folder, endpoint, key_file=key_file)
  options = check_default_options(query)
  return request_json(url, options, payload="", key_file=key_file, request_type=request_type)