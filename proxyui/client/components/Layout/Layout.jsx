/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';

import HotKeysInfo from 'components/Information/HotKeysInfo'
import RequestCount from 'components/RequestList/RequestCount';
import ConnectionDetails from 'components/Connection/ConnectionDetails';
import Filter from 'components/Filters/Filter';
import InterceptContainer from 'components/Intercepts/InterceptContainer';
import RequestProgress from 'components/RequestProgress/RequestProgress';
import ProgressOneInfo from 'components/Information/ProgressOneInfo'; // needed for info boxes
import RequestBody from 'components/Request/RequestBody';
import ResponseBody from 'components/Response/ResponseBody';
import RequestDetail from 'components/RequestDetail/RequestDetail';
import RequestList from 'components/RequestList/RequestList';
import ExpiredSession from 'components/Index/ExpiredSession';
import OnBoarding from 'components/OnBoarding/OnBoarding';
import ConnectionInfo from 'components/Connection/ConnectionInfo';

export class LayoutComponent extends Component {

  props: Props;
  renderRequestProgress() {
    return <RequestProgress />;
  }

  renderRequestBody() {
    if (this.props.request) {
      return <RequestBody />;
    }
  }

  renderResponseBody() {
    if (this.props.request) {
      return <ResponseBody />;
    }
  }

  connectionInfo() {
    if (this.props.show_connection_info) {
      return (
        <ConnectionInfo />
      )
    } else {
      return false;
    }
  }

  render() {
    return (
        <div>
          <ConnectionDetails />
          <div className="dashboard">
            <ExpiredSession />
            { this.connectionInfo() }
            <div className="intercept-progress">
              <InterceptContainer />
              {this.renderRequestProgress()}
            </div>
            <div className="request-info">
              <div className={"request-info " + this.props.layout} >
                <RequestList />
                <RequestDetail />
              </div>
            </div>
          </div>
          <div>
            {this.renderRequestBody()}
            {this.renderResponseBody()}
          </div>
        </div>
      )
  };
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    layout: state.layout.layout,
    request: state.flow.selected,
    requests: state.flows.requests,
    show_connection_info: state.layout.show_connection_info
  }
}

export default connect(mapStateToProps)(LayoutComponent);
