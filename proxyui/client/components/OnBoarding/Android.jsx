/* @flow */


import React, { Component } from 'react';
import { connect } from 'react-redux'

import AndroidSsOne from 'components/OnBoarding/AndroidSsOne';
import AndroidSsTwo from 'components/OnBoarding/AndroidSsTwo';
import AndroidSsThree from 'components/OnBoarding/AndroidSsThree';
import AndroidSsFour from 'components/OnBoarding/AndroidSsFour';
export class AndroidComponent extends Component {

  props: Props;



  render() {
  	return (
   		<div>
   			<h2>Steps to configure Android</h2>
   			<ul className="instructions-list">
				  <li>Go to your <span className="blue">Wi-Fi settings</span> and press and hold down on the Wi-Fi connection you want to set-up, until a menu appears</li>
				  <li>Select '<span className="green">Modify network config.</span>'</li>
				  <li>Select '<span className="green">Show advanced settings</span>' [you may need to scroll down] and press on the arrow to change the Proxy from '<span className="base1">None</span>' to '<span className="green">Manual</span>'</li>
				  <li>Enter the <span className="yellow">Proxy Server</span> [listed left] in 'Proxy host name' and the <span className="magenta">Port</span> [also listed left] under 'Proxy port'</li>
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

export default connect(mapStateToProps)(AndroidComponent);
