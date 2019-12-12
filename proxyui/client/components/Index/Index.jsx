/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'

import Layout from 'components/Layout/Layout';
import HotKeysInfo from 'components/Information/HotKeysInfo'
import Header from 'components/Header/Header';
import Footer from 'components/Header/Footer';

import { showProgressOneInfo } from 'actions/info';
import { startSocket } from 'actions/socket'
import { loadIntercepts } from 'actions/intercepts'
import { addFlow } from 'actions/flows'
import { keyPress } from 'actions/keypress'
import { pingServer } from 'actions/ping'

export class IndexComponent extends Component {

  componentDidMount() {
    this.props.dispatch(startSocket())
    this.props.dispatch(loadIntercepts())
    window.requests.reverse().forEach(request => {
      this.props.dispatch(addFlow(request))
    })
    setTimeout(() => this.pingServer(), 1000)
    document.addEventListener("keydown", function(e){
      this.props.dispatch(keyPress(e));
    }.bind(this));
  }

  pingServer() {
    this.props.dispatch(pingServer());
    setTimeout(() => this.pingServer(), 1000 * 30);
  }



  render() {
    return (
      <div>
        <Header />
        <HotKeysInfo />
        <Layout />
        <Footer />
      </div>
     )
  };
}


function mapStateToProps(state) {
  return {
    request: state.flow.selected
  }
}


export default connect(mapStateToProps)(IndexComponent)
