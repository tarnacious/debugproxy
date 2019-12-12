/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { showAddressInfo } from 'actions/info'
import AddressInfo from 'components/Information/AddressInfo';
import ConnectionInfoButton from 'components/Connection/ConnectionInfoButton';
import type Action from 'types/action';
import type StateType from 'types/state';


export class ProxyDetailsComponent extends Component {

  props: Props;

  connection_info() {
    var address = window.proxy_url
    var addressStr = address.toString()
    var userName = addressStr.slice(0,5)
    var password = addressStr.slice(6,11)
    var server = addressStr.slice(12,(addressStr.length - 5))
    var port = addressStr.slice((addressStr.length - 4), addressStr.length)

    return (
      <div>
        <span className="username">{ userName }</span>:<span className="password">{ password }</span>@<span className="server">{ server }</span>:<span className="port">{ port }</span>


      </div>
      );
  }

  render() {
    return (
      <div className="connection-split">
        <div className="proxy-details">
          <span
            onMouseOver={ () => this.props.dispatch(showAddressInfo(true))}
            onMouseOut={ () => this.props.dispatch(showAddressInfo(false))}>
              { this.connection_info() }
          </span>
          <AddressInfo />
        </div>
        <ConnectionInfoButton />
      </div>
    )
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
  }
}

export default connect(mapStateToProps)(ProxyDetailsComponent);
