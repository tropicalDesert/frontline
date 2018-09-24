status_codes={
    "version":"HTTP/1.1",
    "200":{
        "Content-Type":"text/html",
        "Cache-Control":"no-cache, private",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "ACCEPT_ENCODING":"gzip, deflate, br",
        "ACCEPT_LANGUAGE":"en-US,en;q=0.9",
        "Connection":"keep-alive",
        "DNT":"1",
        "USER_AGENT":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
}

def status(code):
    status_code=str(code)
    headers=status_codes['version'] + " " + status_code + "\r"
    status_code_headers=status_codes[status_code]
    for key in status_code_headers.keys():
        header=key + ": " + status_code_headers[key] + "\r\n"
        headers+=header
    headers+="\r\n"
    return headers
