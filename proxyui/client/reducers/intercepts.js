/* @flow */

import Immutable from 'immutable';
import _ from 'lodash';

export function intercepts(state: any = {
  selected: false,
  loading_error: false,
  loading: true,
  saving: false,
  save_error: false,
  intercepts: Immutable.List(),
  editing: null
}, action: any) {
  switch (action.type) {
    case "INTERCEPT_CREATE":
      return Object.assign({}, state, {
        selected: _.clone({ "query": "" })
      })
    case "INTERCEPT_RECEIVE":
      return Object.assign({}, state, {
        loading: false,
        loading_error: false,
        intercepts: Immutable.List(action.intercepts)
      })
    case "INTERCEPT_RECEIVE_ERROR":
      return Object.assign({}, state, {
        loading_error: true
      })
    case "INTERCEPT_SELECT":
      return Object.assign({}, state, {
        save_error: false,
        selected: action.selected
      })
    case "INTERCEPTS_SAVE_START":
      return Object.assign({}, state, {
        saving: true
      })
    case "INTERCEPTS_DELETE_COMPLETE":
      var index = state.intercepts.findIndex(function(i) {
        return i.id == action.intercept.id;
      })
      var intercepts = state.intercepts.delete(index);
      return Object.assign({}, state, {
        saving: false,
        selected: null,
        intercepts: intercepts
      })
    case "INTERCEPTS_SAVE_COMPLETE":
      var index = state.intercepts.findIndex(function(i) {
        return i.id == action.intercept.id;
      })
      var updated = _.clone(action.intercept)

      if (index >= 0) {
        var intercepts = state.intercepts.update(index, function(_) { return updated });
      } else {
        var intercepts = state.intercepts.push(updated);
      }

      return Object.assign({}, state, {
        saving: false,
        selected: null,
        intercepts: intercepts
      })
    case "INTERCEPTS_SAVE_ERROR":
      return Object.assign({}, state, {
        save_error: true
      })
    case "INTERCEPT_CHANGE":
      var updated = _.clone(state.selected)
      updated.query = action.value
      return Object.assign({}, state, {
        selected: updated
      })

    default:
      return state;
  }
}

export default intercepts;
