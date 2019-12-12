/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'

export class ClearInfoComponent extends Component {

  props: Props;


  renderContent() {
    if (this.props.show) {
      return (
        <div className="info-box-right" key="key" id="clear-info">
          <div className="info-box-container">
            <h1 className="title clear">Clear all Requests</h1>
            <p>Clears all requests in the Request List. Request List only shows the most 100 recent Requests.
            </p>
            <p>[Shift] + c</p>
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
    show: state.info.clear_button
  }
}

export default connect(mapStateToProps)(ClearInfoComponent);
