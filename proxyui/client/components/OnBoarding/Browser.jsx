/* @flow */


import React, { Component } from 'react';
import { connect } from 'react-redux'

import type Action  from 'types/action';
import type State from 'types/state';

export class BrowserComponent extends Component {

  props: Props;

  render() {
  	return (

   		<div>
   			<p>For browsers on your local machine, you need to choose a different one to
        <p></p>
          what you are currently using debugProxy through. (?˙¿). e.g. Using Chrome now? The use Firefox or Safari etc to view the traffic.</p>
          <p>Go to the advanced settings of the other browser and change the proxy settings to the <span className="server">server</span> and <span className="port">port</span> listed here.</p>
          <p>If set-up correctly you will then be prompted to enter the <span className="username">username</span> and <span className="password">password</span> listed here. If you can still see this message then it is not configured correctly. If you need further help go to <a href="#">our tutorials</a></p>

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

export default connect(mapStateToProps)(BrowserComponent);
