/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { prettyUrl, truncate } from 'lib/utils';
import { selectRequest } from 'actions/list'

import type { FlowType } from 'types/flow';
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class StatusCellComponent extends Component {

  props: Props;

  response(request) {
    if (request && request.response) {
      return (<span>{ "[" + request.response.status_code + "]"}</span>);
    } else if (request.error) {
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
    const {rowIndex, data, props} = this.props;
    return (
      <span className="response-code">{ this.response(data.get(rowIndex)) }</span>
    )
  }
}


export default StatusCellComponent;
