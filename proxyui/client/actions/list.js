/* @flow */
import type { FlowType } from 'types/flow';

export function selectRequest(request: FlowType) {
  return {
    type: "REQUEST_SELECT",
    request: request
  }
}

export function toggleListDirection() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "LIST_DIRECTION",
      reverse: !getState().flows.reverse
    });
  };
}

export function nextRequest() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    const flows = getState().flows.requests;
    const selected = getState().flow.selected;
    if (selected && flows) {
      const index = flows.findIndex((flow) => flow.id == selected.id)
      if (index >= 0) {
        if ((index + 1) < flows.count()) {
          dispatch(selectRequest(flows.get(index + 1)))
        } else {
          console.log("last request selected");
        }
      } else {
        console.log("selected flow not found in list")
      }
      return;
    } else {
      console.log("no flow selected")
    }
  }
}

export function previousRequest() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    const flows = getState().flows.requests;
    const selected = getState().flow.selected;
    if (selected && flows) {
      const index = flows.findIndex((flow) => flow.id == selected.id)
      if (index >= 0) {
        if (index !== 0) {
          dispatch(selectRequest(flows.get(index - 1)))
        } else {
          console.log("first request selected");
        }
      } else {
        console.log("selected flow not found in list")
      }
      return;
    } else {
      console.log("no flow selected")
    }
  }
}

export function clearAll() {
  return (dispatch: DispatchType, getState: () => StateType) => {

    const state = getState()
    const session_id = state.socket.session_id;
    const csrf_token = state.socket.csrf_token;

    const headers = new Headers();
    headers.append("X-CSRFToken", csrf_token);

    window.fetch("/requests/clear/" + session_id, {
      credentials: "same-origin",
      method: "POST",
      headers: headers
    }).then(function(response) {
      console.log("clear request successful");
    }).catch(function() {
      console.log("clear request failed");
    });

    dispatch({
      type: "REQUEST_CLEAR_ALL"
    })
  }
}

