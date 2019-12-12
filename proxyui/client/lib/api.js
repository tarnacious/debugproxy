/* @flow */

import { arrayBufferToBase64, base64ToUint8Array, unicodeToBase64 } from 'lib/utils';
import type { DispatchType } from 'types';
import type { FlowType } from 'types/flow'

export function getResponse(session_id : string, request_id : string) {
  return window.fetch("/requests/response/" + session_id + "/" + request_id, {
    credentials: "same-origin"
  })
}

export function getRequest(session_id : string, request_id : string) {
  return window.fetch("/requests/request/" + session_id + "/" + request_id, {
    credentials: "same-origin"
  })
}

export function updateState(
  request_id : string,
  session_id : string,
  data: FlowType,
  csrf_token: string,
  dispatch : DispatchType) {

  dispatch({
    type: "REQUEST_UPDATE_STATE",
    data: data
  });

  var headers = new Headers();
  headers.append("X-CSRFToken", csrf_token);

  var body = JSON.stringify(data);

  return new Promise(function(resolve, reject) {
    window.fetch("/requests/state/" + session_id + "/" + request_id, {
      credentials: "same-origin",
      method: "POST",
      headers: headers,
      body: body,
    }).then(function(response) {
      response.text().then(function(text) {
        dispatch({
          type: "REQUEST_UPDATE_STATE_COMPLETE"
        });
        resolve(response)
      }.bind(this));
    }.bind(this)).catch(function() {
      reject()
    });
  });
};

export function updateResponse(
  request_id : string,
  session_id : string,
  data: string,
  csrf_token: string) {

  var headers = new Headers();
  headers.append("X-CSRFToken", csrf_token);
  const update_promise = new Promise(function(resolve, reject) {
    const update_server = window.fetch("/requests/response/" + session_id + "/" + request_id, {
      credentials: "same-origin",
      method: "POST",
      headers: headers,
      body: data
    })
    update_server.then(function(response) {
      response.text().then(function(text) {
        resolve(text)
      }).catch(function() {
        reject();
      });
    }).catch(function() {
      reject();
    });
  })

  return update_promise
}


export function updateRequest(
  request_id : string,
  session_id : string,
  data: string,
  csrf_token: string) {

  var headers = new Headers();
  headers.append("X-CSRFToken", csrf_token);

  const update_promise = new Promise(function(resolve, reject) {
    window.fetch("/requests/request/" + session_id + "/" + request_id, {
      credentials: "same-origin",
      method: "POST",
      headers: headers,
      body: data
    }).then(function(response) {
      response.text().then(function(text) {
        resolve(text)
      }).catch(function() {
        reject();
      });
    }).catch(function() {
      reject();
    });
  })
  return update_promise;
}
