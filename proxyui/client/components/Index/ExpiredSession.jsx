/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import type Action from 'types/action';
import type StateType from 'types/state';


export class ExpiredSessionComponent extends Component {

  props: Props;

  render() {
    if (this.props.active) {
      return false;
    }
    return (
      <div className="expired-session">
        This proxy session has expired and will not accept any more requests.
        Please visit the <a href="/">home page</a> renable the session or create a new one.
      </div>
    )
  }
}

type Props = {
  active: boolean,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    active: state.session.active
  }
}

export default connect(mapStateToProps)(ExpiredSessionComponent);
