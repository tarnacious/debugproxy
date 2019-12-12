/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'
import { prettyUrl, truncate } from 'lib/utils';
import moment from 'moment';


export class ProgressOneInfoComponent extends Component {

  props: Props;

  renderDetails() {
    if (!this.props.request) {
      return (
        <p>
          { " This state is active when a request has been received by the proxy  " }
        </p>
      )
    }
    const received_at = moment(this.props.request.client_conn.timestamp_start * 1000)
    const date = received_at.format('MMMM Do YYYY');
    const time = received_at.format('h:mm:ss a');
    const url = truncate(prettyUrl(this.props.request), 35);

    return (
      <p>
        { "A request for " }
        <a>
          { url }
        </a>
        { " was received on " }
        <span>
          { date }
        </span>
        { " at " }
        <span>
          { time }
        </span>
      </p>
    )
  }
  renderStatus() {
    if (!this.props.request) {
      return "A proxy connection has not yet been received.";
    }
    if (!this.props.request.response) {
      return (
        <span>The request is currently being held awaiting modification.</span>
        )
    }
    if (this.props.request.intercepted) {
      return "The request is still in progress.";
    } else {
      return "The request has now been fetched and a response returned to the client..";
    }
  }

  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box-right" key="key">
          <div className="info-box-container">
            <h1 className="title request">
              Proxy request received
            </h1>
            { this.renderDetails() }
            <p>
              { this.renderStatus() }
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
        transitionName="normal-fade"
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
    show: state.info.progress_state_1,
    request: state.flow.selected
  }
}

export default connect(mapStateToProps)(ProgressOneInfoComponent);
