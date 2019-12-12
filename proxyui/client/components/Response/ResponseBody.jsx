/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { updateResponseBody, loadResponse } from 'actions/response'
import { releaseInputFocus, takeInputFocus } from 'actions/focus';
import type Action  from 'types/action';
import type State from 'types/state';
import AceEditor from 'react-ace';
import { canEditResponse } from 'lib/utils';
import BodyInfo from 'components/Response/ResponseBodyInfo';

import * as ace from 'brace';
import 'brace/mode/html';
import 'brace/theme/solarized_dark';
import 'brace/theme/solarized_light';

export class ResponseBodyComponent extends Component {

  props: Props;

  constructor() {
    super();
  }

  loadResponse() {
    this.props.dispatch(loadResponse(this.props.request.id));
  }

  handleChange(s) {
    this.props.dispatch(updateResponseBody(s))
  }

  renderContent() {
    if (canEditResponse(this.props.request)) {
      const updatedProps = _.clone(this.props) // REVISIT: this is probably quite expensive here
      delete updatedProps.dispatch

      return (
          <div className="editing-intercepted-response-container">
            <div className="editing-intercepted-response">
              <div className="titles violet">
                Response Body (Editable)
              </div>
              <BodyInfo />
              <AceEditor {...updatedProps}
                autoFocus
                mode="html"
                onChange={ this.handleChange.bind(this)}
                name="intercepted-response-text"
                value={ this.props.response_data }
                theme="solarized_light"
                width="100%"
                height="350px"
                onFocus={ () => this.props.dispatch(takeInputFocus()) }
                onBlur={ () =>  this.props.dispatch(releaseInputFocus()) }
              />
            </div>
        </div>)
    } else {

      if (this.props.response_data == "") {
        return (
          <div className="no-body-content">
            <div className="titles violet">
              Response Body (Completed)
            </div>
            No body content
          </div>);
      }

      var headers = this.props.request.response.headers.reduce(function(acc, value) {
        acc[value[0]] = value[1];
        return acc;
      }, {});

      var contentType = headers["Content-Type"];
      if (contentType && contentType.startsWith("image")) {
        return (
          <div className="img-container">
            <div className="titles violet">
              Response Body (Completed)
            </div>
            <BodyInfo />
            <img src={ "data:" + contentType.split(";")[0] + ";base64," + this.props.response_data } />
          </div>
        )
      } else {
        return (
          <div className="">
            <div className="titles violet">
              Response Body (Completed)
            </div>
            <BodyInfo />
            <AceEditor
              mode="html" // to be a read from file type
              readOnly={ true }
              name="response-body"
              value={ this.props.response_data }
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
    if (this.props.loading_response && this.props.selected_tab == "response") {
      return (
        <div className="intercepted-response-container">
          <div className="titles violet">
            Response Body (Completed)
          </div>
          <div>
            Loading Raw Response Data
          </div>
        </div>
      )
    }

    if (this.props.response_data != null && this.props.selected_tab == "response") {
      return (
        <div className="intercepted-response-container">
          { this.renderContent() }
        </div>
      )
    }
    if (this.props.selected_tab == "response" && this.props.request.response) {
      return (
        <div className="load-intercepted-response-container">
          <a className="load-response"
             onClick={ () => this.loadResponse() }>
            Load Response Data
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
  loading_response: boolean,
  response_data: string,
  updating_response: boolean,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    request: state.flow.selected,
    loading_response: state.response.loading_response,
    response_data: state.response.response_data,
    updating_response: state.response.updating_response,
    selected_tab: state.tabs.selected
  }
}

export default connect(mapStateToProps)(ResponseBodyComponent);
