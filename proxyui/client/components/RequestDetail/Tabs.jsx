/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { showOverview, showResponse, showRequest } from 'actions/tabs';
import type { SelectTabType } from 'types/tabs';
import type { Action } from 'types/action';
import type { State } from 'types/state';

export class TabsComponent extends Component {

  showOverview() {
    this.props.dispatch(showOverview());
  }

  showResponse() {
    this.props.dispatch(showResponse());
  }

  showRequest() {
    this.props.dispatch(showRequest());
  }

  render() {
    return (
      <div className="tabs">
        <ul>
          <li id="overview-tab" className={ (this.props.selected_tab == "overview" ? "active" : "") + (this.props.request.error ? " error" : "")}
                onClick={ () => this.showOverview() }>
            Overview
          </li>
          <li id="request-tab" className={ this.props.selected_tab == "request" ? "active" : "" }
                onClick={ () => this.showRequest() }>
            Request
          </li>
          <li id="response-tab" className={ this.props.selected_tab == "response" ? "active" : "" }
                onClick={ () => this.showResponse() }>
            Response
          </li>
        </ul>
      </div>
    );
  }
}

type Props = {
  selected_tab: SelectTabType,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    request: state.flow.selected,
    selected_tab: state.tabs.selected
  }
}

export default connect(mapStateToProps)(TabsComponent);
