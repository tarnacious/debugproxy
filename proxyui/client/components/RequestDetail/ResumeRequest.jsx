/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { resume } from 'actions/flow'
import { showResumeRequestInfo } from 'actions/info';
import { showResponse } from 'actions/tabs';

import type { Action } from 'types/action';
import type { State } from 'types/state';
import ResumeRequestInfo from 'components/Information/ResumeRequestInfo';

export class ResumeRequestComponent extends Component {

  props: Props;

  onResume() {
    this.props.dispatch(resume())
  }

  resumeArrow() {
    return (
    <svg viewBox="0 0 45 45">
      <polygon points="18.9,16.5 16.5,17.7 22.7,21.6 22.7,21.6 24.3,22.5 22.7,23.4 22.7,23.4 22.6,23.5 22.6,23.5 22.6,23.5 16.5,27.1
    18.9,28.5 28.5,22.5   "/>
    </svg>
    )
  }



  showResponse() {
    this.props.dispatch(showResponse());
  }

  render() {
    if (this.props.request.intercepted && !this.props.request.response) {
      return (
        <div className="resume-buttons-container">

          <button type="button"
                  className="resume-request-button"
                  onMouseOver={ () => this.props.dispatch(showResumeRequestInfo(true)) }
                  onMouseOut={ () => this.props.dispatch(showResumeRequestInfo(false)) }
                  onClick={ () => {
                    this.onResume();
                    this.props.dispatch(showResumeRequestInfo(false));
                    this.showResponse();
                  }}>
            { this.resumeArrow() }
          </button>
          <ResumeRequestInfo />
        </div>
      );
    } else {
      return (
        <div className="blank"></div>
      );
    }
  }
}

type Props = {
  request: any,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    request: state.flow.selected,
    selected_tab: state.tabs.selected
  }
}

export default connect(mapStateToProps)(ResumeRequestComponent);
