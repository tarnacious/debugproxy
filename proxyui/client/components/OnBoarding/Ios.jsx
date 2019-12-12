/* @flow */


import React, { Component } from 'react';
import { connect } from 'react-redux'

export class IosComponent extends Component {

  props: Props;

  render() {
  	return (
   		<div>
   			<ul className="instructions-list">
        <p></p>
          <li></li>
          <li></li>
          <li></li>
          <li></li>
        </ul>

   			<p><a href="#" target="_blank">Click to view in a new tab</a></p>
   		</div>
   )
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: Action) {
  return {

  }
}

export default connect(mapStateToProps)(IosComponent);