/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import ConnectionInfo from 'components/Information/ConnectionInfo';
import { showConnectionInfo } from 'actions/info'
import type Action from 'types/action';
import type StateType from 'types/state';


export class WebsocketDetailsComponent extends Component {

  props: Props;

  render() {
    return (
      <div className="connection-split-right">
        <div className="websocket-details">
          <div className={ this.props.connected ? "connected" : "not-connected" }
              onMouseOver={ () => this.props.dispatch(showConnectionInfo(true))}
              onMouseOut={ () => this.props.dispatch(showConnectionInfo(false))} >
            { this.props.connected ? "Connected" : "Not connected" }
          </div>
          <ConnectionInfo />
        </div>
      </div>
    )
  }
}

type Props = {
  connected: boolean,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    connected: state.socket.connected
  }
}

export default connect(mapStateToProps)(WebsocketDetailsComponent);
