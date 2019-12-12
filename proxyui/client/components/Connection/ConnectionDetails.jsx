/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import ProxyDetails from 'components/Connection/ProxyDetails';
import WebsocketDetails from 'components/Connection/WebsocketDetails';

import type Action from 'types/action';
import type StateType from 'types/state';


export class ConnectionDetailsComponent extends Component {

  props: Props;

  render() {
    return (
      <div className={ "connection-info " + (this.props.connected ? "connected" : "non-connected") }>
        <div className="connection-wrapper">
          <ProxyDetails />
          <WebsocketDetails />
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

export default connect(mapStateToProps)(ConnectionDetailsComponent);
