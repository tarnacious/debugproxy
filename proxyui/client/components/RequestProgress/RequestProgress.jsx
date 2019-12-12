/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { prettyUrl, truncate } from 'lib/utils';
import { showProgressOneInfo,
         showProgressTwoInfo,
         showProgressThreeInfo,
         showProgressFourInfo } from 'actions/info';
import { } from 'actions/info';

import ResumeRequest from 'components/RequestDetail/ResumeRequest'
import ResumeResponse from 'components/RequestDetail/ResumeResponse'
import ProgressOneInfo from 'components/Information/ProgressOneInfo';
import ProgressTwoInfo from 'components/Information/ProgressTwoInfo';
import ProgressThreeInfo from 'components/Information/ProgressThreeInfo';
import ProgressFourInfo from 'components/Information/ProgressFourInfo';
import { requestState } from 'lib/utils/';

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class RequestProgressComponent extends Component {

  props: Props;

  errorOnTheDanceFloor() {
    if (this.props.request) {
      if (this.props.request.error) {
        return " error"
      }
      return ""
    }
    return ""
  }

  requestStateName(n: number) {
    var state = requestState(this.props.request);
    if (state == n) {
      return "active"
    }
    if (n <= state) {
      return "complete"
    }
    return ""

  }

  className(n: number) {
    return "state state_" + n + " " + this.requestStateName(n)
  }

  renderResume() {
    if (!this.props.request) {
      return (
        <div className="progress-button-container">
          <div className="resume-buttons-container">
            <div className="resume-filler">&nbsp;</div>
            <div className="button-filler">&nbsp;</div>
          </div>
        </div>
      )
    }
    if (this.props.request.intercepted && this.props.request.response) {
      return (
        <div className="progress-button-container">
          <div className="resume-filler">&nbsp;</div>
          <ResumeResponse />
        </div>
      )
    }
    if (this.props.request.intercepted && !this.props.request.response) {
      return (
          <div className="progress-button-container">
            <div className="resume-filler">&nbsp;</div>
            <ResumeRequest />
          </div>
        )
    }
    return (
        <div className="progress-button-container">
          <div className="resume-buttons-container">
            <div className="resume-filler">&nbsp;</div>
            <div className="button-filler">&nbsp;</div>
          </div>
        </div>
      )
  }

  render() {
    if (false) {
      return false;
    }
    return (
      <div className="request-progress">
        <div className="titles titles-margin">
          Request Progress
        </div>
        <div className="">
          { this.renderResume() }
        </div>
        <div className="request-container">
          <div className="progress-title">Request</div>
            <div className="state-container">
              <div className={ this.className(1) }
                   onMouseOver={ () => this.props.dispatch(showProgressOneInfo(true)) }
                   onMouseOut={ () => this.props.dispatch(showProgressOneInfo(false)) }>
              </div>
              <ProgressOneInfo />
            </div>
            <div className="state-container">
              <div className={ (this.className(2)) + (this.errorOnTheDanceFloor()) }
                   onMouseOver={ () => this.props.dispatch(showProgressTwoInfo(true)) }
                   onMouseOut={ () => this.props.dispatch(showProgressTwoInfo(false)) }>
              </div>
              <ProgressTwoInfo />
            </div>
        </div>
        <div className="response-container">
          <div className="progress-title">Response</div>
            <div className="state-container">
              <div className={ (this.className(3)) + (this.errorOnTheDanceFloor()) }
                   onMouseOver={ () => this.props.dispatch(showProgressThreeInfo(true)) }
                   onMouseOut={ () => this.props.dispatch(showProgressThreeInfo(false)) }>
              </div>
              <ProgressThreeInfo />
            </div>
          <div className="state-container">
            <div className={ (this.className(4)) + (this.errorOnTheDanceFloor()) }
                 onMouseOver={ () => this.props.dispatch(showProgressFourInfo(true)) }
                 onMouseOut={ () => this.props.dispatch(showProgressFourInfo(false)) }>
            </div>
            <ProgressFourInfo />
          </div>
        </div>
      </div>
    )
  }
}

type Props = {
  request: any,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    request: state.flow.selected
  }
}

export default connect(mapStateToProps)(RequestProgressComponent);
