#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponseServerError
import traceback

template = '''
    <div style="padding:50px 0px 0px 0px; font-size:48; text-align:center">
        <strong>%s</strong>
    </div>
    <div style="font-size:20; text-align:center">
        %s
    </div>
    <div style="padding:30px;">
        %s
    </div>
    <div style="padding:20px; font-size:12; text-align:center">
        Powered by Yard
    </div>
'''


class ServerErrorTemplate(HttpResponseServerError):
    '''
    Template for any Error in YARD side
    '''
    def __init__(self, text, with_trace=False):        
        if with_trace:
            trace   = [ (i[:i.index(',')], i[i.index(','):]) for i in traceback.format_stack()]
            trace   = "<br>".join( ["%s<small>%s</small>"%(a,b) for a,b in trace] )
            text    = "%s. Please notify the developer."%text
            content = template %("Server Error", text, trace)
        else:
            content = template %("Server Error", text, '')
        
        HttpResponseServerError.__init__(self, content)

    