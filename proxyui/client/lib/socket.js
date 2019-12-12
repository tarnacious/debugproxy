/* @flow */

import ReconnectingWebsocket from 'reconnecting-websocket';
import type { DispatchType } from 'types';

var websocketUrl = window.websocket_url + "?id=" + window.session_id;

export function connectSocket(dispatch : DispatchType) {
  console.log("Connnecting to websocket: " + websocketUrl);
  var socket = new ReconnectingWebsocket(websocketUrl);

  socket.onopen = function(event) {
    dispatch({
      type: "SOCKET_OPEN",
      socket: socket
    });
  }.bind(this);

  socket.onerror = function(error) {
    dispatch({
      type: "SOCKET_ERROR"
    });
  }.bind(this);

  socket.onclose = function(error) {
    dispatch({
      type: "SOCKET_CLOSE"
    });
  }.bind(this);

  socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data.type !== "log") {
      dispatch({
        type: "REQUEST_RECEIVE",
        request: data
      })
    }
  }.bind(this);
  return socket;
}
