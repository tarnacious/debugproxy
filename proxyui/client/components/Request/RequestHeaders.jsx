/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import Header from 'components/Headers/Header';
import RequestHeaderDetail from 'components/Request/RequestHeaderDetail';
import { editRequestHeader, quickDeleteRequestHeader, createRequestHeader } from 'actions/request';
import { canEditRequest } from 'lib/utils';

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class RequestHeadersComponent extends Component {

  props: Props;

  canEdit() {
    return canEditRequest(this.props.selected);
  }

  editHeaders(header: [string, string], index: number) {
    this.props.dispatch(editRequestHeader(header, index));
  }

  deleteHeader(header: [string, string], index: number) {
    this.props.dispatch(quickDeleteRequestHeader(index));
  }

  createHeader() {
    this.props.dispatch(createRequestHeader());
  }

  renderHeader(header: [string, string], index: number) {
    if (this.props.selected_header && this.props.selected_header.index == index) {
      return (
        <RequestHeaderDetail />
      )
    } else {
      if (this.props.selected_header) {
        return (
            <Header header={ header }
              onClick={ () => this.editHeaders(header, index) }
            />)
      } else {
        if (this.canEdit()) {
          return (
            <Header header={ header }
              onClick={ () => this.editHeaders(header, index) }
              onDelete={ () => this.deleteHeader(header, index) }
            />
          )
        } else {
          return (
            <Header header={ header }
              onClick={ () => this.editHeaders(header, index) }
            />
          )
        }
      }
    }
  }

  isEditingNewHeader() {
    return this.props.selected_header && this.props.selected_header.index == null;
  }

  newHeader() {
    if (this.isEditingNewHeader()) {
      return (
        <div>
          <RequestHeaderDetail />
        </div>
        )
    }
  }

  headers() {
    return (this.props.selected && this.props.selected.request) ? this.props.selected.request.headers : []
  }

  renderHeaders() {
    return this.headers().map((header, index) => (
      <div key={ index }>
        { this.renderHeader(header, index) }
      </div>
    ));
  }

  renderExistingHeaders() {
    if (this.headers().length > 0 || this.isEditingNewHeader()) {
      return (
        <div>
        <div className="headers">
          { this.renderHeaders() }
        </div>
          { this.newHeader() }
        </div>
      )
    } else {
      return (
        <div className="no-headers">
          No headers
        </div>
      );
    }
  }

  renderAddHeader() {
    if (!this.props.selected_header && this.canEdit()) {
      return (
        <div>
          <button className="green margin-top" onClick={ () => this.createHeader() }>Add Header</button>
        </div>
      );
    }
  }

  render() {
    return (
      <div className="headers">
        { this.renderExistingHeaders() }
        { this.renderAddHeader() }
      </div>
    );
  }
}

type Props = {
  headers: any,
  selected_header: any,
  dispatch: Action
};

function mapStateToProps(state : State) {
  return {
    selected: state.flow.selected,
    selected_header: state.request.selected_request_header
  }
}

export default connect(mapStateToProps)(RequestHeadersComponent);
