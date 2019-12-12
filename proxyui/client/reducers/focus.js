/* @flow */

export function focus(state = {
  input_focus: false
}, action: DispatchInfoType) {
  switch (action.type) {
    case "INPUT_FOCUS":
      return Object.assign({}, state, {
        input_focus: action.input_focus
      })
    default:
      return state
  }
}

export default focus;
