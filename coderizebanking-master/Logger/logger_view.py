import os
from django.shortcuts import render
from django.http import HttpResponse


def get_server_log(request):
    log_file_path = os.path.join('Logger', 'dev_log_files', 'dev-log.log')

    try:
        with open(log_file_path) as log_file:

            formatter = ["date", "time", "name", "levelname"]
            table_entries = []
            for l in log_file.readlines():
                try:
                    log_entry_dict = {formatter[i]: x for i, x in enumerate(l.split(" ")[:4])}
                    log_entry_dict['message'] = l.split(log_entry_dict['levelname'])[1]
                    table_entries.append(log_entry_dict)
                except Exception as e:
                    pass

            return render(request, 'log_render.html', context={"table": table_entries})
    except FileNotFoundError:
        return HttpResponse(f"Log file not found at {log_file_path}")
