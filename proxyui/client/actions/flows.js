/* @flow */

import type { DispatchType  } from 'types';
import type { StateType } from 'types/state';
import type { FlowType } from 'types/flow';

export function addFlow(flow) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "REQUEST_RECEIVE",
      request: flow
    });
  }
}
