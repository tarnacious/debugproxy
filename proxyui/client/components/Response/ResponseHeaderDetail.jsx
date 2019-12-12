/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import HeaderDetail from 'components/Headers/HeaderDetail';
import { updateState } from 'lib/api';
import {
  updateResponseHeader,
  deleteResponseHeader,
  changeResponseHeader,
  cancelResponseHeader} from 'actions/response';

import type Action  from 'types/action';
import type State from 'types/state';
import { canEditResponse } from 'lib/utils';

export class ResponseHeaderDetailComponent extends Component {

  props: Props;

  canEdit() {
    return canEditResponse(this.props.request);
  }

  saveHeader() {
    this.props.dispatch(updateResponseHeader())
  }

  deleteHeader() {
    this.props.dispatch(deleteResponseHeader())
  }

  cancelHeader() {
    this.props.dispatch(cancelResponseHeader())
  }

  changeHeaders(name: string, value: string) {
    if (this.canEdit()) {
      this.props.dispatch(changeResponseHeader(name, value))
    }
  }

  renderDelete() {
    if (this.props.selected_header.index !== undefined && this.props.selected_header.index !== null && this.canEdit()) {
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
  selected_header: any,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    request: state.flow.selected,
    selected_header: state.response.selected_response_header
  }
}

export default connect(mapStateToProps)(ResponseHeaderDetailComponent);
