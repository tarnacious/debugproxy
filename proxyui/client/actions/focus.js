/* @flow */

import type { DispatchType  } from 'types';
import type { StateType } from 'types/state';

export function takeInputFocus(flow) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "INPUT_FOCUS",
      input_focus: true
    });
  }
}

export function releaseInputFocus(flow) {
  return (dispatch: DispatchType, getState: () => StateType) => {
    dispatch({
      type: "INPUT_FOCUS",
      input_focus: false
    });
  }
}
