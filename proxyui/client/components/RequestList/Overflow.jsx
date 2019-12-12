/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class OverflowComponent extends Component {

  props: Props;

  render() {
    if (this.props.overflow) {
      return (
        <div className="most-recent-warning">
          Only the most recent { this.props.requests.size } requests will be shown.
        </div>
      )
    } else {
      return false;
    }
  }
}

type Props = {
  requests: RequestsType
};

function mapStateToProps(state: State): Props {
  return {
    overflow: state.flows.overflow,
    requests: state.flows.requests
  }
}

export default connect(mapStateToProps)(OverflowComponent);
