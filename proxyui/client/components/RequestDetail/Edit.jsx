/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import _ from 'lodash';
import { prettyUrl, truncate, canEditRequest } from 'lib/utils';
import { cancelOverview, updateOverview, saveOverview } from 'actions/flow'
import Input from 'components/Input/Input';

import type { FlowType } from 'types/flow';
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class EditComponent extends Component {

  props: Props;

  canEdit() {
    return canEditRequest(this.props.request);
  }

  onCancel() {
    this.props.dispatch(cancelOverview());
    console.log("Cancel");
  }

  onSave() {
    var updated = _.cloneDeep(this.props.request);
    this.props.dispatch(saveOverview(updated));
  }

  onChangeMethod(e : SyntheticInputEvent) {
    if (this.canEdit()) {
      var updated = _.cloneDeep(this.props.request);
      updated.request.method = e.target.value;
      this.props.dispatch(updateOverview(updated))
    }
  }

  onChangeScheme(e : SyntheticInputEvent) {
    if (this.canEdit()) {
      var updated = _.cloneDeep(this.props.request);
      updated.request.scheme = e.target.value;
      this.props.dispatch(updateOverview(updated))
    }
  }

  onChangeHost(e : SyntheticInputEvent) {
    if (this.canEdit()) {
      var updated = _.cloneDeep(this.props.request);
      updated.request.host = e.target.value;
      this.props.dispatch(updateOverview(updated))
    }
  }

  onChangePort(e : SyntheticInputEvent) {
    if (this.canEdit()) {
      var updated = _.cloneDeep(this.props.request);
      updated.request.port = e.target.value;
      this.props.dispatch(updateOverview(updated))
    }
  }

  onChangePath(e : SyntheticInputEvent) {
    if (this.canEdit()) {
      var updated = _.cloneDeep(this.props.request);
      updated.request.path = e.target.value;
      this.props.dispatch(updateOverview(updated))
    }
  }

  valid() {
    return true;
  }

  renderSave() {
    if (this.valid() && this.canEdit()) {
      return (
        <button className="green"
                onClick={ () => this.onSave() }>
          Save
        </button>
      )
    }
  }

  render() {
    return (
      <div className="overview-inputs">
        <div>
          <Input
            onChange={ (e) => this.onChangeMethod(e) }
            value={ this.props.request.request.method }
          />
        </div>
        <div>
          <Input
            onChange={ (e) => this.onChangeScheme(e) }
            value={this.props.request.request.scheme}
          />
        </div>
        <div>
          <Input
            onChange={ (e) => this.onChangeHost(e) }
            value={this.props.request.request.host}
          />
        </div>
        <div>
          <Input
            onChange={ (e) => this.onChangePort(e) }
            value={this.props.request.request.port}
          />
        </div>
        <div className="last-overview-input">
          <Input
            onChange={ (e) => this.onChangePath(e) }
            value={this.props.request.request.path}
          />
        </div>
        <div>

        <button className="yellow" onClick={ () => this.onCancel() }>
          Cancel
        </button>
        { this.renderSave() }
        </div>
      </div>
    )
  }
}

type Props = {
  request: FlowType,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    request: state.request.editing,
  }
}

export default connect(mapStateToProps)(EditComponent);
