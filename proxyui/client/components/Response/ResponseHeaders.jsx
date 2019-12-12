/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import Header from 'components/Headers/Header';
import ResponseHeaderDetail from 'components/Response/ResponseHeaderDetail';
import { editResponseHeader, quickDeleteResponseHeader, createResponseHeader } from 'actions/response';
import { canEditResponse } from 'lib/utils';

import type { Action } from 'types/action';
import type { State } from 'types/state';

export class ResponseHeadersComponent extends Component {

  props: Props;

  canEdit() {
    return canEditResponse(this.props.selected);
  }

  editHeaders(header: [string, string], index: number) {
    this.props.dispatch(editResponseHeader(header, index));
  }

  deleteHeader(header: [string, string], index: number) {
    this.props.dispatch(quickDeleteResponseHeader(index));
  }

  createHeader() {
    this.props.dispatch(createResponseHeader());
  }

  renderHeader(header: [string, string], index: number) {
    if (this.props.selected_header && this.props.selected_header.index == index) {
      return (
        <ResponseHeaderDetail />
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
          <ResponseHeaderDetail />
        </div>
        )
    }
  }

  headers() {
    return (this.props.selected && this.props.selected.response) ? this.props.selected.response.headers : []
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
          <button className="violet" onClick={ () => this.createHeader() }>Add Header</button>
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
    selected_header: state.response.selected_response_header
  }
}

export default connect(mapStateToProps)(ResponseHeadersComponent);
