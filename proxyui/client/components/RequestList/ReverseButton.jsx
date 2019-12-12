/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import { toggleListDirection } from 'actions/list'
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class ReverseButtonComponent extends Component {

  props: Props;

  toggle() {
    this.props.dispatch(toggleListDirection());
  }

  render() {
    if (this.props.reverse) {
      return (
        <button className="unreverse"
                title="Currently most recent Request last"
                onClick={ () => this.toggle() }
                >
          List Order<span>&nbsp;</span>
        </button>
      )
    } else {
      return (
        <button className="reverse"
                title="Currently most recent Request first"
                onClick={ () => this.toggle() }
                >
         List Order<span>&nbsp;</span>
        </button>
      )
    }
  }
}

type Props = {
  requests: RequestsType
};

function mapStateToProps(state: State): Props {
  return {
    reverse: state.flows.reverse,
  }
}

export default connect(mapStateToProps)(ReverseButtonComponent);
