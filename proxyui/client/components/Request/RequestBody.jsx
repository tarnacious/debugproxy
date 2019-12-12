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

export class RequestBodyComponent extends Component {

  props: Props;

  constructor() {
    super();
  }

  loadRequest() {
    this.props.dispatch(loadRequest(this.props.request.id));
  }

  handleChange(s) {
    this.props.dispatch(updateRequestBody(s))
  }

  renderContent() {
    if (canEditRequest(this.props.request)) {
      const updatedProps = _.clone(this.props)
      delete updatedProps.dispatch

      return (
        <div className="editing-intercepted-request-container">
          <div className="editing-intercepted-request">
            <div className="titles green">
              Request Body (Editable)
            </div>
            <AceEditor {...updatedProps}
              autoFocus
              mode="html"
              onChange={ this.handleChange.bind(this)}
              name="intercepted-response-text"
              value={ this.props.request_data }
              theme="solarized_light"
              width="100%"
              height="350px"
              onFocus={ () => this.props.dispatch(takeInputFocus()) }
              onBlur={ () =>  this.props.dispatch(releaseInputFocus()) }
            />
          </div>
        </div>
      )
    } else {

      if (this.props.request_data == "") {
        return (
          <div className="no-body-content">
            <div className="titles green">
              Request Body (Completed)
            </div>
            No body content
          </div>);
      }

      var headers = this.props.request.request.headers.reduce(function(acc, value) {
        acc[value[0]] = value[1];
        return acc;
      }, {});

      var contentType = headers["Content-Type"];
      if (contentType && contentType.startsWith("image")) {
        return (
          <div className="img-container">
            <div className="titles green">
              Request Body (Completed)
            </div>
            <img src={ "data:" + contentType.split(";")[0] + ";base64," + this.props.request_data } />
          </div>
        )
      } else {
        return (
          <div className="">
            <div className="titles green">
              Request Body (Completed)
            </div>
            <AceEditor
              mode="html" // to be a read from file type
              readOnly={ true }
              name="response-body"
              value={ this.props.request_data }
              theme="solarized_dark"
              width="100%"
              height="350px"
              onFocus={ () => this.props.dispatch(takeInputFocus()) }
              onBlur={ () =>  this.props.dispatch(releaseInputFocus()) }
            />
          </div>
        )
      }
    }
  }

  render() {
    if (this.props.loading_request && this.props.selected_tab == "request") {
      return (
        <div className="intercepted-request-container">
          <div className="titles green">
              Request Body
            </div>
          <div>
            Loading Raw Request Data
          </div>
        </div>
      )
    }


    if (this.props.request_data != null && this.props.selected_tab == "request") {
      return (
        <div className="intercepted-request-container">
          { this.renderContent() }
        </div>
      )
    }
    if (this.props.selected_tab == "request") {
      return (
        <div className="load-intercepted-request-container">
          <a className="load-request"
             onClick={ () => this.loadRequest() }>
            Load Request Data
          </a>
        </div>
      )
    }


    return (
      false
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
    request: state.flow.selected,
    loading_request: state.request.loading_request,
    request_data: state.request.request_data,
    selected_tab: state.tabs.selected
  }
}

export default connect(mapStateToProps)(RequestBodyComponent);
