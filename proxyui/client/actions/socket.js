import { connectSocket } from 'lib/socket';


export function startSocket() {
  return (dispatch, getState) => {
    dispatch({
      type: "SOCKET_CREDENTIALS",
      username: window.username,
      password: window.password,
      session_id: window.session_id,
      csrf_token: window.csrf_token
    })

    var socket = connectSocket(dispatch);
  }
}
