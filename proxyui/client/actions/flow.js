/* @flow */

import _ from 'lodash';
import { updateResponse, updateRequest, updateState, getRequest, getResponse } from 'lib/api';

import type { DispatchType  } from 'types';
import type { StateType } from 'types/state';
import type { FlowType } from 'types/flow';

export function editOverview() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "REQUEST_EDIT_REQUEST",
      request: getState().flow.selected
    });
  }
}

export function cancelOverview() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "REQUEST_EDIT_REQUEST",
      request: null
    });
  }
}

export function updateOverview(request: FlowType) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "REQUEST_EDIT_REQUEST",
      request: request
    });
  }
}

export function saveOverview(request: FlowType) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state : StateType = getState();
    if (state.flow.selected) {
      updateState(
        state.flow.selected.id,
        state.socket.session_id,
        request,
        state.socket.csrf_token,
        dispatch).then(function() {
          dispatch({
            type: "REQUEST_EDIT_REQUEST",
            request: null
          })
          dispatch({
            type: "REQUEST_RECEIVE",
            request: request
          })
      });
    }
  }
}

function updateRequestState(newState: FlowType, dispatch, getState) {
  var state = getState();
  if (state.request.selected) {
    return
  }
}

export function resume() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    var state = getState();
    var selected = state.flow.selected

    if (selected) {
      var updated = _.clone(state.flow.selected);
      updated.intercepted = false;

      let updateStore = updateState(
        selected.id,
        state.socket.session_id,
        updated,
        state.socket.csrf_token,
        dispatch);

      const responseData = state.response.response_data;
      const requestData = state.request.request_data;

      updateStore.then(function() {

        if (responseData != null) {
          const update_promise = updateResponse(
            state.flow.selected.id,
            state.socket.session_id,
            responseData,
            state.socket.csrf_token);

          update_promise.then(function() {

            // Response saved, now resume
            let socket = getState().socket.socket;
            if (socket) {
              socket.send(JSON.stringify({
                type: "resume",
                id: updated.id
              }));
            }

            dispatch({
              type: "REQUEST_RECEIVE",
              request: updated
            })

          })

          update_promise.catch(function(e) {
            throw e;
          });

        } else if(requestData != null) {

          const update_promise = updateRequest(
            state.flow.selected.id,
            state.socket.session_id,
            requestData,
            state.socket.csrf_token);

          update_promise.then(function() {

            // Request saved, now resume
            let socket = getState().socket.socket;
            if (socket) {
              socket.send(JSON.stringify({
                type: "resume",
                id: updated.id
              }));
            }

            dispatch({
              type: "REQUEST_RECEIVE",
              request: updated
            })

          })


        } else {
          let socket = getState().socket.socket;
          if (socket) {
            socket.send(JSON.stringify({
              type: "resume",
              id: updated.id
            }));
          }
          dispatch({
            type: "REQUEST_RECEIVE",
            request: updated
          })
        }
      }).catch(function(e) {
        // dispatch error
        throw e;
      })
    }
  }
}
