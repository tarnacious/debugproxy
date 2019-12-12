/* @flow */

import { combineReducers } from 'redux';

import focus from 'reducers/focus';
import user from 'reducers/user';
import tabs from 'reducers/tabs';
import filter from 'reducers/filter';
import socket from 'reducers/socket';
import flows from 'reducers/flows';
import flow from 'reducers/flow';
import request from 'reducers/request';
import response from 'reducers/response';
import intercepts from 'reducers/intercepts';
import session from 'reducers/session';
import info from 'reducers/info';
import layout from 'reducers/layout';

const rootReducer = combineReducers({
  user,
  tabs,
  filter,
  socket,
  flows,
  flow,
  request,
  response,
  intercepts,
  info,
  layout,
  focus,
  session
})

export default rootReducer;
