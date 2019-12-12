/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { prettyUrl, truncate } from 'lib/utils';
import Header from 'components/Headers/Header';

export class HeadersComponent extends Component {

  onClick(header: [string, string], index: number) {
    this.props.onClick({
      key: header[0],
      value: header[1],
      index: index
    })
  }

  renderItems() {
    return this.props.headers.map((header, index) => (
      <div key={ index }>
        <Header header={ header }
          onClick={ () => this.onClick(header, index) }
        />
      </div>
    ));
  }

  newHeader() {
    this.props.onCreate()
  }

  render() {
    if (this.props.headers.length > 0) {
      return (
        <div>
          <div className="headers">
            { this.renderItems() }
          </div>
          <div>
            <button className="violet" onClick={ this.newHeader.bind(this) }>Add Header</button>
          </div>
        </div>
      );
    } else {
      return (
        <div>
          No headers
        </div>
      );
    }
  }
}

export default HeadersComponent;
