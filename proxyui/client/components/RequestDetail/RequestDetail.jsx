/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { prettyUrl, truncate, arrayBufferToBase64 } from 'lib/utils';
import Overview from 'components/RequestDetail/Overview';
import Request from 'components/Request/Request';
import Response from 'components/Response/Response';
import RequestProgress from 'components/RequestProgress/RequestProgress';
import Tabs from 'components/RequestDetail/Tabs';

import type { SelectTabType } from 'types/tabs';
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class RequestDetailComponent extends Component {

  renderActiveTab() {
    if (this.props.selected_tab == 'overview') {
      return (<Overview />)
    }
    if (this.props.selected_tab == 'request') {
      return (<Request />)
    }
    if (this.props.selected_tab == 'response') {
      return (<Response />)
    }
  }

  render() {
    if (this.props.request) {
      return (
        <div className="request-detail">
        <div className="titles titles-margin">
          Request Details
        </div>
          <Tabs />
          <div className="panel">
            { this.renderActiveTab() }
          </div>
        </div>
      );
    } else {
      return (
        <div className="request-detail loading-detail">
          No request selected
        </div>
      );
    }
  }
}

type Props = {
  request: any,
  selected_tab: SelectTabType,
  session_id: string,
  dispatch: Action
}


function mapStateToProps(state : State) {
  return {
    request: state.flow.selected,
    selected_tab: state.tabs.selected,
    session_id: state.socket.session_id,
  }
}

export default connect(mapStateToProps)(RequestDetailComponent);
