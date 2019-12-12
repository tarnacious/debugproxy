/* @flow */

import { showHotkeysInfo } from 'actions/info'
import { clearAll } from 'actions/list'
import { resume } from 'actions/flow'
import { nextRequest, previousRequest } from 'actions/list'
import { shiftLeft, shiftRight } from 'actions/tabs'

export function keyPress(key) {
	return (dispatch, getState) => {
    const state = getState();
    if (!state.focus.input_focus) {
      if (key.key == "?") {
        dispatch(showHotkeysInfo(true))
      }
      if (key.keyCode == 27) {
        dispatch(showHotkeysInfo(false))
      }
      if (key.key == "C") {
        dispatch(clearAll())
      }
      if (key.key == "r") {
        dispatch(resume())
      }
      if (key.key == 'h') {
        dispatch(shiftRight())
      }
      if (key.key == 'l') {
        dispatch(shiftLeft())
      }
      if (key.key == 'j') {
        dispatch(nextRequest())
      }
      if (key.key == 'k') {
        dispatch(previousRequest())
      }
    } else {
      // keyboard in use (ie in an input field)
    }
	}
}

