/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { updateRequestBody, loadRequest } from 'actions/request'
import { releaseInputFocus, takeInputFocus } from 'actions/focus';
import AceEditor from 'react-ace';
import { canEditRequest } from 'lib/utils';

import * as ace from 'brace';
import 'brace/mode/html';
import 'brace/theme/solarized_dark';
import 'brace/theme/solarized_light';

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class BodyInfoComponent extends Component {

  props: Props;

  constructor() {
    super();
  }

  render() {
    if (!this.props.meta) {
      return null;
    }
    if (this.props.meta.error) {
      return (
        <p>
        this.props.meta.error
        </p>
      )
    }
    return (
      <p>
      The response encoding is {this.props.meta.charset}.
      </p>
    )
  }
}

type Props = {
  request: any,
  loading_request: boolean,
  request_data: string,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    meta: state.response.response_meta,
  }
}

export default connect(mapStateToProps)(BodyInfoComponent);
