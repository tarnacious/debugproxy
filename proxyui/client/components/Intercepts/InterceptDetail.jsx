/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import Input from 'components/Input/Input';

import {
  saveIntercept,
  deleteIntercept,
  changeIntercept,
  cancelIntercept } from 'actions/intercepts';

export class InterceptDetailComponent extends Component {

  onChange(e : SyntheticInputEvent) {
    this.props.dispatch(changeIntercept(e.target.value))
    e.stopPropagation();
  }

  onKeyPress(e) {
    if (e.key == "Escape") {
      this.props.dispatch(cancelIntercept())
      return;
    }
    if (e.key == "Enter") {
      this.props.dispatch(saveIntercept())
      return;
    }
  }

  onDelete() {
    console.log(this.props.intercept.id);

    this.props.dispatch(deleteIntercept())
  }

  onSave() {
    this.props.dispatch(saveIntercept())

  }

  onCancel() {
    this.props.dispatch(cancelIntercept())
  }

  renderSaveError() {
    if (this.props.save_error) {
      return (
        <div>
        Save Error
        </div>
      )
    }
  }

  renderDelete() {
    if (this.props.intercept.id) {
      return (
        <button className="red-intercept" onClick={ this.onDelete.bind(this) }>Delete</button>
      )
    }
  }

  renderSave() {
    if (this.props.intercept.query && this.props.intercept.query.trim()) {
      return (
        <button className="green-intercept" onClick={ this.onSave.bind(this) }>Save</button>
      )
    }
  }

  render() {
    return (
      <div className="edit-intercept-container">
        <div className="titles">
          Intercepts
        </div>
        <Input autoFocus onChange={ this.onChange.bind(this) }
          onKeyDown={ this.onKeyPress.bind(this) }
          value={ this.props.intercept.query} />
        { this.renderSaveError() }
        { this.renderDelete() }
        <button className="yellow-intercept" onClick={ this.onCancel.bind(this) }>Cancel</button>
        { this.renderSave() }
      </div>
    )
  };
}


function mapStateToProps(state) {
  return {
    intercept: state.intercepts.selected,
    save_error: state.intercepts.save_error
  }
}


export default connect(mapStateToProps)(InterceptDetailComponent)
