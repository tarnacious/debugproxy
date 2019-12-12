/* @flow */

import Immutable from 'immutable';
import _ from 'lodash';

import type RequestState from 'types/state/tabs'
import type RequestAction from 'types/actions/tabs'

export function flow(state : RequestsState = {
  selected: null,
}, action : RequestAction) {
  switch (action.type) {
    case "REQUEST_CLEAR_ALL":
      return Object.assign({}, state, {
        selected: null,
      })
    case "REQUEST_RECEIVE":
      let request = _.clone(action.request);
      if (!state.selected || state.selected.id == request.id) {
        return Object.assign({}, state, {
          selected: request
        });
      } else {
        return state;
      }
    case "REQUEST_SELECT":
      return Object.assign({}, state, {
        selected: action.request,
      })
    default:
      return state
  }
}

export default flow;
