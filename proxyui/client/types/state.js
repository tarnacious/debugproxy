/* @flow */

import type { FilterStateType } from 'types/state/filter';
import type { FlowStateType } from 'types/state/flow';
import type { FlowsStateType } from 'types/state/flows';
import type { RequestStateType } from 'types/state/request';
import type { ResponseStateType } from 'types/state/response';
import type { SocketStateType } from 'types/state/socket';
import type { TabsStateType } from 'types/state/tabs';


export type State = {
  flow: FlowStateType,
  flows: FlowsStateType,
  request: RequestStateType,
  response: ResponseStateType,
  socket: SocketStateType,
  tabs: TabStateType,
  filter: FilterStateType
}
