#!/usr/bin/env python
# encoding: utf-8
import re

def get_entry_paths(urllist, lambda_):
    pathlist = []
    for entry in urllist:
        regex = r'\?|\$|\^|\(|P|\)|<.*>'
        entry.clean_pattern = re.sub( regex, '', entry.regex.pattern )
        if hasattr(entry, 'url_patterns'):
            for i in get_paths( entry.url_patterns ):
                pathlist.append( entry.clean_pattern + i )
        elif not entry.clean_pattern or entry.name and 'single' in entry.name:
           continue
        else:
            pathlist.append( lambda_(entry) )
    return pathlist
