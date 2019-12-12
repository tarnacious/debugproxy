/* @flow */

import type SocketState from 'types/state/socket'
import type SocketAction from 'types/actions/socket'

export function socket(state : SocketState = {
  username: "",
  password: "",
  session_id: "",
  csrf_token: "",
  socket: null,
  connected: false
}, action : SocketAction) {
  switch (action.type) {
    case "CSRF_TOKEN":
      return Object.assign({}, state, {
        csrf_token: action.csrf_token
      })
    case "SOCKET_CREDENTIALS":
      return Object.assign({}, state, {
        username: action.username,
        password: action.password,
        session_id: action.session_id,
        csrf_token: action.csrf_token
      })
    case "SOCKET_OPEN":
      return Object.assign({}, state, {
        connected: true,
        socket: action.socket
      })
    case "SOCKET_CLOSE":
      return Object.assign({}, state, {
        connected: false,
        socket: null
      })
    case "SOCKET_ERROR":
      return Object.assign({}, state, {
        connected: false,
        socket: null
      })
    default:
      return state
  }
}

export default socket;
