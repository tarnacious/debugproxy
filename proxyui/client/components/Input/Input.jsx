/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { releaseInputFocus, takeInputFocus } from 'actions/focus';
import type Action from 'types/action';
import type State from 'types/state';

export class InputComponent extends Component {

  props: Props;

  render() {
    const updatedProps = _.clone(this.props)
    delete updatedProps.dispatch
    return (
      <input {...updatedProps}
        onFocus={ () => this.props.dispatch(takeInputFocus()) }
        onBlur={ () =>  this.props.dispatch(releaseInputFocus()) }
      />);
  }

  componentWillUnmount() {
    // TODO: this should really check if it's currently selected.
    this.props.dispatch(releaseInputFocus())
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
  }
}

export default connect(mapStateToProps)(InputComponent);

