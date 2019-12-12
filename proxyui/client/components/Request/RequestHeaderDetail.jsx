/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import HeaderDetail from 'components/Headers/HeaderDetail';
import { updateState } from 'lib/api';
import { canEditRequest } from 'lib/utils';
import {
  updateRequestHeader,
  deleteRequestHeader,
  changeRequestHeader,
  cancelRequestHeader
} from 'actions/request';

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class RequestHeaderDetailComponent extends Component {

  props: Props;

  canEdit() {
    return canEditRequest(this.props.request);
  }

  saveHeader() {
    this.props.dispatch(updateRequestHeader())
  }

  deleteHeader() {
    this.props.dispatch(deleteRequestHeader())
  }

  cancelHeader() {
    this.props.dispatch(cancelRequestHeader())
  }

  changeHeaders(name: string, value: string) {
    if (this.canEdit()) {
      this.props.dispatch(changeRequestHeader(name, value))
    }
  }

  renderDelete() {
    if (this.props.selected_header.index !== null && this.canEdit()) {
      return (
        <button className="red"
                onClick={ this.deleteHeader.bind(this) }>
          Delete
        </button>
      )
    }
  }

  valid() {
    return (this.props.selected_header.name.trim() &&
            this.props.selected_header.value.trim())
  }

  renderSave() {
    if (this.valid() && this.canEdit()) {
      return (
        <button className="green"
                onClick={ this.saveHeader.bind(this) }>
          Save
        </button>
      )
    }
  }

  renderCancel() {
    return (
      <button className="yellow" onClick={ this.cancelHeader.bind(this) }>Cancel</button>
    );
  }

  render() {
    return (
      <div className="response">
        <HeaderDetail name={ this.props.selected_header.name }
                      value={ this.props.selected_header.value }
                      index={ this.props.selected_header.index }
                      onChange={ this.changeHeaders.bind(this) }
                      onCancel={ this.cancelHeader.bind(this) }
                      onSave={ this.saveHeader.bind(this) }
                      editable={ true }
        />
        { this.renderDelete() }
        { this.renderCancel() }
        { this.renderSave() }
      </div>
    )
  }
}

type Props = {
  request: any,
  session_id: string,
  csrf_token: string,
  selected_header: any,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    request: state.flow.selected,
    session_id: state.socket.session_id,
    csrf_token: state.socket.csrf_token,
    selected_header: state.request.selected_request_header
  }
}

export default connect(mapStateToProps)(RequestHeaderDetailComponent);
