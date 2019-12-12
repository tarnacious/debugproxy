/* @flow */


export function showInterceptInfo(show: boolean) {
	return (dispatch, getState) => {
    dispatch({
      type: "INTERCEPT_INFO_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_intercept_button) {
          dispatch({
            type: "INTERCEPT_INFO_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "INTERCEPT_INFO_SHOW",
        show: show
      })
    }
	}
}

export function showAddressInfo(show: boolean) {
	return (dispatch, getState) => {

    dispatch({
      type: "ADDRESS_INFO_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_address_button) {
          dispatch({
            type: "ADDRESS_INFO_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "ADDRESS_INFO_SHOW",
        show: show
      })
    }
  }
}

export function showConnectionInfo(show: boolean) {

	return (dispatch, getState) => {

    dispatch({
      type: "CONNECTION_INFO_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_connection) {
          dispatch({
            type: "CONNECTION_INFO_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "CONNECTION_INFO_SHOW",
        show: show
      })
    }
  }
}

export function showProgressOneInfo(show: boolean) {
	return (dispatch, getState) => {

    dispatch({
      type: "PROGRESS_INFO_1_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_progress_state_1) {
          dispatch({
            type: "PROGRESS_INFO_1_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "PROGRESS_INFO_1_SHOW",
        show: show
      })
    }
  }
}

export function showProgressTwoInfo(show: boolean) {
	return (dispatch, getState) => {
    dispatch({
      type: "PROGRESS_INFO_2_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_progress_state_2) {
          dispatch({
            type: "PROGRESS_INFO_2_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "PROGRESS_INFO_2_SHOW",
        show: show
      })
    }
  }
}

export function showProgressThreeInfo(show: boolean) {
	return (dispatch, getState) => {
    dispatch({
      type: "PROGRESS_INFO_3_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_progress_state_3) {
          dispatch({
            type: "PROGRESS_INFO_3_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "PROGRESS_INFO_3_SHOW",
        show: show
      })
    }
  }
}

export function showProgressFourInfo(show: boolean) {
	return (dispatch, getState) => {
    dispatch({
      type: "PROGRESS_INFO_4_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_progress_state_4) {
          dispatch({
            type: "PROGRESS_INFO_4_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "PROGRESS_INFO_4_SHOW",
        show: show
      })
    }
  }
}

export function showClearInfo(show: boolean) {
  return (dispatch, getState) => {
    dispatch({
      type: "CLEAR_INFO_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_clear_button) {
          dispatch({
            type: "CLEAR_INFO_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "CLEAR_INFO_SHOW",
        show: show
      })
    }
  }
}

export function showResumeRequestInfo(show: boolean) {
  return (dispatch, getState) => {
    dispatch({
      type: "RESUME_REQUEST_INFO_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_resume_request_button) {
          dispatch({
            type: "RESUME_REQUEST_INFO_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "RESUME_REQUEST_INFO_SHOW",
        show: show
      })
    }
  }
}

export function showResumeResponseInfo(show: boolean) {
  return (dispatch, getState) => {
    dispatch({
      type: "RESUME_RESPONSE_INFO_MOUSE",
      show: show
    })
    if (show == true) {
      setTimeout(function() {
        var state = getState()
        if (state.info.mouse_over_resume_response_button) {
          dispatch({
            type: "RESUME_RESPONSE_INFO_SHOW",
            show: show
          })
        }
      }, 2000)
    } else {
      dispatch({
        type: "RESUME_RESPONSE_INFO_SHOW",
        show: show
      })
    }
  }
}

export function showHotkeysInfo(show: boolean) {
	return (dispatch, getState) => {
    dispatch({
      type: "HOTKEYS",
      show: show
    })
	}
}

