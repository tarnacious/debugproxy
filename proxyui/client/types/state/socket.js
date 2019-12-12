/* @flow */

import type { SocketType } from 'types/socket';

export type SocketState = {
  connected: boolean,
  socket: ?SocketType,
  username: string,
  password: string,
  session_id: string,
  csrf_token: string
}

export default SocketState
