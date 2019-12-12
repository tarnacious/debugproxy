/* @flow */

import type { FlowType } from 'types/flow';

export function truncate(s : string, n : number) {
  return (s.length > n) ? s.substr(0,n-1)+' ..' : s;
}

export function requestState(request) {
  if (!request) {
    return 0;
  }
  if (!request.response) {
    if (request.intercepted) {
      return 1;
    } else {
      return 2;
    }
  } else {
    if (request.intercepted) {
      return 3;
    } else {
      return 5; // no state 4 yet.
    }
  }
}

export function canEditRequest(request) {
  return requestState(request) < 2;
}

export function canEditResponse(request) {
  return requestState(request) === 3;
}

export function prettyUrl(data : FlowType, query = false) {
  var request = data.request;
  var path = "/"
  if (request.path) {
    const path = query ? request.path : request.path.split("?")[0];
    if (request.port == 80 || request.port == 443) {
      return request.scheme + "://" + request.host + path;
    } else {
      return request.scheme + "://" + request.host + ":" + request.port + path;
    }
  } else {
    // CONNECT requests
    if (request.port == 80) {
      return request.host;
    } else {
      return request.host + ":" + request.port;
    }
  }
}

export function arrayBufferToBase64( buffer : ArrayBuffer ): string {
    var binary = '';
    var bytes = new Uint8Array( buffer );
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode( bytes[ i ] );
    }
    return window.btoa( binary );
}

var BASE64_MARKER = ';base64,';

export function base64ToUint8Array(b64: string): Uint8Array {
  var base64Index = b64.indexOf(BASE64_MARKER) + BASE64_MARKER.length;
  var base64 = b64.substring(base64Index);
  var raw = window.atob(base64);
  var rawLength = raw.length;
  var array = new Uint8Array(new ArrayBuffer(rawLength));

  for(var i = 0; i < rawLength; i++) {
    array[i] = raw.charCodeAt(i);
  }
  return array;
}

export function stringToByteArray(str: string): Array<number> {
    var byteArray = [];
    for (var i = 0; i < str.length; i++)
        if (str.charCodeAt(i) <= 0x7F)
            byteArray.push(str.charCodeAt(i));
        else {
            var h = encodeURIComponent(str.charAt(i)).substr(1).split('%');
            for (var j = 0; j < h.length; j++)
                byteArray.push(parseInt(h[j], 16));
        }
    return byteArray;
};

export function unicodeToBase64(unicode: string): string {
  return window.btoa(stringToByteArray(unicode).map(function(x) { return String.fromCharCode(x) }).join(""))
}
