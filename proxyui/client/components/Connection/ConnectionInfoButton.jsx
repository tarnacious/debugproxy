/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import { showConnectionInfo } from 'actions/layout'
import type Action from 'types/action';
import type StateType from 'types/state';


export class ConnectionInfoButton extends Component {

  props: Props;

  className() {
    return  "connection-info-button " + (this.props.show_connection_info ? "inactive" : "active");
  }

  logo() {
    return (
      <svg viewBox="0 0 251.7 257.7">


        <g>
  <path id="head" className="st0" d="M97.7,61.5c-16.9,9.8-27.3,27.9-27.4,47.4h112.9c-0.1-19.6-10.5-37.6-27.4-47.4
    c1.2-25.9,23-46.7,49.7-46.7V0c-33,0-60.3,24.2-64.4,55.4c-4.7-1.2-9.5-1.8-14.4-1.8c-4.9,0-9.7,0.6-14.4,1.8
    C108.2,24.2,80.9,0,47.9,0v14.8C74.7,14.8,96.5,35.5,97.7,61.5z"/>
  <g id="body">
    <path className="st0" d="M193.4,168.2c1.5-9,2.3-18.1,2.2-27.2c0-0.6,0-1.3,0-1.9l41.7-13.8l14.3-49.7l-14.6-4L225,113.7l-30.2,10
      c-0.1-1.4-0.3-2.8-0.5-4.2H59.1c-0.2,1.4-0.3,2.7-0.5,4.1l-30.1-10L14.3,72.4L0,77.1l16.6,48.2l41.2,13.6c0,0.7,0,1.4,0,2
      c0,9.2,0.7,18.4,2.2,27.4l-43,14.2L5.2,255.3l14.9,2.3l10.3-63.9l32.7-10.9c10.5,38.5,35,65.5,63.5,65.5s53.1-27,63.6-65.6
      l32.2,10.7l9.3,64.1l15-2.1l-10.6-73.2L193.4,168.2z M159,226.2h-23.4l-1.3-7.9c-1.8,2.8-4.3,5.1-7.2,6.8
      c-2.9,1.6-6.1,2.4-9.4,2.3c-7.9,0-14.1-2.9-18.5-8.7c-4.4-5.8-6.6-13.5-6.6-23v-1.2c0-10.2,2.2-18.4,6.6-24.6
      c4.4-6.2,10.6-9.4,18.6-9.4c3,0,6,0.7,8.7,2.1c2.7,1.5,5,3.5,6.8,6v-23.1l-9.3-1.8v-10.5h26.7v80.7l8.3,1.8L159,226.2z"/>
    <path className="st0" d="M128.8,175.7c-2-1.2-4.2-1.8-6.5-1.7c-4-0.2-7.6,2.1-9.3,5.7c-2,3.8-2.9,8.7-2.9,14.8v1.2
      c0,5.6,0.9,10.1,2.8,13.3c1.9,3.2,5,4.9,9.3,4.9c2.3,0.1,4.6-0.5,6.6-1.6c1.9-1.1,3.5-2.6,4.6-4.5v-27.3
      C132.2,178.5,130.6,176.9,128.8,175.7z"/>
  </g>
</g>
      </svg>
    )
  }

  render() {
    return (
      <div className={ this.className() }
           onClick={ () => this.props.dispatch(showConnectionInfo(true)) } >
           { this.logo() }
      </div>
    )
  }
}

type Props = {
  connected: boolean,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    show_connection_info: state.layout.show_connection_info
  }
}

export default connect(mapStateToProps)(ConnectionInfoButton);
