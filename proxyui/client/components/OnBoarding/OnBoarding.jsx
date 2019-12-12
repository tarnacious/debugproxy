/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import DeviceTabs from 'components/OnBoarding/DeviceTabs';
import Browser from 'components/OnBoarding/Browser';
import Android from 'components/OnBoarding/Android';
import Ios from 'components/OnBoarding/Ios';

import AndroidSsOne from 'components/OnBoarding/AndroidSsOne';
import AndroidSsTwo from 'components/OnBoarding/AndroidSsTwo';
import AndroidSsThree from 'components/OnBoarding/AndroidSsThree';
import AndroidSsFour from 'components/OnBoarding/AndroidSsFour';

import type { SelectTabType } from 'types/tabs';
import type Action from 'types/action';
import type StateType from 'types/state';


export class OnBoardingComponent extends Component {

  props: Props;

    renderActiveTab() {
      if (this.props.selected_tab == 'browser') {
        return (<Browser />)
      }
      if (this.props.selected_tab == 'android') {
        return (<Android />)
      }
      if (this.props.selected_tab == 'ios') {
        return (<Ios />)
      }
    }

    noTabSelected() {
      if (this.props.selected_tab == 'request') {
        return (
          <p>Select a tab for your desired device.</p>
        )
      }
    }

    renderActiveScreens() {
      if (this.props.selected_tab == 'browser') {
        return (
          <div>
          screens for browser...
          </div>
        )
      }
      if (this.props.selected_tab == 'android') {
        return (
          <div>
            <h2>Screenshots</h2>
            <div className="one"><AndroidSsOne /></div>
            <div className="two"><AndroidSsTwo /></div>
            <div className="three"><AndroidSsThree /></div>
            <div className="four"><AndroidSsFour /></div>
          </div>
        )
      }
      if (this.props.selected_tab == 'ios') {
        return (
          <div>
            <p>Here comes images about the iOS setup</p>
          </div>
        )
      }
    }

  connection_info() {
    var address = window.proxy_url
    var addressStr = address.toString()
    var userName = addressStr.slice(0,5)
    var password = addressStr.slice(6,11)
    var server = addressStr.slice(12,(addressStr.length - 5))
    var port = addressStr.slice((addressStr.length - 4), addressStr.length)

    return (
      <div className="session-info">
        <p className="username">Username: <span>{ userName }</span></p>
        <p className="password">Password:<span>{ password }</span></p>
        <p className="server">Proxy Server: <span>{ server }</span></p>
        <p className="port">Port: <span>{ port }</span></p>
        <div>
        <a href="/help/android" target="_blank">Setup on Android</a>
        </div>
      </div>

      );
  }

  render() {
    return (
      <div className="onboarding">
        <div className="onboarding-left">
          <h2>Proxy Session</h2>
          <p>Need help connecting your debugProxy session to a device or browser?</p>
          { this.connection_info() }

        </div>
        <div className="onboarding-right">
          <DeviceTabs />
          <div className={"device-panel " + ( this.props.selected_tab ) }>
            { this.noTabSelected() }
            { this.renderActiveTab() }
          </div>
        </div>
        <div className="screen-display">
          { this.renderActiveScreens() }
        </div>
      </div>
    )
  }
}

type Props = {
  selected_tab: SelectTabType
};

function mapStateToProps(state: State) {
  return {
    selected_tab: state.tabs.selected
  }
}

export default connect(mapStateToProps)(OnBoardingComponent);
