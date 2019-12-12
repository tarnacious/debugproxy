/* @flow */
import type { DispatchFilterType } from 'types/actions/filter';
import type { SelectTabType } from 'types/tabs';
import type { FlowType } from 'types/flow';
import Immutable from 'immutable';


export type DispatchType = (
  DispatchUserType |
  DispatchSocketType |
  DispatchFilterType |
  DispatchRequestType
) => null

export type DispatchUserType = DispatchConnectType;

export type DispatchSocketType = (
  DispatchSocketOpen |
  DispatchSocketError |
  DispatchSocketClose
)

export type DispatchConnectType = {
  type: "CONNECT" | "DISCONNECT"
}

export type DispatchTabType = {
  type: "CHANGE_TAB",
  selected_tab: SelectTabType
}

export type DispatchRequestType = (
  DispatchRequestLoadRequestDateType |
  DispatchRequestLoadResponseDateType |
  DispatchRequestReceiveRequestDataType |
  DispatchRequestRecieveResponseData |
  DispatchRequestUpdateStateComplete |
  DispatchRequestUpdateRequestDataComplete |
  DispatchRequestUpdateRequestData |
  DispatchRequestUpdateState |
  DispatchRequestReceive |
  DispatchRequestUpdate |
  DispatchRequestSelect |
  DispatchUpdateResponseData |
  DispatchRequestChangeQuery |
  DispatchRequestClearAll
)

export type DispatchRequestUpdateState = {
  type: "REQUEST_UPDATE_STATE",
  data: string
}

export type DispatchRequestUpdateRequestDataComplete = {
  type: "REQUEST_UPDATE_REQUEST_DATA_COMPLETE",
  data: string
}

export type DispatchRequestUpdateRequestData = {
  type: "REQUEST_UPDATE_REQUEST_DATA",
  data: string
}

export type DispatchRequestUpdateStateComplete = {
  type: "REQUEST_UPDATE_STATE_COMPLETE",
  data: string
}

export type DispatchRequestLoadRequestDateType = {
  type: "REQUEST_LOAD_REQUEST_DATA"
}

export type DispatchRequestLoadResponseDateType = {
  type: "REQUEST_LOAD_RESPONSE_DATA"
}

export type DispatchRequestReceiveRequestDataType = {
  type: "REQUEST_RECEIVE_REQUEST_DATA",
  data: string
}

export type DispatchRequestSelect = {
  type: "REQUEST_SELECT",
  request: FlowType
}

export type DispatchUpdateResponseData = {
  type: "REQUEST_UPDATE_RESPONSE_DATA" | "REQUEST_UPDATE_RESPONSE_DATA_COMPLETE",
  data: string
}

export type DispatchRequestUpdate = {
  type: "REQUEST_UPDATE",
  request: FlowType
};

export type DispatchRequestRecieveResponseData = {
  type: "REQUEST_RECEIVE_RESPONSE_DATA",
  data: string
}

export type DispatchRequestReceive = {
  type: "REQUEST_RECEIVE",
  request: FlowType
}

export type DispatchRequestChangeQuery = {
  type: "REQUEST_CHANGE_QUERY",
  query: string
}

export type DispatchRequestClearAll = {
  type: "REQUEST_CLEAR_ALL"
}


export type DispatchSocketClose = {
  type: "SOCKET_CLOSE"
}

export type DispatchSocketError = {
  type: "SOCKET_ERROR"
}

export type DispatchSocketOpen = {
  type: "SOCKET_OPEN",
  socket: any
}



