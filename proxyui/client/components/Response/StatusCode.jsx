/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { selectStatusCode, saveStatusCode } from 'actions/response'
import { canEditResponse } from 'lib/utils';

import type Action  from 'types/action';
import type State from 'types/state';


export class StatusCodeComponent extends Component {

  props: Props;

  canEdit() {
    return canEditResponse(this.props.request);
  }

  onChange(e : SyntheticInputEvent) {
    if (this.canEdit()) {
      this.props.dispatch(selectStatusCode(e.target.value))
    }
  }

  renderSave() {
    if (this.canEdit()) {
      return (
        <button className="green" onClick={ () => this.props.dispatch(saveStatusCode()) }>Save</button>
      )
    }
  }

  render() {
    if (this.props.selected != null) {
      return (
        <div className="status-code no-hover">
          <span>Status </span>
          <input autoFocus onChange={ this.onChange.bind(this) } value={ this.props.selected} />
          <div className="status-code-buttons-container">
            { this.renderSave() }
            <button className="yellow" onClick={ () => this.props.dispatch(saveStatusCode()) }>Cancel</button>
          </div>
        </div>
      )
    }
    if (this.props.request.response) {
      return (
        <div className="status-code" onClick={ () => this.props.dispatch(selectStatusCode(this.props.request.response.status_code)) }>
          <span>Status </span>{ this.props.request.response.status_code }
        </div>
      )
    }
  }
}

type Props = {
  dispatch: Action,
};

function mapStateToProps(state : State) {
  return {
    selected: state.response.selected_status_code,
    request: state.flow.selected
  }
}

export default connect(mapStateToProps)(StatusCodeComponent);
