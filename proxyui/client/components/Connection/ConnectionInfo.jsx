/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import { showConnectionInfo } from 'actions/layout'

import type Action from 'types/action';
import type StateType from 'types/state';


export class ConnectionInfoComponent extends Component {

  props: Props;

    noRequestsInfo() {
      if (!this.props.seen_request) {
        return (
          <h3 className="no-request-title">{ "No requests have been received yet" }</h3>
        )
      }
    }

  render() {
    var address = window.proxy_url
    var addressStr = address.toString()
    var userName = addressStr.slice(0,5)
    var password = addressStr.slice(6,11)
    var server = addressStr.slice(12,(addressStr.length - 5))
    var port = addressStr.slice((addressStr.length - 4), addressStr.length)



    return (
      <div className="onboarding">

        <div className="onboarding-container">
           { this.noRequestsInfo() }
          <p>
            Use the following connection details in conjunction with the device configuration guides [links below] to configure your device:
          </p>
          <div className="session-info">
            <p className="username">
              Username: <span>{ userName }</span>
            </p>
            <p className="password">
              Password: <span>{ password }</span>
            </p>
            <p className="server">
              Proxy Server: <span>{ server }</span>
            </p>
            <p className="port">
              Port: <span>{ port }</span>
            </p>
          </div>

          <p>
            If you have the <span className="curl">curl</span> program installed on your computer, you can
            test if the proxy works with this command:
          </p>
          <code className="curl">
            curl http://www.example.com --proxy { userName }:{ password }@{ server }:{ port }
          </code>
          <div className="guides">
            <a className="link-buttons yello-link" href="/help/curl" target="_blank">cURL</a>
            <a className="link-buttons green-link" href="/help/android" target="_blank">Android Config</a>
            <a className="link-buttons blue-link" href="/help/ios" target="_blank">iOS Config</a>
            <div className="hide" >
              <a className="link-buttons yellow-link" onClick={ () => this.props.dispatch(showConnectionInfo(false)) }>Ok, got it</a>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

type Props = {
};

function mapStateToProps(state: State) {
  return {
    seen_request: state.layout.seen_request
  }
}

export default connect(mapStateToProps)(ConnectionInfoComponent);
