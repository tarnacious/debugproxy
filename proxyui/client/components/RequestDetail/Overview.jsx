/* @flow */


import React, { Component } from 'react';
import { connect } from 'react-redux'
import { prettyUrl, truncate } from 'lib/utils';
import Edit from 'components/RequestDetail/Edit'
import { cancelOverview, editOverview } from 'actions/flow'
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class OverviewComponent extends Component {

  props: Props;

  renderError() {
    if (this.props.request.error) {
      return (<p className="error"> { this.props.request.error.msg } </p>);
    }
  }

  edit() {
    this.props.dispatch(editOverview());
  }

  render() {
    if (this.props.editing) {
      return (
         <Edit />
      );
    }

    return (
      <div className="overview">
        <div className="request-overview" onClick={ () => this.edit() }>
          <span className="method">
            { this.props.request.request.method }
          </span>
          <span className="url">
            { prettyUrl(this.props.request, true) }
          </span>
        </div>
        { this.renderError() }
      </div>
    )
  }
}

type Props = {
  request: any,
  dispatch: Action
};

function mapStateToProps(state: Action) {
  return {
    request: state.flow.selected,
    editing: state.request.editing
  }
}

export default connect(mapStateToProps)(OverviewComponent);
