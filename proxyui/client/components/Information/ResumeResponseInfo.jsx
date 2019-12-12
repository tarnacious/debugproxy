/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'

export class ResumeResponseInfoComponent extends Component {

  props: Props;


  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box" key="key" id="resume-info">
          <div className="info-box-container">
            <h1 className="title response">Resume the response</h1>
            <p>
              Return the current response to the client.
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
    show: state.info.resume_response_button
  }
}

export default connect(mapStateToProps)(ResumeResponseInfoComponent);
