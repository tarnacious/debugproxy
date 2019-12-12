/* @flow */

import Immutable from 'immutable';
import _ from 'lodash';

import type FlowsState from 'types/state/flows'
import type FlowsAction from 'types/actions/flows'

function receiveRequest(request, state) {
  const max_requests = 1000;
  let index = state.requests.findIndex(function(r) {
    return r.id == request.id;
  })

  if (index >= 0) {
    // request exists in the list, so we update the request in the list
    return Object.assign({}, state, {
      requests: state.requests.update(index, function(_) { return request })
    });
  } else {
    // request doesn't exist in the list so we work out where it should be
    // inserted into the list, based on the timestamp start.
    const index_of_older_request = state.requests.findIndex(function(r) {
      return r.client_conn.timestamp_start <= request.client_conn.timestamp_start;
    })

    var new_requests;
    if (index_of_older_request === -1) {
      // every request in the list is newer, this is presumably an update to a
      // request that is no longer on the list, maybe the list was cleared or
      // has been limited. in either case, we just append it to the end, if the
      // list is already at the maximum size, it will be dropped.
      new_requests = state.requests.push(request)
    } else {
      // insert the request above older requests
      new_requests = state.requests.insert(index_of_older_request, request)
    }

    // return update the maximum number of requests, set overflow flag if the
    // list has been reduced.
    return Object.assign({}, state, {
      overflow: new_requests.count() > max_requests,
      requests: new_requests.take(max_requests)
    });
  }
}

export function flows(state : FlowsState = {
  requests: Immutable.List(),
  overflow: false,
  reverse: false
}, action : FlowsAction) {
  switch (action.type) {
    case "REQUEST_CLEAR_ALL":
      return Object.assign({}, state, {
        selected: null,
        overflow: false,
        requests: Immutable.List(),
      })
    case "REQUEST_RECEIVE":
      const request = _.clone(action.request);
      const updated = receiveRequest(request, state);
      return updated;
    case "LIST_DIRECTION":
      return Object.assign({}, state, {
        reverse: action.reverse
      })

    default:
      return state
  }
}

export default flows;
