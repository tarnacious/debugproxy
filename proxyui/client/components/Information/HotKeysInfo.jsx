/* @flow */

import React, { Component } from 'react';
import { connect } from 'react-redux'
import type Action from 'types/action';
import type StateType from 'types/state';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup'

export class HotKeysInfoComponent extends Component {

  props: Props;

  renderContent() {
    if (this.props.show) {
      return (
        <div className="hotkeys-overlay" key="key">
          <div>
            <div className="hotkeys-info">
              <h1>Keyboard Shortcuts</h1>
              <div className="hotkeys-table">
                <div className="hotkeys-column">
                  <div>
                    <span>escape&nbsp;</span>
                    Go back
                  </div>
                  <div>
                    <span>Shift ?</span>
                    Help (this screen)
                  </div>
                  <div>
                    <span>Shift c</span>
                    Clear all
                  </div>
                  <div>
                    <span>Shift r</span>
                    Resume current request
                  </div>
                  <div>
                    <span>h</span>
                    Previous tab
                  </div>
                  <div>
                    <span>l</span>
                    Next tab
                  </div>
                </div>
                <div className="hotkeys-column">
                  <div>
                    <span>j</span>
                    Previous request
                  </div>
                  <div>
                    <span>k</span>
                    Next request
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    } else {
      return false;
    }
  }

  render() {
    return (
      <CSSTransitionGroup
        transitionName="delayed-fade"
        transitionEnterTimeout={500}
        transitionLeaveTimeout={500}>
        { this.renderContent() }
      </CSSTransitionGroup>
    )
  }
}

type Props = {
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    show: state.info.hotkeys
  }
}

export default connect(mapStateToProps)(HotKeysInfoComponent);
