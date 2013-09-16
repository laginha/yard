# HTTP Responses

In case you prefer to use Http Response explicitly, *Yard* offers a small number of `HttpResponse` sub classes.


## JSON responses

Regarding *JSON* responses, *yard* does not apply any indentation for response efficiency purposes.

If you use Chrome, install [JSONView](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc) in order to make it easy to debug the *JSON* response on the browser.


### JsonResponse

Http Response with *JSON* or *JSONP* content type, according to context.

    JsonResponse( json_serializable_content, context=request )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)   
- **context** (optional)   


### JSONResponse

Http Response with *JSON* content type.

    JsonResponse( json_serializable_content )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)


### JSONPResponse

Http Response with *JSONP* content type. Use this for *AJAX* requests.

    JsonpResponse( json_serializable_content )

Expected arguments:

- **content** 
- **status** (optional)
- **mimetype** (optional)


## Other Responses

### FileResponse

Http Response with file content. The mimetype of the response is filled automatically according to the type of file.

    FileResponse( file )

Expected arguments:

- **content** 
- **filename** (optional)
- **status** (optional)
- **content_type** (optional)
