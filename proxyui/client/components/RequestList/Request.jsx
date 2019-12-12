/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { prettyUrl, truncate } from 'lib/utils';
import { selectRequest } from 'actions/list'

import type { FlowType } from 'types/flow';
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class RequestComponent extends Component {

  props: Props;

  response() {
    // Special handling for CONNECT events
    if (this.props.request.request.method == "CONNECT") {
      if (this.props.request.status == "disconnected") {
        return (<span>{ "disconnected" } </span>);
      } else {
        return (<span>{ "connected" } </span>);
      }
    }

    if (this.props.request && this.props.request.response) {
      return (<span>{ "[" + this.props.request.response.status_code + "]"}</span>);
    } else if (this.props.request.error) {
      return (<span>error</span>);
    } else {
      return (<span>{ "waiting" } </span>);
    }
  }

  handle_click() {
    this.props.dispatch(selectRequest(this.props.request));
  }

  class_name() {
    var names = ["request"]
    if (this.props.selected && this.props.selected.id === this.props.request.id) {
      names = names.concat(["selected"]);
    }

    if (this.props.request.intercepted) {
      names = names.concat(["intercepted"]);
    }

    return names.join(" ");
  }

  render() {
    // make the url length change with the width
    const url_width = this.props.width / 12;

    return (
      <div className={ this.class_name() } onClick={ () => this.handle_click() } >

        <span className="status-code">
          <span> { this.props.request.intercepted ? "!" : "" } </span>
          { this.props.request.request.method }
        </span>
        <span className="url">{ truncate(prettyUrl(this.props.request), url_width) }</span>
        <span className="response-code">{ this.response() }</span>
      </div>
    )
  }
}

type Props = {
  selected: FlowType,
  request: FlowType,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    selected: state.flow.selected
  }
}

export default connect(mapStateToProps)(RequestComponent);
