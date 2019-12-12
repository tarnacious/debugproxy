/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'

export class ResumeRequestInfoComponent extends Component {

  props: Props;


  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box" key="key" id="resume-info">
          <div className="info-box-container">
            <h1 className="title">Resume the request</h1>
            <p>
            Fetch the upstream response.
            </p>
            <p>[Shift] + r</p>
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
    show: state.info.resume_request_button
  }
}

export default connect(mapStateToProps)(ResumeRequestInfoComponent);
