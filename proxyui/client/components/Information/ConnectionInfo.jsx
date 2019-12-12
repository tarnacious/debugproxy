/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'

export class ConnectionInfoComponent extends Component {

  props: Props;

  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box-right" key="key" id="connection-info">
          <div className="info-box-container">
            <h1 className="title">
              Dashboard server connection
            </h1>
            <p>
              This shows the state of the connection between this page and
              debugProxy. This needs to be connected to see requests going through
              the proxy on this dashboard. When this is not connected, the proxy
              will still work but requests won't be shown in this dashboard.
            </p>
          </div>
        </div>
      )
    } else {
      return false;
    }
  }

  render() {
    return (
      <CSSTransitionGroup
        transitionName="delayed-fade"
        transitionEnterTimeout={500}
        transitionLeaveTimeout={500}>
        { this.renderContent() }
      </CSSTransitionGroup>
    )
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    show: state.info.connection
  }
}

export default connect(mapStateToProps)(ConnectionInfoComponent);
