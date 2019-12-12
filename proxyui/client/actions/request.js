/* @flow */

import _ from 'lodash';
import { updateResponse, updateRequest, updateState, getRequest, getResponse } from 'lib/api';
import { arrayBufferToBase64 } from 'lib/utils';

import type { DispatchType  } from 'types';
import type { StateType } from 'types/state';
import type { FlowType } from 'types/flow';

export function cancelRequestHeader() {
  return {
    type: "REQUEST_SELECT_REQUEST_HEADER",
    header: null
  }
}

export function updateRequestHeader() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state = getState();
    var updated = state.flow.selected;
    var header = state.request.selected_request_header;
    if (header && updated) {
      var newHeader = [
        header.name,
        header.value
      ];
      var index = header.index;
      if (index != null) {
        updated.request.headers[index] = newHeader;
      } else {
        updated.request.headers.push(newHeader);
      }
      dispatch(cancelRequestHeader())
      dispatch({
        type: "REQUEST_RECEIVE",
        request: updated
      })
    }
  }
}

export function createRequestHeader() {
  return {
    type: "REQUEST_SELECT_REQUEST_HEADER",
    header: {
      name: "",
      value: "",
      index: null
    }
  }
}


export function quickDeleteRequestHeader(index) {
  console.log(index)
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state = getState();
    var updated = _.clone(state.flow.selected);
    var selected = state.flow.selected;
    if (selected) {
      var newHeaders = selected.request.headers;
      newHeaders.splice(index, 1);
      updated.request.headers = newHeaders;
      dispatch({
        type: "REQUEST_RECEIVE",
        request: updated
      })
    }
  }
}

export function deleteRequestHeader() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state = getState();
    var updated = _.clone(state.flow.selected);
    var header = state.request.selected_request_header;
    var selected = state.flow.selected;
    if (header && selected) {
      var newHeaders = selected.request.headers;
      var index = header.index;
      if (index !== null && index !== undefined) {
        newHeaders.splice(index, 1);
        updated.request.headers = newHeaders;

        dispatch(cancelRequestHeader())
        dispatch({
          type: "REQUEST_RECEIVE",
          request: updated
        })
      }
    }
  }
}

export function changeRequestHeader(name: string, value: string) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state = getState();
    var selectedHeader = state.request.selected_request_header;
    if (selectedHeader) {
      dispatch({
        type: "REQUEST_SELECT_REQUEST_HEADER",
        header: {
          name: name,
          value: value,
          index: selectedHeader.index
        }
      })
    }
  }
}

export function editRequestHeader(header: [string, string], index: number) {
  return {
    type: "REQUEST_SELECT_REQUEST_HEADER",
    header: {
      name: header[0],
      value: header[1],
      index: index
    }
  }
}

export function updateRequestBody(value: string) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "UPDATE_REQUEST_BODY",
      value: value
    })
  }
}

export function loadRequest(request_id: string) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state = getState();
    dispatch({
      type: "REQUEST_LOAD_REQUEST_DATA"
    });
    getRequest(
      state.socket.session_id,
      request_id
    ).then(function(response) {
      response.json().then(function(data) {
        dispatch({
          type: "REQUEST_RECEIVE_REQUEST_DATA",
          data: data.response
        });
      }).catch(function() {
        console.error("ERROR: reading raw request");
      });
    }).catch(function() {
      console.error("ERROR: requesting raw request");
    });
  }
}
