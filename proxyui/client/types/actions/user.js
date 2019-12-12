/* @flow */

export type UserAction = (
  UserConnectAction
)

export type UserConnectAction = {
  type: "CONNECT" | "DISCONNECT"
}
