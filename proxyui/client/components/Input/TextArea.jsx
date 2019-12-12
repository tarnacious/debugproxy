/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { releaseInputFocus, takeInputFocus } from 'actions/focus';
import type Action from 'types/action';
import type State from 'types/state';

export class TextAreaComponent extends Component {

  props: Props;

  render() {
    const updatedProps = _.clone(this.props)
    delete updatedProps.dispatch
    return (
      <textarea {...updatedProps}
        onFocus={ () => this.props.dispatch(takeInputFocus()) }
        onBlur={ () =>  this.props.dispatch(releaseInputFocus()) }
      />);
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
  }
}

export default connect(mapStateToProps)(TextAreaComponent);

