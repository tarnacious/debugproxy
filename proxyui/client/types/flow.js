/* @flow */

export type RequestType = {
  headers: Array<[string, string]>,
  method: string,
  host: string,
  scheme: string,
  port: number,
  path: string
}

export type ResponseType = {
  headers: Array<[string, string]>,
  status_code: number
}

export type FlowType = {
  id: string,
  request: RequestType,
  response: ResponseType
}
