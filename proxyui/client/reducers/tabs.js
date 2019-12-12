/* @flow */

import Immutable from 'immutable';
import _ from 'lodash';

import type TabState from 'types/state/tabs'
import type TabAction from 'types/actions/tabs'

export function tabs(state : TabState = {
  selected: 'request'
}, action: TabAction) {
  switch (action.type) {
    case "CHANGE_TAB":
      return Object.assign({}, state, {
        selected: _.clone(action.selected_tab)
      })
    default:
      return state
  }
}

export default tabs;
