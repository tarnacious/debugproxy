/* @flow */

import type { UserState } from 'types/state/user'
import type { UserAction } from 'types/actions/user'

export function user(state : UserState = {
  connected: false
}, action : UserAction) {
  switch (action.type) {
    case "CONNECT":
      return Object.assign({}, state, {
        connected: true
      })
    case "DISCONNECT":
      return Object.assign({}, state, {
        connected: false
      })
    default:
      return state
  }
}

export default user;
