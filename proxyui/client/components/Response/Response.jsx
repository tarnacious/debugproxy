/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import ResponseHeaderDetail from 'components/Response/ResponseHeaderDetail';
import ResponseHeaders from 'components/Response/ResponseHeaders';
import StatusCode from 'components/Response/StatusCode';

import type Action  from 'types/action';
import type State from 'types/state';


export class ResponseComponent extends Component {

  props: Props;

  render() {
    if (this.props.request.response) {
      return (
        <div className="response">
          <div>
            <StatusCode />
          </div>
          <ResponseHeaders />
        </div>
      )
    } else {
      return (
        <div className="response">
          <p>{ "There is no response data for this request" }</p>
        </div>
      )
    }
  }
}

type Props = {
  request: any,
  dispatch: Action,
  selected_header: any
};

function mapStateToProps(state : State) {
  return {
    request: state.flow.selected,
    selected_header: state.response.selected_response_header
  }
}

export default connect(mapStateToProps)(ResponseComponent);
