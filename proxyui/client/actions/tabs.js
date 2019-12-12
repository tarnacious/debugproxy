export function showOverview() {
  return {
    type: "CHANGE_TAB",
    selected_tab: 'overview'
  };
}

export function showResponse() {
  return {
    type: "CHANGE_TAB",
    selected_tab: 'response'
  };
}

export function showRequest() {
  return {
    type: "CHANGE_TAB",
    selected_tab: 'request'
  };
}

export function shiftLeft() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    const state = getState().tabs.selected;
    if (state == "request") {
      dispatch({
        type: "CHANGE_TAB",
        selected_tab: 'response'
      });
    }
    if (state == "response") {
      dispatch({
        type: "CHANGE_TAB",
        selected_tab: 'overview'
      });
    }
    if (state == "overview") {
      dispatch({
        type: "CHANGE_TAB",
        selected_tab: 'request'
      });
    }
  }
}

export function shiftRight() {
  return (dispatch: DispatchType, getState: () => StateType) => {
    const state = getState().tabs.selected;
    if (state == "request") {
      dispatch({
        type: "CHANGE_TAB",
        selected_tab: 'overview'
      });
    }
    if (state == "response") {
      dispatch({
        type: "CHANGE_TAB",
        selected_tab: 'request'
      });
    }
    if (state == "overview") {
      dispatch({
        type: "CHANGE_TAB",
        selected_tab: 'response'
      });
    }
  }
}

export function showBrowser() {
  return {
    type: "CHANGE_TAB",
    selected_tab: 'browser'
  };
}

export function showAndroid() {
  return {
    type: "CHANGE_TAB",
    selected_tab: 'android'
  };
}

export function showIos() {
  return {
    type: "CHANGE_TAB",
    selected_tab: 'ios'
  };
}