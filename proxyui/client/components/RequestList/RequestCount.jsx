/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class RequestCountComponent extends Component {

  props: Props;

  render() {
    return (
      <div className="request-count">
        { "Requests:  "} <span>{ this.props.requests.count() }</span>
      </div>
    )
  }
}

type Props = {
  requests: RequestsType
};

function mapStateToProps(state: State): Props {
  return {
    requests: state.flows.requests
  }
}

export default connect(mapStateToProps)(RequestCountComponent);



