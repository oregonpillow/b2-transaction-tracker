
"""

b2_delete_key is not an official transaction name, but is used within the reports page instead of
b2_delete_file_version. This is an inconsistency that I have reported to b2 which they have
acknowledged.

every time you access the reports page (aka run this app) you are actually increasing your
b2_list_buckets by 1, since b2 run this transaction themselves to get your account info.

"""

class_a = [
'b2_cancel_large_file',
'b2_delete_bucket',
'b2_delete_file',
'b2_delete_file_version',
'b2_delete_key',
'b2_finish_large_file',
'b2_get_upload_part_url',
'b2_get_upload_url',
'b2_hide_file',
'b2_start_large_file',
'b2_update_file_legal_hold',
'b2_update_file_retention',
'b2_upload_file',
'b2_upload_part',
]

class_b = [
'b2_download_file_by_id',
'b2_download_file_by_name',
'b2_get_file_info',
]

class_c = [
'b2_authorize_account',
'b2_copy_file',
'b2_copy_part',
'b2_create_bucket',
'b2_create_key',
'b2_get_download_authorization',
'b2_list_buckets',
'b2_list_file_names',
'b2_list_file_versions',
'b2_list_keys',
'b2_list_parts',
'b2_list_unfinished_large_files',
'b2_update_bucket',
]
