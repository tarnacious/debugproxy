/* @flow */

import Immutable from 'immutable';
import type { FlowType } from 'types/flow';

export type Flows = Immutable.List<FlowType>;

export type FlowsState = {
  requests: Flows
}

export default FlowsState;
