/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'

export class InterceptInfoComponent extends Component {

  props: Props;


  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box" key="1">
          <div className="info-box-container">
            <h1 className="create-intercept-title title">Create Intercepts</h1>
            <p>
            Create rules to pause and modify requests.
            </p>
            <p>
            Every request that goes through the proxy is checked if the
            requested URL matches any intercept. If it does, the request is paused
            before the upstream request is made and before the response is
            recieved.
            </p>
            <p>
            Paused (intercepted) requests can be modified at both these stages. The resume
            button is used to instruct the proxy server to continue processing the
            request.
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
        transitionName="delayed-fade"
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
    show: state.info.intercept_button
  }
}

export default connect(mapStateToProps)(InterceptInfoComponent);
