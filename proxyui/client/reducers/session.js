/* @flow */

export function session(state = {
  active: true
}, action) {
  switch (action.type) {
    case "SESSION_ACTIVE":
      return Object.assign({}, state, {
        active: true
      })
    case "SESSION_NOT_ACTIVE":
      return Object.assign({}, state, {
        active: false
      })
    default:
      return state
  }
}

export default session;
