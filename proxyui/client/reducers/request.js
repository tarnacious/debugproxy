/* @flow */

import RequestAction from 'types/actions/request';
import RequestState from 'types/state/request';

export function request(state : RequestState = {
  loading_request: false,
  request_data: null,
  selected_request_header: null,
  updating_request: false,
  editing: null
}, action: RequestAction) {
  switch (action.type) {
    case "REQUEST_SELECT_REQUEST_HEADER":
        return Object.assign({}, state, {
          selected_request_header: action.header
        })
    case "REQUEST_CLEAR_ALL":
        return Object.assign({}, state, {
          loading_request: false,
          request_data: null,
          updating_request: false
        })
    case "REQUEST_SELECT":
      return Object.assign({}, state, {
        loading_request: false,
        selected_request_header: null,
        updating_request: false,
        request_data: null,
        editing: null
      });
    case "REQUEST_LOAD_REQUEST_DATA":
      return Object.assign({}, state, {
        loading_request: true
      });
    case "REQUEST_RECEIVE_REQUEST_DATA":
      return Object.assign({}, state, {
        loading_request: false,
        request_data: action.data
      });
    case "REQUEST_UPDATE_REQUEST_DATA":
      return Object.assign({}, state, {
        updating_request: true
      })
    case "UPDATE_REQUEST_BODY":
      return Object.assign({}, state, {
        request_data: action.value
      })
    case "REQUEST_UPDATE_REQUEST_DATA_COMPLETE":
      return Object.assign({}, state, {
        updating_request: false,
        request_data: action.data
      })
    case "REQUEST_EDIT_REQUEST":
      return Object.assign({}, state, {
        editing: action.request
      })
    default:
      return state
  }
}

export default request;
