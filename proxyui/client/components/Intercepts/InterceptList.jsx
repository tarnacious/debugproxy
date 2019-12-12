/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux';
import Intercept from 'components/Intercepts/Intercept';

export class InterceptListComponent extends Component {

  renderItems() {
    return this.props.intercepts.map((e, index) => (
      <div key={ e.id }>
        <Intercept intercept={ e } />
      </div>
    ));
  }

  render() {
    return (
      <div className="intercept-items">
        { this.renderItems() }
      </div>
    )
  }
}


function mapStateToProps(state) {
  return {
    loading: state.intercepts.loading,
    loading_error: state.intercepts.loading_error,
    intercepts: state.intercepts.intercepts,
    selected: state.intercepts.selected
  }
}


export default connect(mapStateToProps)(InterceptListComponent)
