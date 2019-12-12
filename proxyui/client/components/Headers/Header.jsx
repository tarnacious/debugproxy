/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import { truncate } from 'lib/utils';

export class HeaderComponent extends Component {

  constructor(props) {
    super(props);
    this.state = {
      hover: false
    };
  }

  onMouseOver() {
    this.setState({hover: true});
  }

  onMouseOut() {
    this.setState({hover: false});
  }

  onDelete(e) {
    e.stopPropagation();
    this.props.onDelete();
  }

  renderDelete() {
    if (this.state.hover && this.props.onDelete) {
      return (
        <span onClick={ (e) => this.onDelete(e) } className="show">delete</span>
      )
    } else {
      return (
        <span className="hide">delete</span>
      )
    }
  }

  render() {
    return (
      <div className="header-detail-container"
        onMouseOver={ () => this.onMouseOver() }
        onMouseOut={ () => this.onMouseOut() }
        onClick={ this.props.onClick }>
        <span className="header-name"> { this.props.header[0] } </span>
        <span className="header-value"> { truncate(this.props.header[1], 40) } </span>
        <span className="header-delete">
          { this.renderDelete() }
        </span>
      </div>
    );
  }
}

export default HeaderComponent;
