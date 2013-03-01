# HTTP Responses

In case you prefer to use Http Response explicitly, *Yard* offers a small number of `HttpResponse` sub classes.


## JSON responses

Regarding *JSON* responses, *yard* applies indentation if setting's `DEBUG` set to `True` in order to make it easy for the developer to see and validate the *JSON* representation while in develop mode. Otherwise, *JSON* is returned without indentation for response efficiency purposes. 

By default, the indentation is set to two spaces, however it can be overwritten using `INDENT_JSON` setting.


### JsonResponse

Http Response with *JSON* content type.

    JsonResponse( json_serializable_content )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)


### JsonpResponse

Http Response with *JSONP* content type. Use this for *AJAX* requests.

    JsonpResponse( json_serializable_content )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)


### ProperJsonResponse

Http Response with *JSON* or *JSONP* content type, according to the request.

    ProperJsonResponse( request )( json_serializable_content )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)   


### JsonDebugResponse

HTTP Response recommended for debug purposes, which makes use of *Django Debug Toolbar* project.

    JsonDebugResponse( json_serializable_content )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)
- **content_type** (optional)

By default *Yard* returns a `JsonDebugResponse` if *Django Debug Toolbar* application is in the `INSTALLED_APPS` and if `DEBUG` is set to `True`. This behavior can be overwritten by using the setting `YARD_DEBUG_TOOLBAR`.


## Other Responses

### FileResponse

Http Response with file content. The mimetype of the response is filled automatically according to the type of file.

    FileResponse( file )

Expected arguments:

- **content** 
- **status** (optional)
- **content_type** (optional)
