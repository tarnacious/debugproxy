/* @flow */

export function info(state : InfoStateType = {
  hotkeys: false,
  intercept_button: false,
  mouse_over_intercept_button: false,
  address: false,
  connection: false,
  progress_state_1: false,
  progress_state_2: false,
  progress_state_3: false,
  progress_state_4: false,
  clear_button: false,
  mouse_over_clear_button: false

}, action: DispatchInfoType) {
  switch (action.type) {
    case "INTERCEPT_INFO_MOUSE":
      return Object.assign({}, state, {
        mouse_over_intercept_button: _.clone(action.show)
      })
    case "INTERCEPT_INFO_SHOW":
      return Object.assign({}, state, {
        intercept_button: _.clone(action.show)
      })
    case "ADDRESS_INFO_MOUSE":
      return Object.assign({}, state, {
        mouse_over_address_button: _.clone(action.show)
      })
    case "ADDRESS_INFO_SHOW":
      return Object.assign({}, state, {
        address: _.clone(action.show)
      })
    case "CONNECTION_INFO_MOUSE":
      return Object.assign({}, state, {
        mouse_over_connection: _.clone(action.show)
      })
    case "CONNECTION_INFO_SHOW":
      return Object.assign({}, state, {
        connection: _.clone(action.show)
      })
    case "PROGRESS_INFO_1_MOUSE":
      return Object.assign({}, state, {
        mouse_over_progress_state_1: _.clone(action.show)
      })
    case "PROGRESS_INFO_1_SHOW":
      return Object.assign({}, state, {
        progress_state_1: _.clone(action.show)
      })
    case "PROGRESS_INFO_2_MOUSE":
      return Object.assign({}, state, {
        mouse_over_progress_state_2: _.clone(action.show)
      })
    case "PROGRESS_INFO_2_SHOW":
      return Object.assign({}, state, {
        progress_state_2: _.clone(action.show)
      })
    case "PROGRESS_INFO_3_MOUSE":
      return Object.assign({}, state, {
        mouse_over_progress_state_3: _.clone(action.show)
      })
    case "PROGRESS_INFO_3_SHOW":
      return Object.assign({}, state, {
        progress_state_3: _.clone(action.show)
      })
    case "PROGRESS_INFO_4_MOUSE":
      return Object.assign({}, state, {
        mouse_over_progress_state_4: _.clone(action.show)
      })
    case "PROGRESS_INFO_4_SHOW":
      return Object.assign({}, state, {
        progress_state_4: _.clone(action.show)
      })
    case "CLEAR_INFO_MOUSE":
      return Object.assign({}, state, {
        mouse_over_clear_button: _.clone(action.show)
      })
    case "CLEAR_INFO_SHOW":
      return Object.assign({}, state, {
        clear_button: _.clone(action.show)
      })
    case "RESUME_REQUEST_INFO_MOUSE":
      return Object.assign({}, state, {
        mouse_over_resume_request_button: _.clone(action.show)
      })
    case "RESUME_REQUEST_INFO_SHOW":
      return Object.assign({}, state, {
        resume_request_button: _.clone(action.show)
      })
    case "RESUME_RESPONSE_INFO_MOUSE":
      return Object.assign({}, state, {
        mouse_over_resume_response_button: _.clone(action.show)
      })
    case "RESUME_RESPONSE_INFO_SHOW":
      return Object.assign({}, state, {
        resume_response_button: _.clone(action.show)
      })
    case "HOTKEYS":
      return Object.assign({}, state, {
        hotkeys: _.clone(action.show)
      })

    default:
      return state
  }
}

export default info;
