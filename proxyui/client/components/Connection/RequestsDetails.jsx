/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import ConnectionInfo from 'components/Information/ConnectionInfo';
import ClearInfo from 'components/Information/ClearInfo';
import RequestCount from 'components/RequestList/RequestCount';
import { clearAll } from 'actions/list'
import { showClearInfo } from 'actions/info';

import type Action from 'types/action';
import type StateType from 'types/state';


export class RequestsDetailsComponent extends Component {

  props: Props;

  clear() {
    this.props.dispatch(clearAll());
    this.props.dispatch(showClearInfo(false))
  }

  rubbishBin() {
    return (
    <svg viewBox="0 0 22 22">
      <path className="bin" d="M15,4V1H7v3H1v4h2v13h16V8h2V4H15z M9,3h4v1H9V3z M6,18v-0.1V9h1h3v9H7.2H6z M16,17.9V18h-1.2H12V9h3h1V17.9z"
    />
    </svg>
    )
  }

  render() {
    return (
      <div className="request-counter">
        <RequestCount />
        <div className="clear-requests-button-container">
          <button className="clear-requests"
                  onClick={ this.clear.bind(this) }
                  onMouseOver={ () => this.props.dispatch(showClearInfo(true))}
                  onMouseOut={ () => this.props.dispatch(showClearInfo(false))} >
            { this.rubbishBin() }
          </button>
          <ClearInfo />
        </div>
      </div>
    )
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
  }
}

export default connect(mapStateToProps)(RequestsDetailsComponent);
