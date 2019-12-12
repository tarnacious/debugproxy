/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'
import moment from 'moment';


export class ProgressTwoInfoComponent extends Component {

  props: Props;

  renderState() {
    if (!this.props.request) {
      return (
        <p>
          During this state a request to an upstream server is being made.
        </p>
      )
    }
    if (this.props.request.response) {
      const received_at = moment(this.props.request.server_conn.timestamp_start * 1000)
      const date = received_at.format('MMMM Do YYYY');
      const time = received_at.format('h:mm:ss a');
      const url = this.props.request.server_conn.address[0];
      return (
        <p>
          { " The host " }
          <a>
            { url }
          </a>
            { " was requested on " }
          <span>
            { date }
          </span>
            { " at " }
          <span>
            { time }
          </span>
        </p>
      )
    } else {
      return (
        <p>
          { "The proxy is waiting for modifications before making the upstream request" }
        </p>
      )
    }
  }

  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box-right" key="key">
          <div className="info-box-container">
            <h1 className="title request">
              Make upstream request
            </h1>
            { this.renderState() }
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
    show: state.info.progress_state_2,
    request: state.flow.selected
  }
}

export default connect(mapStateToProps)(ProgressTwoInfoComponent);
