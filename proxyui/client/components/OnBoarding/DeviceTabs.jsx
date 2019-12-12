/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { showBrowser, showAndroid, showIos } from 'actions/tabs';
import type { SelectTabType } from 'types/tabs';
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class DeviceTabsComponent extends Component {

  showBrowser() {
    this.props.dispatch(showBrowser());
  }

  showAndroid() {
    this.props.dispatch(showAndroid());
  }

  showIos() {
    this.props.dispatch(showIos());
  }

  render() {
    return (
      <div className="tabs">
        <ul>
          <li id="browser-tab" className={ this.props.selected_tab == "browser" ? "active" : ""}
                onClick={ () => this.showBrowser() }>
            Browser
          </li>
          <li id="android-tab" className={ this.props.selected_tab == "android" ? "active" : "" }
                onClick={ () => this.showAndroid() }>
            Android
          </li>
          <li id="ios-tab" className={ this.props.selected_tab == "ios" ? "active" : "" }
                onClick={ () => this.showIos() }>
            iOS
          </li>

        </ul>
      </div>
    );
  }
}

type Props = {
  selected_tab: SelectTabType,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    selected_tab: state.tabs.selected
  }
}

export default connect(mapStateToProps)(DeviceTabsComponent);
