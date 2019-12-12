/* @flow */

import React, { Component } from 'react'
import { Provider } from 'react-redux'
import Index from 'components/Index/Index';



export class RootComponent extends Component {

  render() {
    return (
      <Provider store={ this.props.store }>
        <Index />
      </Provider>
    )
  }
}
export default RootComponent
