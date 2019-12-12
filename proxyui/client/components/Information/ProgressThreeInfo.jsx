/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'


export class ProgressThreeInfoComponent extends Component {

  props: Props;

  renderState() {
    if (!this.props.request) {
      return (
        <div>
          <p>
            { "This state is active after the upstream request has been received." }
          </p>
          <p>
            { "Here the response can be modified before it is returned from the proxy" }
          </p>
          <p>
            { "A proxy connection has not yet been recieved." }
          </p>
        </div>
      )
    }
    if (this.props.request.response) {
      return (
        <p>
          { "An upstream response was received" }
        </p>
      )
    } else {
      return (
        <p>
          { "An upstream response for this request has not been received yet" }
        </p>
      )
    }
  }

  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box-right" key="key">
          <div className="info-box-container">
            <h1 className="title response">
              { "Receive upstream response" }
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
    show: state.info.progress_state_3,
    request: state.flow.selected
  }
}

export default connect(mapStateToProps)(ProgressThreeInfoComponent);
